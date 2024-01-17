#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, datetime, serial, logging, os, functools, threading
import serial.tools.list_ports
from src.i18n.Bms_i18n import *
from src.BMS.tools.CRC16Util import calc_crc
from utils.Common import Common
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, QObject, QTime, QDateTime, QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from .BmsLayout import BmsLayout
from .DataPars import pars_data
from .QssStyle import *
from src.OrderList import *

class ResThread(QThread):
    finished = pyqtSignal(str)
    
    def __init__(self, ser: serial):
        super(ResThread, self).__init__()
        self.is_running = True  # 线程停止标志位
        
        # 进度条收发状态，当num > 100，
        self.respondStatusNum = 0
        self.respondStatus = False
        
        self.ser = ser
        self.res = ''
    
    def run(self):
        while self.is_running:
            # 读取串口
            try:
                self.res = self.ser.read(1024).hex()
            except Exception as e:
                print(e)
            
            if self.res:
                # 传输信号
                self.respondStatusNum = 0
                self.respondStatus = True
                self.finished.emit(self.res)
            else:
                # 进度条状态
                self.respondStatusNum += 1
                if self.respondStatusNum > 100:
                    self.respondStatus = False
                
    
    def go(self):
        self.is_running = True
    
    def stop(self):
        self.is_running = False
    
    def get_running(self):
        return self.is_running
    
    def close(self):
        self.stop()
        self.ser.close()


