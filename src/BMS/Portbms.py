#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, datetime, serial, logging, os, functools
import serial.tools.list_ports
from src.i18n.Bms_i18n import *
from src.BMS.tools.CRC16Util import calc_crc
from src.BMS.tools.Common import Common
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QTimer, QWaitCondition, Qt, QThread, pyqtSignal, QMutex, QSettings
from PyQt5.QtGui import QFont
from .BmsLayout import BmsLayout
from .DataPars import pars_data
from .OrderList import order_list
from .QssStyle import *
from src.OrderList import *

wait_time = 2       # 定时发送时间


# 轮询发送P01数据线程
class SendMsg(QThread):
    # 自定义信号对象
    trigger = pyqtSignal(str)
    
    def __init__(self):
        super(SendMsg, self).__init__()
        self._isPause = False
        # QWaitCondition用于多线程的同步，一个线程调用QWaitCondition.wait()阻塞等待，
        # 直到另一个线程调用QWaitCondition.wake()唤醒才继续往下执行.
        self.cond = QWaitCondition()
        self.mutex = QMutex()   # 互斥锁
    
    # 线程休眠
    def pause(self):
        self._isPause = True

    # 线程启动
    def resume(self):
        self._isPause = False
        # self.cond.wakeAll()
        self.cond.wakeOne() # 唤醒该线程

    def run(self):
        global wait_time
        # 重写线程执行的run函数，触发自定义信号
        while True:
            self.mutex.lock()   # 加锁只能一个线程使用
            if self._isPause:
                self.cond.wait(self.mutex)
            time.sleep(wait_time)
            self.trigger.emit(str(order_list['P01']))
            self.mutex.unlock() # 解锁给接下来的线程使用


# 接收数据线程
class ResMsg(QThread):
    
    trigger = pyqtSignal()

    def __init__(self):
        super(ResMsg, self).__init__()
        self._isPause = False
        self.cond = QWaitCondition()
        self.mutex = QMutex()
    
    def pause(self):
        self._isPause = True

    def resume(self):
        self._isPause = False
        self.cond.wakeOne()

    def run(self):
        global wait_time
        while True:
            self.mutex.lock()
            if self._isPause:
                self.cond.wait(self.mutex)
            time.sleep(1)
            self.trigger.emit()
            self.mutex.unlock()


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
        self.SendMsg = SendMsg()
        self.ResMsg = ResMsg()
        # self.bms_logic_i18n()

        # 创建日志文件
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        self.log_name = f'log/{now}.txt'
        if os.path.exists('log') == False:
            os.mkdir('log')

        with open(self.log_name, 'w', encoding='utf-8'): pass
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(lineno)d %(message)s')

        # 进度条状态
        self.respondStatusNum = 0
        self.respondStatus = False
        
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
        
        # 是否开启实时监控
        self.send_P01_on = None
        
        # 实时监控的开启状态
        self.P01_status = False
        
        # 开关充电按钮状态
        self.charge_mos_status = 0
        
        # 开关放电按钮状态
        self.discharge_mos_status = 0
        
        # 充放电状态二进制
        self.dis_charge_mos_num = [0, 0, 0, 0]
        
        # 是否开启实时数据
        self.respond_on = None
        
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

    # 用得比较多的错误提示
    def assertStatus(self):
        if self.ser.isOpen() == False:
            QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
            return False
        elif self.his_status:
            QMessageBox.information(self, 'Error', bms_logic_label8, QMessageBox.Ok)
            return False
        return True
    
    # 是否关闭实时监控
    def assert_P01_status(self):
        if self.P01_status:
            if QMessageBox.information(self, 'tip', \
                bms_logic_label9, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.SendMsg.pause()
                self.send_P01_on = False
                self.P01_status = False
                self.getP01_data_btn.setText(com_label8)
                self.getP01_data_btn.setStyleSheet(color_close)
                return True
            else:
                return False
        return True

    # 实时监控 槽函数slots
    def monitor_slotsTrigger(self):
        # 打开串口
        self.open_port_btn.clicked.connect(self.openPort)
        
        # 获取P01数据
        self.getP01_data_btn.clicked.connect(self.get_p01)
        # self.getP01_data_btn.clicked.connect(lambda: self.send_p01(order_list['P01']))

        # 登录
        self.pwd_btn.clicked.connect(self.pwd_btn_func)
        
        # 开关充电
        self.charge_btn.clicked.connect(self.charge_mos_switch)
        
        # 开关放电
        self.disCharge_btn.clicked.connect(self.discharge_mos_switch)
        
        # 开关强制休眠
        self.dormancy_btn.clicked.connect(self.dormancy_switch)

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
        
        self.sys_edit_dic = {}
        sys_edit_obj = [
            self.designCap,
            self.remainCap,
            self.fullCap
        ]
        for i in range(len(sys_edit_obj)):
            sys_edit_obj[i].textEdited.connect(functools.partial(self.setSysParams, sys_edit_obj[i]))

    # 并联监控 槽函数slots
    def pal_monitor_slotsTrigger(self):
        # self.pal_check.clicked.connect(self.pal_check_func)
        self.pal_start.clicked.connect(self.pal_start_func)

    # 并联监控-开始获取信息按钮
    def pal_start_func(self):
        if self.assertStatus() == False: return False
        if self.assert_P01_status() == False: return False
        self.rs485_res_status = True
        self.repeat = False
        # self.pal_check.setEnabled(False)
        self.palTable.setColumnCount(int(self.pack_total.currentText()))
        self.palTable.clearContents()
        
        self.pal_start_time = QTimer()
        self.pal_start_time_setp = 1
        self.pal_start_time.timeout.connect(self.pal_start_func_timer)
        self.pal_start_time.start(2000)
    
    # 并联监控-开始获取信息按钮-计时器
    def pal_start_func_timer(self):
        num = f'{self.pal_start_time_setp:02d}'
        adr = ''
        for i in num:
            adr += hex(ord(i))[2:]
        if self.pal_start_time_setp <= int(self.pack_total.currentText()):
            if self.repeat == False:
                txt = f'7E 32 35 {adr} 34 36 34 32 45 30 30 32 {adr}'
                self.repeat = True
            else:
                txt = f'7E 32 35 {adr} 34 36 34 34 45 30 30 32 {adr}'
                self.repeat = False
                self.pal_start_time_setp += 1
            self.send_msg(f'{txt}{Common.rs485_chksum(txt)}0D')
        else:
            self.pal_start_time.stop()
            self.rs485_res_status = False
            # self.pal_check.setEnabled(True)

    # 并联监控-确认地址按钮
    def pal_check_func(self):
        self.rs485_res_status = True
        self.pal_start.setEnabled(False)
        self.palTable.setColumnCount(int(self.pack_total.currentText()))
        self.palTable.clearContents()
        
        self.pal_check_time = QTimer()
        self.pal_check_time_setp = 1
        self.pal_check_time.timeout.connect(self.pal_check_func_timer)
        self.pal_check_time.start(2000)

    # 并联监控-确认地址按钮-计时器
    def pal_check_func_timer(self):
        num = f'{self.pal_check_time_setp:02d}'
        adr = ''
        for i in num:
            adr += hex(ord(i))[2:]
        if self.pal_check_time_setp <= int(self.pack_total.currentText()):
            txt = f'7E 32 35 {adr} 34 36 39 30 30 30 30 30'
            self.send_msg(f'{txt}{Common.rs485_chksum(txt)}0D')
            self.pal_check_time_setp += 1
        else:
            self.pal_check_time.stop()
            self.rs485_res_status = False
            self.pal_start.setEnabled(True)

    # 开关充电
    def charge_mos_switch(self):
        if self.charge_btn.text() == switch_label4:
            self.charge_mos_status = 1
        else:
            self.charge_mos_status = 0
            
        self.dis_charge_mos_num[-1] = self.charge_mos_status
        num = hex(int(''.join(str(i) for i in self.dis_charge_mos_num), 2))[2:].rjust(4, '0')
        msg = f'01 06 3000 {num}'
        self.send_msg(msg + calc_crc(msg))

    # 开关放电
    def discharge_mos_switch(self):
        if self.disCharge_btn.text() == switch_label4:
            self.discharge_mos_status = 1
        else:
            self.discharge_mos_status = 0

        self.dis_charge_mos_num[-2] = self.discharge_mos_status
        num = hex(int(''.join(str(i) for i in self.dis_charge_mos_num), 2))[2:].rjust(4, '0')
        msg = f'01 06 3000 {num}'
        self.send_msg(msg + calc_crc(msg))

    # 开关强制休眠
    def dormancy_switch(self):
        if self.dormancy_btn.text() == switch_label4:
            if self.assert_P01_status() == False: return False
            # 强制休眠定时器
            self.sleep_step = 6
            self.sleepTimer = QTimer()
            self.sleepTimer.timeout.connect(self.sleep_timer_func)
            self.sleepTimer.start(1000)
            self.charge_btn.setEnabled(False)
            self.disCharge_btn.setEnabled(False)
        else:
            msg = '01 06 300c 0000'
            self.dormancy_btn.setText(switch_label4)
            self.dormancy_btn.setStyleSheet(color_close)
            self.send_msg(msg + calc_crc(msg))

    # 强制休眠计时器，倒数至0则发送休眠指令
    def sleep_timer_func(self):
        self.sleep_step -= 1
        self.dormancy_btn.setEnabled(False)
        self.dormancy_btn.setText(f'wating {self.sleep_step}')
        if self.sleep_step == 0:
            msg = '01 06 300c 0001'
            self.dormancy_btn.setText(bms_logic_label6)
            self.dormancy_btn.setStyleSheet(color_open)
            self.sleepTimer.stop()
            self.dormancy_btn.setEnabled(True)
            self.send_msg(msg + calc_crc(msg))

    # 获取修改过的'系统设置-电量'参数
    def setSysParams(self, key):
        text = key.text()
        if text != '':
            try:
                num = int(float(text)*100)
            except ValueError:
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
            except ValueError:
                key.setText('')
                return QMessageBox.critical(self, 'Error', bms_logic_label12, QMessageBox.Ok)

    # 读取系统设置-电量
    def readCap_func(self):
        if self.assertStatus() == False: return False
        if self.assert_P01_status() == False: return False
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
            self.send_msg(order_list['4000'])
            self.readCap_timer_step += 1
        else:
            self.send_msg(order_list['318'])
            self.readCap_timer.stop()
    
    # 设置系统设置-电量
    def writeCap_func(self):
        if self.assertStatus() == False: return False
        if self.assert_P01_status() == False: return False
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

    # 显示进度条
    def pro_timer_func(self):
        if self.respondStatus:
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
            self.writeParam.setEnabled(True)
            self.resetTab3.setEnabled(True)
            QMessageBox.information(self, 'tips', bms_logic_label18, QMessageBox.Ok)
        else:
            QMessageBox.information(self, 'Error', bms_logic_label19, QMessageBox.Ok)

    # 打开/关闭串口
    def openPort(self):
        if self.open_port_btn.text() == com_label6:
            self.port = self.port_combobox.currentText()
            self.baud = self.baud_combobox.currentText()
            self.ser.port = self.port
            self.ser.baudrate = int(self.baud)
            try:
                self.ser.open()
            except serial.SerialException:
                QMessageBox.information(self, 'Error', bms_logic_label20, QMessageBox.Ok)
            self.open_port_btn.setText(bms_logic_label2)
            self.open_port_btn.setStyleSheet(color_open)
            if  self.respond_on == False:
                self.ResMsg.resume()
            else:
                self.respond_on = True
                self.res_msg()
            self.dormancy_btn.setEnabled(True)
        else:
            self.ResMsg.pause()
            self.ser.close()
            self.open_port_btn.setText(com_label6)
            self.open_port_btn.setStyleSheet(color_close)
            self.respondStatus = False
            self.respond_on = False
            self.dormancy_btn.setEnabled(False)

    # 按钮-开始监控
    def get_p01(self):
        if self.getP01_data_btn.text() == com_label8:
            if self.assertStatus() == False: return False
            self.send_msg('01 03 0014 0002 840f')
            time.sleep(0.5)
            self.P01_status = True
            if self.send_P01_on == False:
                self.SendMsg.resume()
            else:
                self.send_P01_on = True
                self.send_p01()
            self.getP01_data_btn.setText(bms_logic_label4)
            self.getP01_data_btn.setStyleSheet(color_open)
            self.charge_btn.setEnabled(True)
            self.disCharge_btn.setEnabled(True)
            self.low_vol = False
        else:
            self.send_P01_on = False
            self.P01_status = False
            try:
                # 休眠
                self.SendMsg.pause()
            except Exception as e:
                print(e)
            self.getP01_data_btn.setText(com_label8)
            self.getP01_data_btn.setStyleSheet(color_close)
            self.charge_btn.setEnabled(False)
            self.disCharge_btn.setEnabled(False)

    # 开始监控
    def send_p01(self):
        # 十六进制转字节发送
        # hex_data = bytes.fromhex(data)
        # self.ser.write(hex_data)
        if self.send_P01_on == True:
            self.SendMsg.trigger.connect(self.send_P01_thread)
            self.SendMsg.start()

    # 激活实时数据线程
    def res_msg(self):
        if self.respond_on == True:
            self.ResMsg.trigger.connect(self.respond_thread)
            self.ResMsg.start()

    # 实时监控线程
    def send_P01_thread(self, data):
        global wait_time
        wait_time = int(self.space_combobox.currentText())
        try:
            self.send_msg(data)
        except serial.PortNotOpenError:
            self.SendMsg.pause()
            return 0

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
                if key == '单体过充告警(V)' or key == '单体过充保护(V)' or key == '单体过充保护恢复(V)' \
                or key == '单体过放告警(V)' or key == '单体过放保护(V)' or key == '单体过放保护恢复(V)':
                    txt = int(float(self.tab3_form_dic[key].text()) * 1000)
                    if txt > 4000:
                        self.tab3_form_dic[key].setText('')
                        return QMessageBox.critical(self, 'Error', bms_logic_label21, QMessageBox.Ok)      
                elif key == '总体过充告警(V)' or key == '总体过充保护(V)' or key == '总体过充保护恢复(V)' \
                or key == '总体过放告警(V)' or key == '总体过放保护(V)' or key == '总体过放保护恢复(V)':
                    txt = int(float(self.tab3_form_dic[key].text()) * 1000)
                    if txt > 60000:
                        self.tab3_form_dic[key].setText('')
                        return QMessageBox.critical(self, 'Error', bms_logic_label22, QMessageBox.Ok)
                else:
                    txt = int(self.tab3_form_dic[key].text())
                keyTxt = f"0106{self.json_modbus['01032007005bbe30'][key][3]}{txt:04x}"
            except Exception as e:
                print(e)
                return QMessageBox.critical(self, 'Error', bms_logic_label11, QMessageBox.Ok)
            self.tab3_dic[key] = keyTxt+calc_crc(keyTxt)

    # 写入参数
    def writeTab3Params(self):
        if self.assertStatus() == False: return False
        if self.assert_P01_status() == False: return False
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
        if self.assert_P01_status() == False: return False
        self.tab3_dic.clear()
        self.send_msg(order_list['P03'])
        self.writeParam.setEnabled(True)
        self.deriveParam.setEnabled(True)

    # 保存参数设置为txt
    def deriveTab3Params(self):
        # print(os.getcwd())
        file_name =os.path.join(os.getcwd, f'{tab_tabel3}.txt')
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
        if self.assert_P01_status() == False: return False
        self.send_msg('01 06 400b 0001 2c08')
    
    # 擦除历史数据
    def clear_his_msg(self):
        if self.ser.isOpen() == False:
            return QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
        if self.assert_P01_status() == False: return False
        self.send_msg('0106300b000136c8')
        self.clearRow_btn(self.hisTable)
        
    # 获取历史数据
    def his_show(self):
        if self.ser.isOpen() == False:
            return QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
        if self.assert_P01_status() == False: return False
        self.clearRow_btn(self.hisTable)
        
        self.clear_his_status = False
        
        self.hisTime = QTimer()
        self.hisTime.timeout.connect(self.his_time_func)
        self.hisTime.start(1000)
        self.hisNum = 1
        self.his_status = True
        self.getP01_data_btn.setText(com_label8)
        self.hisShow.setEnabled(False)
    
    # 获取最近历史数据计时器
    def his_time_func(self):
        if self.clear_his_status == False:
            self.send_msg('0103f0000001b70a')
        try:
            if self.num_max == 0:
                QMessageBox.information(self, 'tip', bms_logic_label27, QMessageBox.Ok)
                self.hisTime.stop()
        except Exception:
            return
        self.clear_his_status = True
        
        if self.num_max > 100:
            self.num_max = 100
        if self.hisNum <= self.num_max:
            num = f'0103f{self.hisNum:03x}0036'
            self.send_msg(f'{num}{calc_crc(num)}')
            self.hisNum += 1
        else:
            self.hisTime.stop()
            self.his_status = False
            self.hisShow.setEnabled(True)

    # 发送数据
    def send_msg(self, data):
        hex_data = bytes.fromhex(data)
        try:
            self.ser.write(hex_data)
        except serial.serialutil.PortNotOpenError as e:
            self.ser.close()
            return False
        self.add_tableItem('↓', bytes.hex(hex_data))    # 在表格中输出

    # 接收数据(打开串口就会启用该线程进行数据接收并解析)
    def respond_thread(self):
        try:
            res = self.ser.read_all()
            res = res.hex()
        except Exception as e:
            logging.error(e)
            return False
        if res != '':
            self.respondStatusNum = 0
            self.respondStatus = True
            # 接收协议是否为 rs485
            if self.rs485_res_status == False:
                crc_error = False
                # 实时监控
                if res[:6] == '0103bc' and len(res) == 386:
                    p01 = pars_data(res, order_list['P01'])
                    if len(p01) == 2:
                        crc_error = True
                    else:
                        # BMS工作状态1（系统状态）
                        if sys_label1 in p01['BMS工作状态1']:
                            self.charg_status.setStyleSheet('color:green')
                        else:
                            self.charg_status.setStyleSheet('color:black')
                            
                        if sys_label2 in p01['BMS工作状态1']:
                            self.disCharg_status.setStyleSheet('color:green')
                        else:
                            self.disCharg_status.setStyleSheet('color:black')
                            
                        if sys_label3 in p01['BMS工作状态1']:
                            self.charge_btn.setText(bms_logic_label6)
                            self.charge_btn.setStyleSheet(color_open)
                            self.charge_mos_status = 1
                            self.chargMos_status.setStyleSheet('color:green')
                        else:
                            self.charge_btn.setText(switch_label4)
                            self.charge_btn.setStyleSheet(color_close)
                            self.charge_mos_status = 0
                            self.chargMos_status.setStyleSheet('color:black')
                        self.dis_charge_mos_num[-1] = self.charge_mos_status
                        
                        if sys_label4 in p01['BMS工作状态1']:
                            self.disCharge_btn.setText(bms_logic_label6)
                            self.disCharge_btn.setStyleSheet(color_open)
                            self.discharge_mos_status = 1
                            self.disChargMos_status.setStyleSheet('color:green')
                        else:
                            self.disCharge_btn.setText(switch_label4)
                            self.disCharge_btn.setStyleSheet(color_close)
                            self.discharge_mos_status = 0
                            self.disChargMos_status.setStyleSheet('color:black')
                        self.dis_charge_mos_num[-2] = self.discharge_mos_status
                        
                        if sys_label5 in p01['BMS工作状态1']:
                            self.batCharg_status.setStyleSheet('color:green')
                        else:
                            self.batCharg_status.setStyleSheet('color:black')
                            
                        if sys_label6 in p01['BMS工作状态1']:
                            self.full_status.setStyleSheet('color:green')
                        else:
                            self.full_status.setStyleSheet('color:black')

                        if len(p01['故障位']) > 0:
                            for _ in p01['故障位']:
                                txt = '\n'.join(p01['故障位'])
                                self.warn_status_txt.setText(txt)

                        warn_txt = '\n'.join(p01['警告位1']) + '\n' + '\n'.join(p01['警告位2'])
                        self.error_status_txt.setText(warn_txt)
                        protect_txt = '\n'.join(p01['保护位1']) + '\n' + '\n'.join(p01['保护位2'])
                        self.protect_status_txt.setText(protect_txt)

                        # 数据显示
                        display_data = [
                            self.bat_wd, 
                            self.cell_temp_8, 
                            self.cell_temp_16, 
                            self.tem_other, 
                            self.cell_vol_8, 
                            self.cell_vol_16,
                            self.vol_other
                        ]
                        for index in range(len(display_data)):
                            for k,v in display_data[index].items():
                                display_data[index][k].setText(p01[k])
                                
                        if ('cell低压' in protect_txt or 'pack低压' in protect_txt) and self.low_vol == False:
                            self.low_vol = True
                            self.SendMsg.pause()
                            self.send_P01_on = False
                            self.P01_status = False
                            self.getP01_data_btn.setText(com_label8)
                            self.getP01_data_btn.setStyleSheet(color_close)
                            QMessageBox.information(self, 'tips', bms_logic_label28, QMessageBox.Ok)
                # 参数设置
                elif res[:6] == '0103b6' and len(res) == 374:
                    self.p03 = pars_data(res, order_list['P03'])
                    if len(self.p03) == 2:
                        crc_error = True
                    else:
                        for k,v in self.p03.items():
                            try:
                                self.tab3_form_dic[k].setText(v)
                            except KeyError:
                                continue
                # 历史数据
                elif res[:6] == '01036c' and len(res) == 226:
                    p06 = pars_data(res, order_list['P06'])
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
                    v1 = int(res[6:8], 16)
                    v2 = int(res[8:10], 16)
                    v3 = int(res[10:12], 16)
                    v4 = int(res[12:14], 16)
                    self.version.setText(f'Version：{v1}.{v2}.{v3}.{v4}')
                # 读取系统设置-电量数据
                elif res[:6] == '010306' and len(res) == 22:
                    ele_data = pars_data(res, order_list['318'])
                    self.remainCap.setText(ele_data[f'{battery_label3}(AH)'])
                    self.fullCap.setText(ele_data[f'总容量(AH)'])
                # 读取系统设置-电量数据2
                elif res[:6] == '010302' and len(res) == 14 and self.sys_status == True:
                    ele_data = pars_data(res, order_list['4000'])
                    self.designCap.setText(ele_data[f'设计容量(AH)'])
                    self.sys_status = False
                # 历史数据总数 
                elif res[:6] == '010302' and len(res) == 14:
                    self.num_max = int(res[6:10], 16)
                    
                if crc_error == False:
                    self.add_tableItem('↑', res)
                else:
                    self.add_tableItem(bms_logic_label29, res)
            else:
                # 接收 rs485 报文并处理
                if res[:2] == '7e' and len(res) == 40:  # 确认 pack 地址
                    temp = res[6:10]
                    hex2asc = ''
                    for i in range(0, len(temp), 2):
                        # 十六进制转换成ascii字符
                        hex2asc += chr(int(temp[i:i + 2], 16))
                    self.palTable.setItem(0, int(hex2asc)-1, QTableWidgetItem('online'))
                elif res[:2] == '7e' and len(res) == 312:  # 获取 PACK 模拟量响应信息
                    msg = res[30:-10]  # 去掉前缀报文和校验码
                    adr = ''
                    for k,v in self.json_rs485['获取 PACK 模拟量响应信息'].items():
                        temp = ''
                        for i in range(v[0], v[0]+v[1], 2):
                            temp += chr(int(msg[i:i + 2], 16))
                        if k == 'Command':
                            adr = int(temp, 16)
                        elif '温度' in k or '电流' in k:
                            data = f'{Common.format_num(Common.signBit_func(temp) / abs(v[2]))} {v[3]}'
                        else:
                            data = f'{int(temp, 16)} {v[3]}'
                        if k in self.col_labels:
                            self.palTable.setItem(self.col_labels.index(k), int(adr)-1, QTableWidgetItem(str(data)))
                elif res[:2] == '7e' and len(res) == 200:  # 获取 PACK 告警量
                    msg = res[30:-10]
                    adr = ''
                    for k,v in self.json_rs485['获取 PACK 告警量'].items():
                        pack_warn = False
                        temp = ''
                        for i in range(v[0], v[0]+v[1], 2):
                            temp += chr(int(msg[i:i + 2], 16))
                        data = int(temp, 16)
                        if k == 'Command':
                            adr = int(temp, 16)
                        elif 'cell' in k or 'PACK总电压' in k:
                            if data == 0:
                                data = '正常'
                            elif data == 1:
                                data = '欠压'
                                pack_warn = True
                            elif data == 2:
                                data = '超压'
                                pack_warn = True
                        elif 'PACK充电' in k or 'PACK放电' in k:
                            if data == 0:
                                data = '正常'
                            elif data == 2:
                                data = '电流过高'
                                pack_warn = True
                        elif '温度' in k:
                            if data == 0:
                                data = '正常'
                            if data == 1:
                                data = '温度过低'
                                pack_warn = True
                            elif data == 2:
                                data = '温度过高'
                                pack_warn = True
                        elif k == '保护状态1' or k == '保护状态2' or k == '指示状态' or k == '控制状态' \
                         or k == '故障状态' or k == '告警状态1' or k == '告警状态2':
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
        else:
            self.respondStatusNum += 1
            if self.respondStatusNum > 5:
                self.respondStatus = False

    
    