class Portbms(BmsLayout):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDate()
        self.monitor_slotsTrigger()
        self.data_slotsTrigger()
        self.setParams_slotsTrigger()
        self.hisdata_slotsTrigger()
        self.sysset_slotsTrigger()
        self.pal_monitor_slotsTrigger()
        
    # 初始化数据
    def initDate(self):
        
        self.ser = serial.Serial()
        
        # self.bms_logic_i18n()

        # 创建日志文件
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        self.log_name = f'log/{now}.txt'
        if os.path.exists('log') == False:
            os.mkdir('log')

        with open(self.log_name, 'w', encoding='utf-8'): pass
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(lineno)d %(message)s')
        
        # 显示当前系统时间定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_func)
        self.timer.start(1000)

        # 显示进度条定时器
        self.step = 0
        self.proTimer = QTimer()
        self.proTimer.timeout.connect(self.pro_timer_func)
        self.connStatus.setFormat(bms_logic_label16)
        self.proTimer.start(100)
        
        # 实时监控的开启状态
        self.moni_switch = False
        
        # 充放电状态二进制
        self.dis_charge_mos_num = [0, 0, 0, 0]
        
        # 是否开启实时数据
        self.res_qtimer_switch = None
        
        # tab3写入参数指令集
        self.tab3_dic = {}
        
        # 是否在获取历史数据
        self.his_status = False
        
        # 擦除历史数据标志位
        self.clear_his_status = False
        
        # 电池设置标志位
        self.sys_status = False
        
        # 启用rs485协议解析
        self.rs485_res_status = False
        
        self.res_thread = ResThread(self.ser)
        self.res_thread.finished.connect(self.bms_qtimer_res_func)
        

    # 用得比较多的错误提示
    def assertStatus(self):
        if self.ser.isOpen() == False:
            QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
            return False
        elif self.his_status:
            QMessageBox.information(self, 'Error', '正在获取历史数据，请等待完成或暂停。', QMessageBox.Ok)
            return False
        return True
    
    # 暂时暂停 实时监控
    def stop_moni(self):
        if self.moni_switch:
            self.bms_qtimer_get_monitor.stop()
            
    # 业务完成开始 实时监控
    def start_moni(self):
        if self.moni_switch:
            self.bms_qtimer_get_monitor.start(int(self.space_combobox.currentText()) * 1000)
        
    # 实时监控 槽函数slots
    def monitor_slotsTrigger(self):
        # 打开串口
        self.open_port_btn.clicked.connect(self.openPort)
        
        # 刷新串口
        self.refresh_port_btn.clicked.connect(self.refresh_port)
        
        # 开始监控
        self.getP01_data_btn.clicked.connect(self.get_p01)
        # self.getP01_data_btn.clicked.connect(lambda: self.send_p01(order_list['P01']))

        # 登录
        self.pwd_btn.clicked.connect(self.pwd_btn_func)
        
        # 开关充电
        self.charge_sw.checkedChanged.connect(self.charge_mos_switch)
        
        # 开关放电
        self.disCharge_sw.checkedChanged.connect(self.discharge_mos_switch)
        
        # 开关强制休眠
        self.dormancy_sw.clicked.connect(self.dormancy_switch)
        
        # 测试模式
        self.testmode_btn.clicked.connect(self.testmode_btn_func)

    # 实时数据 槽函数slots
    def data_slotsTrigger(self):
        self.clearRowbtn.clicked.connect(functools.partial(self.clearRow_btn, self.tableWidget))

    # 历史数据 槽函数slots
    def hisdata_slotsTrigger(self):
        self.hisShow.clicked.connect(self.his_show)
        self.clearShow.clicked.connect(self.clear_his_msg)

    # 参数设置 槽函数slots
    def setParams_slotsTrigger(self):
        self.getTab3Res.clicked.connect(self.getTab3Res_func)
        self.clsTab3Res.clicked.connect(self.clearTab3)
        self.writeParam.clicked.connect(self.writeTab3Params)
        self.resetTab3.clicked.connect(self.reset_default)
        self.deriveParam.clicked.connect(self.deriveTab3Params)
        
        for k,v in self.tab3_form_dic.items():
            self.tab3_form_dic[k].textEdited.connect(functools.partial(self.setTab3Params, k))

    # 系统设置 槽函数slots
    def sysset_slotsTrigger(self):
        self.readCap.clicked.connect(self.readCap_func)
        self.writeCap.clicked.connect(self.writeCap_func)
        
        self.readTime.clicked.connect(self.readTime_func)
        self.sys_time = False   # 系统时间标志位
        
        self.writeTime.clicked.connect(self.writeTime_func)
        
        self.sys_edit_dic = {}
        sys_edit_obj = [
            self.designCap,
            self.remainCap,
            self.fullCap_Line
        ]
        for i in range(len(sys_edit_obj)):
            sys_edit_obj[i].textEdited.connect(functools.partial(self.setSysParams, sys_edit_obj[i]))

        self.adds_btn.clicked.connect(self.adds_btn_func)

    # 并联监控 槽函数slots
    def pal_monitor_slotsTrigger(self):
        # self.pal_check.clicked.connect(self.pal_check_func)
        self.pal_start.clicked.connect(self.pal_start_func)

    # 并联监控-开始获取信息按钮
    def pal_start_func(self):
        if self.pal_start.text() == palset_label2:
            if self.assertStatus() == False: return False
            self.stop_moni()
            self.pal_start.setText('取消')
            
            self.rs485_res_status = True
            self.repeat = False
            self.palTable.setColumnCount(int(self.pack_total.currentText()))
            self.palTable.clearContents()
            
            self.pal_start_time = QTimer()
            self.pal_start_time_setp = 1
            self.pal_start_time.timeout.connect(self.pal_start_func_timer)
            self.pal_start_time.start(2000)
        else:
            self.pal_start_time.stop()
            self.pal_start.setText(palset_label2)
            self.start_moni()
            
    # 并联监控-开始获取信息按钮-计时器
    def pal_start_func_timer(self):
        print(f'self.pal_start_time_setp:{self.pal_start_time_setp}')
        num = f'{self.pal_start_time_setp:02d}'
        adr = ''
        for i in num:
            adr += hex(ord(i))[2:]
        if self.pal_start_time_setp <= int(self.pack_total.currentText()):
            if self.repeat == False:
                self.repeat = True
                txt = f'7E 32 35 {adr} 34 36 34 32 45 30 30 32 {adr}'
            else:
                self.repeat = False
                txt = f'7E 32 35 {adr} 34 36 34 34 45 30 30 32 {adr}'
                self.pal_start_time_setp += 1
            self.send_msg(f'{txt}{Common.rs485_chksum(txt)}0D')

        else:
            self.pal_start_time.stop()
            self.pal_start.setText(palset_label2)
            self.rs485_res_status = False
            self.start_moni()

    # 开关充电
    def charge_mos_switch(self):
        
        if self.charge_sw.isChecked():
            self.dis_charge_mos_num[-1] = 1
            self.dis_charge_mos_num[-2] = 0
        else:
            self.dis_charge_mos_num[-1] = 0
            self.dis_charge_mos_num[-2] = 1
            
        num = hex(int(''.join(str(i) for i in self.dis_charge_mos_num), 2))[2:].rjust(4, '0')
        msg = f'01 06 3000 {num}'
        self.send_msg(msg + calc_crc(msg))

    # 开关放电
    def discharge_mos_switch(self):
        if self.disCharge_sw.isChecked():
            self.dis_charge_mos_num[-3] = 1
            self.dis_charge_mos_num[-4] = 0
        else:
            self.dis_charge_mos_num[-3] = 0
            self.dis_charge_mos_num[-4] = 1

        num = hex(int(''.join(str(i) for i in self.dis_charge_mos_num), 2))[2:].rjust(4, '0')
        msg = f'01 06 3000 {num}'
        self.send_msg(msg + calc_crc(msg))

    # 开关强制休眠
    def dormancy_switch(self):
        self.send_msg(bms_sleep_on + calc_crc(bms_sleep_on))

    def testmode_btn_func(self):
        if self.testmode_btn.text() == '进入测试模式':
            self.testmode_btn.setText('退出测试模式')
            self.charge_sw.setEnabled(True)
            self.disCharge_sw.setEnabled(True)
            
        else:
            self.testmode_btn.setText('进入测试模式')
            self.charge_sw.setEnabled(False)
            self.disCharge_sw.setEnabled(False)
            
            # 阻止信号发送
            self.charge_sw.blockSignals(True)
            self.charge_sw.setChecked(False)
            self.charge_sw.blockSignals(False)
            
            self.disCharge_sw.blockSignals(True)
            self.disCharge_sw.setChecked(False)
            self.disCharge_sw.blockSignals(False)
            
            self.dis_charge_mos_num = [0, 0, 0, 0]
            
            msg = f'01 06 3000 0000'
            self.send_msg(msg + calc_crc(msg))
            

    # 获取修改过的'系统设置-电量'参数
    def setSysParams(self, key):
        text = key.text()
        if text != '':
            try:
                num = int(float(text)*100)
            except ValueError as e:
                print(f"获取修改过的'系统设置-电量'参数1：{e}")
                key.setText('')
                return QMessageBox.critical(self, 'Error', bms_logic_label11, QMessageBox.Ok)
            
            if key == self.designCap:
                send_num = '01064000'
            elif key == self.remainCap:
                send_num = '01060318'
            else:
                send_num = '01060319'
            send_num = f'{send_num}{num:04x}'
            
            try:
                self.sys_edit_dic[key] = f'{send_num}{calc_crc(send_num)}'
            except ValueError as e:
                print(f"获取修改过的'系统设置-电量'参数2：{e}")
                key.setText('')
                return QMessageBox.critical(self, 'Error', bms_logic_label12, QMessageBox.Ok)

    # 读取系统设置-电量
    def readCap_func(self):
        if self.assertStatus() == False: return False
        self.stop_moni()
        self.sys_status = True
        self.sys_edit_dic = {}
        self.readCap_timer = QTimer()
        self.readCap_timer_step = 1
        self.readCap_timer.timeout.connect(self.readCap_func_timer)
        self.readCap_timer.start(1000)
        self.writeCap.setEnabled(True)
    
    # 读取系统设置-电量-计时器
    def readCap_func_timer(self):
        if self.readCap_timer_step == 1:
            self.send_msg(bms_sys_set2 + calc_crc(bms_sys_set2))
            self.readCap_timer_step += 1
        else:
            self.send_msg(bms_sys_set1 + calc_crc(bms_sys_set1))
            self.readCap_timer.stop()
            self.start_moni()
           
    # 读取系统设置-系统时间
    def readTime_func(self):
        if self.assertStatus() == False: return False
        self.sys_time = True
        self.send_msg(bms_sys_time + calc_crc(bms_sys_time))
    
    # 设置系统设置-电量
    def writeCap_func(self):
        if self.assertStatus() == False: return False
        self.stop_moni()
        if len(self.sys_edit_dic) != 0:
            ls = [v for k,v in self.sys_edit_dic.items()]
            self.ls_trv = list(zip(range(len(self.sys_edit_dic)), ls))
            
            self.writeCap_timer = QTimer()
            self.writeCap_timer_step = 0
            self.writeCap_timer.timeout.connect(self.writeCap_func_timer)
            self.writeCap_timer.start(1000)
            self.writeCap.setEnabled(False)
        else:
            return QMessageBox.critical(self, 'Error', bms_logic_label13, QMessageBox.Ok)
        
    # 设置系统设置-电量-计时器
    def writeCap_func_timer(self):
        if self.writeCap_timer_step < len(self.sys_edit_dic):
            self.send_msg(self.ls_trv[self.writeCap_timer_step][1])
            self.writeCap_timer_step += 1
            self.writeCap.setText('Writing...')
        else:
            self.writeCap_timer.stop()
            self.writeCap.setEnabled(True)
            self.writeCap.setText(sysset_label6)
            self.start_moni()
    
    # 写入系统设置-系统时间
    def writeTime_func(self):
        if self.assertStatus() == False: return False
        self.stop_moni()
        
        self.writeTime_timer = QTimer()
        self.writeTime_timer_step = 1
        self.writeTime_timer.timeout.connect(self.writeTime_func_timer)
        self.writeTime_timer.start(1000)
        self.writeTime.setEnabled(False)
    
    # 写入系统设置-系统时间-计时器
    def writeTime_func_timer(self):
        if self.writeTime_timer_step == 1:
            year = hex(self.now_time.dateTime().date().year() - 2000)[2:].rjust(2,'0')
            month = hex(self.now_time.dateTime().date().month())[2:].rjust(2,'0')
            msg = f'01062004{year}{month}'
            self.send_msg(msg + calc_crc(msg))
        elif self.writeTime_timer_step == 2:
            day = hex(self.now_time.dateTime().date().day())[2:].rjust(2,'0')
            hour = hex(self.now_time.dateTime().time().hour())[2:].rjust(2,'0')
            msg = f'01062005{day}{hour}'
            self.send_msg(msg + calc_crc(msg))
        elif self.writeTime_timer_step == 3:
            minute = hex(self.now_time.dateTime().time().minute())[2:].rjust(2,'0')
            second = hex(self.now_time.dateTime().time().second())[2:].rjust(2,'0')
            msg = f'01062006{minute}{second}'
            self.send_msg(msg + calc_crc(msg))
            self.writeTime.setEnabled(True)
            self.writeTime_timer.stop()
            self.start_moni()
            return QMessageBox.information(self, 'tips', '写入完毕，请重新获取数据。', QMessageBox.Ok)
        self.writeTime_timer_step += 1

    # 发送校准值
    def adds_btn_func(self):
        if self.assertStatus() == False: return False
        self.stop_moni()
        txt = self.adds_combox.currentText()
        hex_addr = self.datacalibration_adds_list[txt]
        if txt == '电流' or txt == '总压':
            hex_num = format(int(float(self.adds_txt.text()) * 100), '04x')
            print(hex_num)
        else:
            get_poi = int(self.adds_txt.text().split('.')[1])
            if get_poi > 0:
                return QMessageBox.information(self, 'tips', '请输入整数', QMessageBox.Ok)
        
            hex_num = format(int(float(self.adds_txt.text())), '04x')
        self.datacalibration_msg = hex_addr + hex_num + '000'
        
        self.adds_btn_time = QTimer()
        self.adds_btn_time_setp = 1
        self.adds_btn_time.timeout.connect(self.adds_btn_func_timer)
        self.adds_btn_time.start(1000)
    
    # 发送校准值定时器
    def adds_btn_func_timer(self):
        msg = self.datacalibration_msg + str(self.adds_btn_time_setp)
        self.send_msg(msg + calc_crc(msg))
        
        self.adds_progress.setValue(self.adds_btn_time_setp)
        
        self.adds_btn_time_setp += 1
        if self.adds_btn_time_setp == 7:
            self.adds_btn_time.stop()
            self.start_moni()
            return QMessageBox.information(self, 'tips', '校准完毕。', QMessageBox.Ok)

    # 显示进度条
    def pro_timer_func(self):
        if self.res_thread.respondStatus:
            self.connStatus.setFormat(bms_logic_label15)
            self.connStatus.setStyleSheet(GREEN_ProgressBar)
        else:
            self.connStatus.setFormat(bms_logic_label16)
            self.connStatus.setStyleSheet(RED_ProgressBar)
        self.step += 1
        self.connStatus.setValue(self.step)
        if self.step > 99:
            self.step = 0

    # 显示当前系统时间
    def update_func(self):
        self.now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.nowTime.setText(str(self.now))

    # 登录
    def pwd_btn_func(self):
        if self.pwd_line.text() == '123456':
            self.tabWidget.addTab(self.tab_data,tab_tabel6)
            self.pwd_line.setText('')
            self.pwd_btn.setEnabled(False)
            self.clearShow.setEnabled(True)
            self.writeParam.setEnabled(True)
            self.resetTab3.setEnabled(True)
            self.testmode_btn.setEnabled(True)
            QMessageBox.information(self, 'tips', bms_logic_label18, QMessageBox.Ok)
        else:
            QMessageBox.information(self, 'Error', bms_logic_label19, QMessageBox.Ok)

    # 打开/关闭串口
    def openPort(self):
        if self.open_port_btn.text() == com_label6:
            self.port = self.port_combobox.currentText()
            self.baud = self.baud_combobox.currentText()
            self.ser.port = self.port
            self.ser.timeout = 0.07
            self.ser.baudrate = int(self.baud)
            try:
                self.ser.open()
            except serial.SerialException as e:
                print(f'打开/关闭串口：{e}')
                return QMessageBox.information(self, 'Error', bms_logic_label20, QMessageBox.Ok)
            except Exception as e:
                print(f'串口异常：{e}')
                return QMessageBox.information(self, 'Error', '串口异常', QMessageBox.Ok)
            self.open_port_btn.setStyleSheet(open_Button)
            self.open_port_btn.setText(bms_logic_label2)
            
            # 开启接收数据定时器
            # self.bms_qtimer_res = QTimer()
            # self.bms_qtimer_res.timeout.connect(self.bms_qtimer_res_func)
            # self.bms_qtimer_res.start(1500)
            
            # thread = threading.Thread(target=self.thread_test)
            # thread.setDaemon = True
            # thread.start()
            
            # self.res_thread = ResThread(self.ser)
            # self.res_thread.finished.connect(self.bms_qtimer_res_func)
            self.res_thread.start()
            
        else:
            self.res_thread.close()
            self.open_port_btn.setStyleSheet(close_Button)
            self.open_port_btn.setText(com_label6)
            self.res_qtimer_switch = False
            # self.bms_qtimer_res.stop()

    def res_thread_func(self, res):
        print(res)
        # while True:
        #     try:
        #         self.thread_res = self.ser.read_all().hex()
        #         if self.thread_res != '':
        #             self.bms_qtimer_res_func(self.thread_res)
        #     except Exception as e:
        #         print(f'接收数据：{e}')
        #         return False

    # 刷新串口
    def refresh_port(self):
        self.port_combobox.clear()
        self.port_combobox.addItems(Common.load_serial_list())
    
    # 按钮-开始监控
    def get_p01(self):
        self.stop_monitor = 0   # 用于监测低压次数，如果达到600则自动停止监控
        
        if self.getP01_data_btn.text() == com_label8:
            if self.assertStatus() == False: return False
            self.moni_switch = True
            
            self.getP01_data_btn.setText(bms_logic_label4)
            self.getP01_data_btn.setStyleSheet(open_Button)
            self.low_vol = False
            
            # 定时器
            self.bms_qtimer_get_monitor = QTimer()
            self.bms_qtimer_get_monitor.timeout.connect(self.bms_qtimer_get_monitor_func)
            self.bms_qtimer_get_monitor_step = 0
            self.bms_qtimer_get_monitor.start(int(self.space_combobox.currentText()) * 1000)
            
        else:
            self.moni_switch = False
            self.bms_qtimer_get_monitor.stop()  # 暂停定时器
            
            self.getP01_data_btn.setText(com_label8)
            self.getP01_data_btn.setStyleSheet(close_Button)
    
    # 开始监控定时器
    def bms_qtimer_get_monitor_func(self):
        if self.bms_qtimer_get_monitor_step == 0:
            self.send_msg(bms_version + calc_crc(bms_version))
            self.bms_qtimer_get_monitor_step += 1
        else:
            self.send_msg(bms_monitor + calc_crc(bms_monitor))
        
    # 清空表格
    def clearRow_btn(self, tableWidget):
        rowPosition = tableWidget.rowCount()
        for rows in range(rowPosition)[::-1]:
            tableWidget.removeRow(rows)

    # 增加一行数据收发
    def add_tableItem(self, status: str, hexdata: str):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        rows = self.tableWidget.rowCount()
        # 最大行数
        if rows > 50:
            self.tableWidget.removeRow(0)
            rows = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rows + 1)

        # 添加时间
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(now)))

        # 添加↑↓标志并居中
        DirectionItem = QTableWidgetItem(status)
        DirectionItem.setTextAlignment(Qt.AlignCenter)
        DirectionItem.setFont(QFont('times', 14))
        self.tableWidget.setItem(rows, 1, DirectionItem)
        
        # 每两个字节增加一个空格
        space_hexdata = list(hexdata)
        for i in range(len(space_hexdata)-1)[::-1]:
            if i % 2 != 0:
                space_hexdata.insert(i+1, ' ')
        hexdata = ''.join(space_hexdata)

        # 写入日志文件
        with open(self.log_name, 'a+', encoding='utf-8') as f:
            f.write(f'{now}\t{status}\t{hexdata}\n')
        
        # 添加数据
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(hexdata))
        # 滚动条滚动到最下方
        self.tableWidget.verticalScrollBar().setSliderPosition(self.tableWidget.rowCount())

    # 获取修改过的'参数设置'参数
    def setTab3Params(self, key):
        if self.tab3_form_dic[key].text() != '':
            try:
                # txt = ''
                if key == '单体过充告警(V)' or key == '单体过充保护(V)' or key == '单体过充保护恢复(V)' \
                or key == '单体过放告警(V)' or key == '单体过放保护(V)' or key == '单体过放保护恢复(V)':
                    txt = int(float(self.tab3_form_dic[key].text()) * 1000)
                    print(1)
                    if txt > 4000:
                        self.tab3_form_dic[key].setText('')
                        return QMessageBox.critical(self, 'Error', bms_logic_label21, QMessageBox.Ok)      
                elif key == '总体过充告警(V)' or key == '总体过充保护(V)' or key == '总体过充保护恢复(V)' \
                or key == '总体过放告警(V)' or key == '总体过放保护(V)' or key == '总体过放保护恢复(V)':
                    txt = int(float(self.tab3_form_dic[key].text()) * 1000)
                    print(2)
                    if txt > 60000:
                        self.tab3_form_dic[key].setText('')
                        return QMessageBox.critical(self, 'Error', bms_logic_label22, QMessageBox.Ok)
                else:
                    print(3)
                    txt = int(self.tab3_form_dic[key].text()) * self.json_modbus[bms_setting][key][2]
                keyTxt = f"0106{self.json_modbus[bms_setting][key][3]}{txt:04x}"
            except Exception as e:
                print(f"获取修改过的'参数设置'参数：{e}")
                return QMessageBox.critical(self, 'Error', bms_logic_label11, QMessageBox.Ok)
            self.tab3_dic[key] = keyTxt + calc_crc(keyTxt)

    # 写入参数
    def writeTab3Params(self):
        if self.assertStatus() == False:
            return False
        if len(self.tab3_dic) == 0:
            return QMessageBox.information(self, 'tips', bms_logic_label13, QMessageBox.Ok)
        txt = ''
        for k,v in self.tab3_dic.items():
            txt += f'{k}: {self.tab3_form_dic[k].text()}\n'
        btn = QMessageBox.question(self, parset9_label3, f'{bms_logic_label24}：\n{txt}', QMessageBox.Yes | QMessageBox.No)
        if btn == QMessageBox.Yes:
            for k,v in self.tab3_dic.items():
                self.send_msg(v)
                time.sleep(0.5)

    # 读取 参数设置 数据
    def getTab3Res_func(self):
        if self.assertStatus() == False: return False
        self.tab3_dic.clear()
        self.send_msg(bms_setting + calc_crc(bms_setting))
        # self.writeParam.setEnabled(True)
        self.deriveParam.setEnabled(True)
        # self.resetTab3.setEnabled(True)

    # 保存参数设置为txt
    def deriveTab3Params(self):
        file_name =os.path.join(os.getcwd(), f'{tab_tabel3}.txt')
        if len(self.p03) != 0:
            with open(file_name, 'w', encoding='utf-8') as f:
                for k,v in self.p03.items():
                    f.write(f'{k}:{v}\n')
        QMessageBox.information(self, 'tips', f'{bms_logic_label26}:\n{file_name}', QMessageBox.Ok)

    # 参数设置清屏
    def clearTab3(self):
        for k,v in self.tab3_form_dic.items():
            self.tab3_form_dic[k].setText('')
        self.tab3_dic.clear()
    
    # 恢复默认值(出厂设置)
    def reset_default(self):
        if self.assertStatus() == False: return False
        self.send_msg(bms_reset + calc_crc(bms_reset))
    
    # 擦除历史数据
    def clear_his_msg(self):
        if self.ser.isOpen() == False:
            return QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
        self.send_msg(bms_clear_history + calc_crc(bms_clear_history))
        self.clearRow_btn(self.hisTable)
        self.hisTime.stop()
        self.hisShow.setEnabled(True)
        
    # 获取历史数据
    def his_show(self):
        if self.hisShow.text() == hisdata_label1:   # 获取最近历史数据(1~100)
            if self.ser.isOpen() == False:
                return QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
            self.stop_moni()
            self.clearRow_btn(self.hisTable)
            
            self.clear_his_status = False
            
            self.hisTime = QTimer()
            self.hisTime.timeout.connect(self.his_time_func)
            self.hisTime.start(1000)
            self.hisNum = 0
            self.his_status = True
            self.hisShow.setText('暂停')
            
        elif self.hisShow.text() == '暂停':
            self.hisTime.stop()
            self.his_status = False
            self.start_moni()
            self.hisShow.setText('继续')
            
        elif self.hisShow.text() == '继续':
            self.stop_moni()
            if self.continue_status:
                self.hisTime.start(1000)
                self.his_status = True
                self.hisShow.setText('暂停')
    
    # 获取最近历史数据计时器
    def his_time_func(self):
        if self.hisNum == 0:
            print('self.clear_his_status: {}'.format(self.clear_his_status))
            if self.clear_his_status == False:
                self.send_msg(bms_recent_history + calc_crc(bms_recent_history))
            try:
                if self.num_max == 0:
                    print('self.num_max: {}'.format(self.num_max))
                    QMessageBox.information(self, 'tip', bms_logic_label27, QMessageBox.Ok)
                    self.hisTime.stop()
            except Exception as e:
                print(f'获取最近历史数据计时器：{e}')
                return 0
            self.clear_his_status = True
            self.continue_status = True # 继续-暂停 标志位
            self.hisNum += 1
            print('self.hisNum: {}'.format(self.hisNum))
            return 0
        
        if self.num_max > 100:
            self.num_max = 100
        if self.hisNum <= self.num_max:
            num = f'{bms_history[:5]}{self.hisNum:03x}0036'
            self.send_msg(f'{num}{calc_crc(num)}')
            self.hisNum += 1
        else:
            self.hisTime.stop()
            self.his_status = False
            self.start_moni()
            self.hisShow.setText(hisdata_label1)
            self.continue_status = False

    # 发送数据
    def send_msg(self, data):
        hex_data = bytes.fromhex(data)
        try:
            self.ser.write(hex_data)
        except Exception as e:
            print(f'发送数据：{e}')
            self.ser.close()
            return False
        self.add_tableItem('↓', bytes.hex(hex_data))    # 在表格中输出

    # 接收数据(打开串口就会启用该线程进行数据接收并解析)
    def bms_qtimer_res_func(self, res):
        
        print(f'此次接收的数据：{res}')
        # 接收协议是否为 rs485
        if self.rs485_res_status == False:
            crc_error = False
            
            # 实时监控
            if res[:6] == f'{bms_monitor[:4]}bc' and len(res) == 386:
                print('实时监控')
                self.bms_bc_pass = False
                p01 = pars_data(res, bms_monitor + calc_crc(bms_monitor))
                # print(f'P01: {p01}')
                if len(p01) == 2:
                    crc_error = True
                else:
                    # BMS工作状态1（系统状态）
                    if sys_label1 in p01['BMS工作状态1']:
                        self.charg_status.setStyleSheet('color:#01B481')
                    else:
                        self.charg_status.setStyleSheet('color:#626262')
                        
                    if sys_label2 in p01['BMS工作状态1']:
                        self.disCharg_status.setStyleSheet('color:#01B481')
                    else:
                        self.disCharg_status.setStyleSheet('color:#626262')
                        
                    if sys_label3 in p01['BMS工作状态1']:
                        self.chargMos_status.setStyleSheet('color:#01B481')
                    else:
                        self.chargMos_status.setStyleSheet('color:#626262')
                    
                    if sys_label4 in p01['BMS工作状态1']:
                        self.disChargMos_status.setStyleSheet('color:#01B481')
                    else:
                        self.disChargMos_status.setStyleSheet('color:#626262')
                    
                    if sys_label5 in p01['BMS工作状态1']:
                        self.batCharg_status.setStyleSheet('color:#01B481')
                    else:
                        self.batCharg_status.setStyleSheet('color:#626262')
                        
                    if sys_label6 in p01['BMS工作状态1']:
                        self.full_status.setStyleSheet('color:#01B481')
                    else:
                        self.full_status.setStyleSheet('color:#626262')

                    if len(p01['故障位']) > 0:
                        for _ in p01['故障位']:
                            txt = '\n'.join(p01['故障位'])
                            self.error_body.setText(txt)
                    else:
                        self.error_body.setText('')

                    warn_txt = '\n'.join(p01['警告位1']) + '\n' + '\n'.join(p01['警告位2'])
                    self.warn_body.setText(warn_txt)
                    protect_txt = '\n'.join(p01['保护位1']) + '\n' + '\n'.join(p01['保护位2'])
                    self.protect_body.setText(protect_txt)

                    # 电池信息
                    self.soc_pr.setValue(int(p01['SOC']))
                    self.soh_pr.setValue(int(p01['SOH']))
                    self.battery_label1_line.setText(p01[battery_label1])
                    self.battery_label2_line.setText(p01[battery_label2])
                    self.battery_label3_line.setText(p01[battery_label3])
                    self.battery_label4_line.setText(p01[battery_label4])
                    self.battery_label5_line.setText(p01[battery_label5])
                    
                    # 单体电压
                    self.cellLine1.setText(p01[vol_label17 + '(V)'])
                    self.cellLine2.setText(p01[vol_label18 + '(V)'])
                    self.cellLine3.setText(p01[vol_label19 + '(V)'])
                    
                    # 数据显示
                    display_data = [
                        self.cell_temp_16, 
                        self.tem_other, 
                        self.cell_vol_16,
                    ]
                    for index in range(len(display_data)):
                        for k,v in display_data[index].items():
                            display_data[index][k].setText(p01[k])
                            
                    if (f'cell{bms_parse_label2}' in protect_txt or f'pack{bms_parse_label2}' in protect_txt) and self.low_vol == False:
                        self.stop_monitor += 1
                        # print(self.stop_monitor)
                        if self.stop_monitor >= 600:
                            self.low_vol = True
                            self.bms_qtimer_get_monitor.stop()
                            self.moni_switch = False
                            self.getP01_data_btn.setText(com_label8)
                            self.getP01_data_btn.setStyleSheet(close_Button)
                            QMessageBox.information(self, 'tips', bms_logic_label28, QMessageBox.Ok)
            # 参数设置
            elif res[:6] == f'{bms_setting[:4]}b6' and len(res) == 374:
                print('参数设置')
                self.p03 = pars_data(res, bms_setting + calc_crc(bms_setting))
                if len(self.p03) == 2:
                    crc_error = True
                else:
                    for k,v in self.p03.items():
                        try:
                            self.tab3_form_dic[k].setText(v)
                        except KeyError as e:
                            # print(f'参数设置：{e}')
                            continue
            # 历史数据
            elif res[:6] == f'{bms_history[:4]}6c' and len(res) == 226:
                print('历史数据')
                p06 = pars_data(res, bms_history + calc_crc(bms_history))
                if len(p06) == 2:
                    crc_error = True
                else:
                    rows = self.hisTable.rowCount()
                    self.hisTable.setRowCount(rows + 1)
                    count = 0
                    for k,v in p06.items():
                        self.hisTable.setItem(rows, count, QTableWidgetItem(p06[k]))
                        count += 1
            # 读取版本号
            elif res[:6] == '010304' and len(res) == 18:
                print('读取版本号')
                v1 = int(res[6:8], 16)
                v2 = int(res[8:10], 16)
                v3 = int(res[10:12], 16)
                v4 = int(res[12:14], 16)
                self.version.setText(f'{ver_label1}：{v1}.{v2}.{v3}.{v4}')
            # 读取系统设置-系统时间
            elif res[:6] == f'{bms_sys_time[:4]}06' and self.sys_time and len(res) == 22:
                print('读取系统设置-系统时间')
                sysTime_data = pars_data(res, bms_sys_time + calc_crc(bms_sys_time))
                year_month = sysTime_data['年月'].split('/')
                year = int(f'20{year_month[0]}')
                month = int(year_month[1])
                
                day_hour = sysTime_data['日时'].split('/')
                day = int(day_hour[0])
                hour = int(day_hour[1])
                
                minutes_seconds = sysTime_data['分秒'].split('/')
                minutes = int(minutes_seconds[0])
                seconds = int(minutes_seconds[1])
                
                thisTime = QDateTime.currentDateTime()
                thisTime.setDate(QDate(year, month, day))
                thisTime.setTime(QTime(hour, minutes, seconds))
                self.now_time.setDateTime(thisTime)
            # 读取系统设置-电量数据
            elif res[:6] == f'{bms_sys_set1[:4]}06' and len(res) == 22:
                print('读取系统设置-电量数据')
                ele_data = pars_data(res, bms_sys_set1 + calc_crc(bms_sys_set1))
                self.remainCap.setText(ele_data[f'{battery_label3}(AH)'])
                self.fullCap_Line.setText(ele_data[f'总容量(AH)'])
            # 读取系统设置-电量数据2
            elif res[:6] == f'{bms_sys_set2[:4]}02' and len(res) == 14 and self.sys_status == True:
                print('读取系统设置-电量数据2')
                ele_data = pars_data(res, bms_sys_set2 + calc_crc(bms_sys_set2))
                self.designCap.setText(ele_data[f'设计容量(AH)'])
                self.sys_status = False
            # 历史数据总数 
            elif res[:6] == f'{bms_recent_history[:4]}02' and len(res) == 14:
                print('历史数据总数')
                print(res[6:10])
                self.num_max = int(res[6:10], 16)
                print('self.num_max: {}'.format(self.num_max))
                
            if crc_error == False:
                self.add_tableItem('↑', res)
            else:
                self.add_tableItem(bms_logic_label29, res)
        else:
            # 接收 rs485 报文并处理
            if len(res) == 48:  # 确认 pack 地址是否存在
                # 如果这个长度拿到的是00，则表示设备不在线或未接入，显示offline并跳过解析
                if res[-14:-10] == '3030':
                    # 显示offline
                    temp = res[6:10]
                    hex2asc = ''
                    for i in range(0, len(temp), 2):
                        # 十六进制转换成ascii字符，如：30 32 转 02
                        hex2asc += chr(int(temp[i:i + 2], 16))
                    self.palTable.setItem(0, int(hex2asc)-1, QTableWidgetItem('OFFLINE'))
                    
                    # 并联发送定时器相关参数
                    self.repeat = False             # 重置循环发送的状态
                    self.pal_start_time_setp += 1   # 跳过获取告警量的指令
                    
                    self.add_tableItem('↑', res)
                    return 0
                
            elif len(res) == 312:  # 获取 PACK 模拟量响应信息
                msg = res[30:-10]  # 去掉前缀报文和校验码
                adr = ''
                for k,v in self.json_rs485['获取PACK模拟量响应信息'].items():
                    temp = ''
                    for i in range(v[0], v[0]+v[1], 2):
                        temp += chr(int(msg[i:i + 2], 16))
                    if k == 'Command':
                        adr = int(temp, 16)
                    elif palnum_label2 in k or bms_history_label3 in k: # 温度、电流
                        data = f'{Common.format_num(Common.signBit_func(temp) / abs(v[2]))} {v[3]}'
                    else:
                        # data = f'{int(temp, 16)} {v[3]}'
                        data = f'{Common.format_num(int(temp, 16) / abs(v[2]))} {v[3]}'
                    if k in self.col_labels:
                        self.palTable.setItem(self.col_labels.index(k), int(adr)-1, QTableWidgetItem(str(data)))
                
            elif len(res) == 200:  # 获取 PACK 告警量
                msg = res[30:-10]
                adr = ''
                for k,v in self.json_rs485['获取PACK告警量'].items():
                    pack_warn = False
                    temp = ''
                    for i in range(v[0], v[0]+v[1], 2):
                        temp += chr(int(msg[i:i + 2], 16))
                    data = int(temp, 16)
                    if k == 'Command':
                        adr = int(temp, 16)
                    elif 'Cell' in k or palnum_label11 in k:    # 'PACK总电压'
                        if data == 0:
                            data = bms_pal_logic_label1
                        elif data == 1:
                            data = bms_pal_logic_label2
                            pack_warn = True
                        elif data == 2:
                            data = bms_parse_label1
                            pack_warn = True
                    elif palnum_label10 in k or palnum_label12 in k:  # 'PACK充电'、'PACK放电'
                        if data == 0:
                            data = bms_pal_logic_label1
                        elif data == 2:
                            data = bms_pal_logic_label3
                            pack_warn = True
                    elif palnum_label2 in k:    # '温度'
                        if data == 0:
                            data = bms_pal_logic_label1
                        if data == 1:
                            data = bms_pal_logic_label4
                            pack_warn = True
                        elif data == 2:
                            data = bms_pal_logic_label5
                            pack_warn = True
                    
                    # 保护状态_1、保护状态_2、指示状态、控制状态、故障状态、告警状态_1、告警状态_2
                    elif k == f'{group_tabel10}_1' or k == f'{group_tabel10}_2' or k == palnum_label14 or k == palnum_label15 \
                    or k == group_tabel8 or k == f'{group_tabel9}_1' or k == f'{group_tabel9}_2':
                        data = bin(int(temp, 16))[2:].zfill(8)
                        warn_list = []
                        for a,b in v[4].items():
                            if data[-(int(a)+1)] == '1':
                                warn_list.append(b)
                        data = '，'.join(warn_list)
                    if k in self.col_labels:
                        self.palTable.setItem(self.col_labels.index(k), int(adr)-1, QTableWidgetItem(str(data)))
                        if pack_warn:
                            self.palTable.item(self.col_labels.index(k), int(adr)-1).setForeground(Qt.red)
                    
            self.add_tableItem('↑', res)

    
    