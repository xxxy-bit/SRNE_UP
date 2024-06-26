#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, datetime, serial, logging, os, functools, subprocess
import serial.tools.list_ports
from src.i18n.Bms_i18n import *
from src.BMS.tools.CRC16Util import calc_crc
from utils.Common import Common
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, QTime, QDateTime, QTimer, Qt, QThread, pyqtSignal
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
                self.ser.timeout = 0.7
                self.res = self.ser.read(1024).hex()
                # print(self.res)
                print(self.respondStatusNum)
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
                if self.respondStatusNum > 10:
                    self.respondStatus = False
    
    def close(self):
        self.is_running = False
        self.respondStatus = False
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
        
        # 是否正在开启实时监控
        self.moni_switch = False
        
        # 是否正在获取单台PACK
        self.pal_single_status = False
        
        # 是否正在获取多台PACK
        self.pal_many_status = False
        
        # 登录状态
        self.login = False
        
        # 充放电状态二进制
        self.dis_charge_mos_num = [0, 0, 0, 0]
        
        # 是否开启实时数据
        self.res_qtimer_switch = None
        
        # tab3写入参数指令集
        self.tab3_dic = {}
        
        # 是否在获取历史数据
        self.his_status = False
        
        # 导出历史数据的目录名称
        self.export_history_dir = 'export_history'
        if os.path.exists(self.export_history_dir) == False:
            os.mkdir(self.export_history_dir)
        
        # 获取蜂鸣器状态标志位
        self.beep_tag = False
        
        # 擦除历史数据标志位
        self.clear_his_status = False
        
        # 读取通信协议标志位
        self.Pro_status = False
        
        # 02 电池设置标志位
        self.sys_status_1 = False
        
        # 04 返回相同字节数的标志位
        self.ver = False
        self.sys_status_2 = False
        
        # 启用rs485协议解析
        self.rs485_res_status = False
        
        # 接收响应值线程
        self.res_thread = ResThread(self.ser)
        self.res_thread.finished.connect(self.bms_qtimer_res_func)

    # 用得比较多的错误提示
    def assertStatus(self):
        if self.ser.isOpen() == False:
            QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
            return False
        elif self.his_status:
            QMessageBox.information(self, 'Error', bms_logic_label30, QMessageBox.Ok)
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
        
        # 开关蜂鸣器
        self.buzzer_sw.checkedChanged.connect(self.buzzer_switch)
        
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
        self.export_history.clicked.connect(self.export_history_func)
        self.clearShow.clicked.connect(self.clear_his_msg)
        self.clearScreen.clicked.connect(self.clear_Screen_msg)

    # 参数设置 槽函数slots
    def setParams_slotsTrigger(self):
        self.getTab3Res.clicked.connect(self.getTab3Res_func)
        self.clsTab3Res.clicked.connect(self.clearTab3)
        self.writeParam.clicked.connect(self.writeTab3Params)
        self.resetTab3.clicked.connect(self.reset_default)
        self.deriveParam.clicked.connect(self.deriveTab3Params)
        
        for k,v in self.tab3_form_dic.items():
            self.tab3_form_dic[k].valueChanged.connect(functools.partial(self.setTab3Params, k))

    # 系统设置 槽函数slots
    def sysset_slotsTrigger(self):
        self.readCap.clicked.connect(self.readCap_func)
        self.writeCap.clicked.connect(self.writeCap_func)
        
        self.readTime.clicked.connect(self.readTime_func)
        self.sys_time = False   # 系统时间标志位
        self.sync_btn.clicked.connect(self.sync_btn_func)   # 同步时间
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
        self.Pro_read.clicked.connect(self.Pro_read_func)
        self.Pro_write.clicked.connect(self.Pro_write_func)
        self.fu_btn.clicked.connect(self.fu_btn_func)

    # 并联监控 槽函数slots
    def pal_monitor_slotsTrigger(self):
        # self.pal_single_start.clicked.connect(self.pal_start_func)
        self.pal_single_start.clicked.connect(self.pal_single_func)
        self.pal_loop_status.clicked.connect(self.pal_loop_func)

    # 系统设置-固件升级
    def fu_btn_func(self):
        
        # 串口自动关闭
        try:
            if self.ser.isOpen():
                self.openPort()
        except Exception:
            pass
        
        # 指定 EXE 文件的路径
        exe_path = os.path.join(os.getcwd(), 'settings', 'sriap-1.33.exe')
        
        # 使用 Popen() 函数打开 EXE 文件
        subprocess.Popen([exe_path])

    # 系统设置-读取协议
    def Pro_read_func(self):
        self.send_msg(bms_sys_protocol + calc_crc(bms_sys_protocol))
        self.Pro_status = True
    
    # 系统设置-写入协议
    def Pro_write_func(self):
        index_can = self.Pro_can_combox.currentIndex()
        index_485 = self.Pro_485_combox.currentIndex()
        msg = f'0106001b{index_can:02x}{index_485:02x}'
        self.send_msg(msg + calc_crc(msg))
    
    # 历史数据-导出历史记录按钮
    def export_history_func(self):
        try:
            with open(self.export_history_name, 'w', encoding='utf-8-sig') as f:
                for k, v in self.cloumn_name.items():
                    f.write(k + ' ,')
                f.write('\n' + self.export_history_csv)
        except PermissionError as e:
            return QMessageBox.critical(self, 'Error', bms_logic_label31, QMessageBox.Ok) 
        except Exception as e:
            return QMessageBox.critical(self, 'Error', f'{e}\n{bms_logic_label32}', QMessageBox.Ok) 

        # 是否需要主动打开目录
        open_file =os.path.join(os.getcwd(), self.export_history_dir, f'{self.export_history_now}.csv')
        if QMessageBox.question(self, 'Tips', f'{bms_logic_label33}{open_file}\n{bms_logic_label34}', 
                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            os.startfile(open_file)

    # 并联监控-获取单个设备数据
    def pal_single_func(self):
        if self.pal_single_start.text() == palset_label2:
            if self.assertStatus() == False: return False
            self.pal_single_start.setText(palset_label3)
            
            # 单PACK获取中
            self.pal_single_status = True
            
            # 暂停单机监控与并联轮询
            try:
                if self.pal_many_time.isActive():
                    self.pal_loop_status.setChecked(False)
                    self.pal_loop_func()
            except Exception:
                print('except pal_single_func')
            self.stop_moni()
            
            # 启用rs485协议
            self.rs485_res_status = True

            # 获取电压与温度个数
            self.get_parallel_vol_tmp = False
            # 单数据，42/44轮询发送
            self.pal_single_repeat = False
            
            self.pal_single_time = QTimer()
            self.pal_single_time_setp = 0
            self.pal_single_time.timeout.connect(self.pal_single_func_timer)
            self.pal_single_time.start(2000)
        else:
            self.pal_single_status = False
            self.rs485_res_status = False
            self.pal_single_time.stop()
            self.pal_single_start.setText(palset_label2)
            self.start_moni()

    # 并联监控-获取单个设备数据-计时器
    def pal_single_func_timer(self):
        # 先获取电压和温度个数
        if self.get_parallel_vol_tmp == False:
            self.pal_single_time_setp = 0
            txt = f'7E 32 35 {3031} 34 36 34 32 45 30 30 32 {3031}'
            self.send_msg(f'{txt}{Common.rs485_chksum(txt)}0D')
            return 0
        # 然后根据个数创建表格
        elif self.pal_single_time_setp == 0 and self.get_parallel_vol_tmp:
            # 创建表格列表 行字段
            self.pal_get_vol_tmp_func()
            
            # 创建完成开始读数据
            self.pal_single_time_setp = 1
            return 0
        
        num = f'{int(self.pack_total.currentText()):02d}'
        adr = ''
        for i in num:
            adr += hex(ord(i))[2:]
        
        # 42 44 轮询发送
        if self.pal_single_repeat == False:
            self.pal_single_repeat = True
            txt = f'7E 32 35 {adr} 34 36 34 32 45 30 30 32 {adr}'
        else:
            self.pal_single_repeat = False
            txt = f'7E 32 35 {adr} 34 36 34 34 45 30 30 32 {adr}'
        self.send_msg(f'{txt}{Common.rs485_chksum(txt)}0D')

    # 并联监控-获取电压与温度个数
    def pal_get_vol_tmp_func(self):
        
        # 添加 模拟量 与 告警量 进表格
        self.create_col_labels = {}
        self.create_col_labels.update(self.parallel_pack_simulate)
        self.create_col_labels.update(self.parallel_pack_tmp)
        del self.create_col_labels["Command"]
        del self.create_col_labels["电池单体个数"]
        del self.create_col_labels["监测温度个数"]
        del self.create_col_labels["用户自定义个数"]
        del self.create_col_labels["Command2"]
        del self.create_col_labels["电池单体告警个数"]
        del self.create_col_labels["监测温度告警个数"]
        
        # 把key作为行字段添加到表格
        self.col_labels = []
        for key, value in self.create_col_labels.items():
            self.col_labels.append(key)
            
        self.palTable.setRowCount(len(self.col_labels))
        self.palTable.setVerticalHeaderLabels(self.col_labels)

    # 并联监控-并联轮询
    def pal_loop_func(self):
        if self.pal_loop_status.isChecked():
            if self.assertStatus() == False:
                self.pal_loop_status.setChecked(False)
                return 0
            
            # 开启并联轮询
            self.pal_many_status = True
            
            # 暂停单机监控与单PACK监控
            try:
                if self.pal_single_time.isActive():
                    self.pal_single_func()
            except Exception:
                print('except pal_loop_func')
            self.stop_moni()
            
            # 总电流累加
            self.pal_count_elc = 0
            
            self.rs485_res_status = True
            self.pal_many_repeat = False
            self.palTable.clearContents()
            
            # 是否已获取到电压与温度个数
            self.get_parallel_vol_tmp = False

            self.pal_many_time = QTimer()
            self.pal_many_time_step = 0
            self.pal_many_time.timeout.connect(self.pal_many_func_timer)
            self.pal_many_time.start(2000)
            
        else:
            self.pal_many_status = False
            self.rs485_res_status = False
            self.pal_many_time.stop()
            self.start_moni()

    # 并联监控-并联轮询-计时器
    def pal_many_func_timer(self):
        
        # 先获取电压和温度个数
        if self.get_parallel_vol_tmp == False:
            self.pal_start_time_setp = 0
            txt = f'7E 32 35 {3031} 34 36 34 32 45 30 30 32 {3031}'
            self.send_msg(f'{txt}{Common.rs485_chksum(txt)}0D')
            return 0
        # 然后根据个数创建表格
        elif self.pal_start_time_setp == 0 and self.get_parallel_vol_tmp:
            # 创建表格列表 行字段
            self.pal_get_vol_tmp_func()
            
            # 创建完成开始读数据
            self.pal_start_time_setp = 1
            return 0
        
        num = f'{self.pal_start_time_setp:02d}'
        adr = ''
        for i in num:
            adr += hex(ord(i))[2:]
        print(adr)
        
        # 42 44 轮询发送
        if self.pal_start_time_setp <= 16:
            if self.pal_many_repeat == False:
                self.pal_many_repeat = True
                txt = f'7E 32 35 {adr} 34 36 34 32 45 30 30 32 {adr}'
            else:
                self.pal_many_repeat = False
                txt = f'7E 32 35 {adr} 34 36 34 34 45 30 30 32 {adr}'
                self.pal_start_time_setp += 1
            self.send_msg(f'{txt}{Common.rs485_chksum(txt)}0D')
            
        elif self.pal_start_time_setp == 17:
            self.send_msg(f'7e 32 35 30 31 34 36 36 31 45 30 30 32 30 31 46 44 32 46 0d')
            self.pal_start_time_setp += 1
        
        elif self.pal_start_time_setp > 17:
            self.pal_start_time_setp = 1

    # 开关蜂鸣器
    def buzzer_switch(self):
        if self.buzzer_sw.isChecked():
            self.send_msg(bms_buzzer_on + calc_crc(bms_buzzer_on))
        else:
            self.send_msg(bms_buzzer_off + calc_crc(bms_buzzer_off))

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

    # 实时监控-测试模式
    def testmode_btn_func(self):
        if self.testmode_btn.text() == switch_label6:
            self.testmode_btn.setText(switch_label7)
            self.charge_sw.setEnabled(True)
            self.disCharge_sw.setEnabled(True)
            
        else:
            self.testmode_btn.setText(switch_label6)
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
                send_num = '01064000'   # 设计容量
            elif key == self.remainCap:
                send_num = '01064005'   # 剩余容量
            else:
                send_num = '01064004'   # 总容量
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
        self.sys_status_1 = True
        self.sys_status_2 = True
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
           
    # 系统设置-同步时间
    def sync_btn_func(self):
        sync_time = self.nowTime.text()
        year = sync_time[0:4]
        month = sync_time[5:7]
        day = sync_time[8:10]
        hour = sync_time[11:13]
        minute = sync_time[14:16]
        second = sync_time[17:]
        
        thisTime = QDateTime.currentDateTime()
        thisTime.setDate(QDate(int(year), int(month), int(day)))
        thisTime.setTime(QTime(int(hour), int(minute), int(second)))
        self.now_time.setDateTime(thisTime)
        
    # 系统设置-读取系统时间
    def readTime_func(self):
        if self.assertStatus() == False: return False
        self.sys_time = True
        self.send_msg(bms_sys_time + calc_crc(bms_sys_time))
    
    # 系统设置-写入电量
    def writeCap_func(self):
        if self.assertStatus() == False: return False
        self.stop_moni()
        if len(self.sys_edit_dic) != 0:
            ls = [v for k,v in self.sys_edit_dic.items()]
            self.ls_trv = list(zip(range(len(self.sys_edit_dic)), ls))
            print(self.ls_trv)
            
            self.writeCap_timer = QTimer()
            self.writeCap_timer_step = 0
            self.writeCap_timer.timeout.connect(self.writeCap_func_timer)
            self.writeCap_timer.start(1000)
            self.writeCap.setEnabled(False)
        else:
            return QMessageBox.critical(self, 'Error', bms_logic_label13, QMessageBox.Ok)
        
    # 系统设置-写入电量-计时器
    def writeCap_func_timer(self):
        if self.writeCap_timer_step < len(self.sys_edit_dic):
            self.send_msg(self.ls_trv[self.writeCap_timer_step][1])
            self.writeCap_timer_step += 1
        else:
            self.writeCap_timer.stop()
            self.writeCap.setEnabled(True)
            self.writeCap.setText(systime_label3)
            self.start_moni()
            QMessageBox.information(self, 'tips', bms_logic_label35, QMessageBox.Ok)
    
    # 系统设置-写入系统时间
    def writeTime_func(self):
        if self.assertStatus() == False: return False
        
        year = hex(self.now_time.dateTime().date().year() - 2000)[2:].rjust(2,'0')
        month = hex(self.now_time.dateTime().date().month())[2:].rjust(2,'0')
        day = hex(self.now_time.dateTime().date().day())[2:].rjust(2,'0')
        hour = hex(self.now_time.dateTime().time().hour())[2:].rjust(2,'0')
        minute = hex(self.now_time.dateTime().time().minute())[2:].rjust(2,'0')
        second = hex(self.now_time.dateTime().time().second())[2:].rjust(2,'0')
        msg = f'01102004000306{year}{month}{day}{hour}{minute}{second}'
        self.send_msg(msg + calc_crc(msg))
        QMessageBox.information(self, 'tips', bms_logic_label35, QMessageBox.Ok)
        
    # 发送校准值
    def adds_btn_func(self):
        if self.assertStatus() == False: return False
        self.stop_moni()
        txt = self.adds_combox.currentText()
        hex_addr = self.datacalibration_adds_list[txt]
        if txt == bms_history_label3 or txt == bms_history_label2:
            hex_num = format(int(float(self.adds_txt.text()) * 100), '04x')
            # print(hex_num)
        else:
            get_poi = int(self.adds_txt.text().split('.')[1])
            if get_poi > 0:
                return QMessageBox.information(self, 'tips', bms_logic_label36, QMessageBox.Ok)
        
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
            return QMessageBox.information(self, 'tips', datacal_label3, QMessageBox.Ok)

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
            
            self.login = True
            
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
                return QMessageBox.information(self, 'Error', bms_logic_label37, QMessageBox.Ok)
            self.open_port_btn.setStyleSheet(open_Button)
            self.open_port_btn.setText(bms_logic_label2)
            
            # 开启数据接收线程
            self.res_thread.is_running = True
            self.res_thread.start()
            
        else:
            self.res_thread.close()
            self.open_port_btn.setStyleSheet(close_Button)
            self.open_port_btn.setText(com_label6)
            self.res_qtimer_switch = False

    # 刷新串口
    def refresh_port(self):
        self.port_combobox.clear()
        self.port_combobox.addItems(Common.load_serial_list())
    
    # 按钮-开始监控
    def get_p01(self):
        self.stop_monitor = 0   # 用于监测低压次数，如果达到600则自动停止监控
        
        if self.getP01_data_btn.text() == com_label8:
            if self.assertStatus() == False: return False
            
            # 判断是否已经开启并联轮询
            if self.pal_single_status or self.pal_many_status:
                return QMessageBox.information(self, 'Error', bms_logic_label38, QMessageBox.Ok)
            
            # 开启单机监控
            self.moni_switch = True
            
            self.getP01_data_btn.setText(bms_logic_label4)
            self.getP01_data_btn.setStyleSheet(open_Button)
            self.low_vol = False
            
            # 版本标志位
            self.ver = True
            
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
        elif self.bms_qtimer_get_monitor_step == 1:
            self.beep_tag = True
            self.send_msg(bms_beep + calc_crc(bms_beep))
        else:
            self.send_msg(bms_monitor + calc_crc(bms_monitor))
        self.bms_qtimer_get_monitor_step += 1
        
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
                print(self.tab3_form_dic[key].text())
                if key == '单体过充告警(V)' or key == '单体过充保护(V)' or key == '单体过充保护恢复(V)' \
                or key == '单体过放告警(V)' or key == '单体过放保护(V)' or key == '单体过放保护恢复(V)':
                    txt = int(float(self.tab3_form_dic[key].value()) * 1000)
                    print(txt)
                elif key == '总体过充告警(V)' or key == '总体过充保护(V)' or key == '总体过充保护恢复(V)' \
                or key == '总体过放告警(V)' or key == '总体过放保护(V)' or key == '总体过放保护恢复(V)':
                    txt = int(float(self.tab3_form_dic[key].value()) * 1000)
                else:
                    txt = int(float(self.tab3_form_dic[key].value()) * abs(self.json_modbus[bms_setting][key][2]))
                    # TODO
                    if txt < 0:
                        txt = txt + 65536
                        
                print(txt)
                keyTxt = f"0106{self.json_modbus[bms_setting][key][3]}{txt:04x}"
                print(keyTxt)
            except Exception as e:
                print(f"获取修改过的'参数设置'参数：{e}")
                return QMessageBox.critical(self, 'Error', bms_logic_label11, QMessageBox.Ok)
            self.tab3_dic[key] = keyTxt + calc_crc(keyTxt)

    # 参数设置-写入参数
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
            self.getTab3Res_func()

    # 读取 参数设置 数据
    def getTab3Res_func(self):
        if self.assertStatus() == False: return False
        self.tab3_dic.clear()
        self.send_msg(bms_setting + calc_crc(bms_setting))
        self.deriveParam.setEnabled(True)
        # QMessageBox.information(self, 'tips', '读取完成', QMessageBox.Ok)

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
            self.tab3_form_dic[k].blockSignals(True)
            self.tab3_form_dic[k].setValue(0)
            self.tab3_form_dic[k].blockSignals(False)
            
        self.tab3_dic.clear()
    
    # 参数设置-恢复默认值(出厂设置)
    def reset_default(self):
        if self.assertStatus() == False: return False
        self.send_msg(bms_reset + calc_crc(bms_reset))
    
    # 清屏历史数据
    def clear_Screen_msg(self):
        if self.ser.isOpen() == False:
            return QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
        self.clearRow_btn(self.hisTable)
        try:
            self.hisTime.stop()
        except Exception as e:
            print(e)
        self.his_status = False
        self.hisShow.setText(hisdata_label1)
        self.start_moni()
        self.export_history.setEnabled(False)
    
    # 擦除历史数据
    def clear_his_msg(self):
        if self.ser.isOpen() == False:
            return QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
        self.send_msg(bms_clear_history + calc_crc(bms_clear_history))
        self.clearRow_btn(self.hisTable)
        try:
            self.hisTime.stop()
        except Exception as e:
            print(e)
        self.his_status = False
        self.hisShow.setText(hisdata_label1)
        self.start_moni()
        self.export_history.setEnabled(False)
        
    # 获取历史数据
    def his_show(self):
        if self.hisShow.text() == hisdata_label1:   # 获取最近历史数据(1~100)
            if self.ser.isOpen() == False:
                return QMessageBox.information(self, 'Error', bms_logic_label7, QMessageBox.Ok)
            
            # 判断是否已经开启并联轮询
            if self.pal_single_status or self.pal_many_status:
                return QMessageBox.information(self, 'Error', bms_logic_label38, QMessageBox.Ok)
            
            self.stop_moni()
            self.clearRow_btn(self.hisTable)
            
            self.clear_his_status = False
            
            # 创建历史记录 .csv:
            self.export_history_now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            self.export_history_name = os.path.join(self.export_history_dir, f'{self.export_history_now}.csv')
                
            # 存储历史数据
            self.export_history_csv = ''
            
            self.hisTime = QTimer()
            self.hisTime.timeout.connect(self.his_time_func)
            self.hisTime.start(1500)
            self.hisNum = 0
            self.his_status = True
            self.hisShow.setText(hisdata_label5)
            
        elif self.hisShow.text() == hisdata_label5:
            self.hisTime.stop()
            self.his_status = False
            self.start_moni()
            self.hisShow.setText(hisdata_label4)
            
            # 允许导出历史记录
            self.export_history.setEnabled(True)
            
        elif self.hisShow.text() == hisdata_label4:
            self.stop_moni()
            self.export_history.setEnabled(False)
            if self.continue_status:
                self.hisTime.start(1000)
                self.his_status = True
                self.hisShow.setText(hisdata_label5)
    
    # 获取最近历史数据计时器
    def his_time_func(self):
        if self.hisNum == 0:
            # print('self.clear_his_status: {}'.format(self.clear_his_status))
            if self.clear_his_status == False:
                self.send_msg(bms_recent_history + calc_crc(bms_recent_history))
            try:
                if self.num_max == 0:
                    # print('self.num_max: {}'.format(self.num_max))
                    QMessageBox.information(self, 'tip', bms_logic_label27, QMessageBox.Ok)
                    self.hisTime.stop()
                    self.his_status = False
                    self.hisShow.setText(hisdata_label1)
                    self.start_moni()
            except Exception as e:
                print(f'获取最近历史数据计时器：{e}')
                return 0
            self.clear_his_status = True
            self.continue_status = True # 继续-暂停 标志位
            self.hisNum += 1
            # print('self.hisNum: {}'.format(self.hisNum))
            return 0
        
        # if self.num_max > 500:
        #     self.num_max = 500
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
            self.export_history.setEnabled(True)    # 允许导出历史数据

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
        
        # print(f'此次接收的数据：{res}')
        # 接收协议是否为 rs485
        if self.rs485_res_status == False:
            crc_error = False
            
            # 实时监控
            if res[:6] == f'{bms_monitor[:4]}c0' and len(res) == 394:
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
                        
                    if sys_label7 in p01['BMS工作状态2']:
                        self.hot_status.setStyleSheet('color:#01B481')
                    else:
                        self.hot_status.setStyleSheet('color:#626262')
                    
                    if sys_label8 in p01['BMS工作状态2']:
                        self.twoProtTrig_status.setStyleSheet('color:#01B481')
                    else:
                        self.twoProtTrig_status.setStyleSheet('color:#626262')

                    if len(p01['故障位']) > 0:
                        for _ in p01['故障位']:
                            txt = '\n'.join(p01['故障位'])
                            self.error_body.setText(txt)
                    else:
                        self.error_body.setText('')

                    warn_txt = '\n'.join(p01['警告位1']) + '\n' + '\n'.join(p01['警告位2'])
                    self.warn_body.setText(warn_txt)
                    protect_txt = '\n'.join(p01['保护位1']) + '\n' + '\n'.join(p01['保护位2'])
                    if self.login:
                        if '207' in protect_txt:
                            if self.testmode_btn.text() == switch_label6:
                                self.testmode_btn.setEnabled(False)
                            elif self.testmode_btn.text() == switch_label7:
                                self.testmode_btn_func()
                                self.testmode_btn.setEnabled(False)
                        else:
                            if self.testmode_btn.text() == switch_label6:
                                self.testmode_btn.setEnabled(True)
                        
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
                    self.cellLine1.setText(f"{float(p01[vol_label17 + '(V)']):.3f}")
                    self.cellLine2.setText(f"{float(p01[vol_label18 + '(V)']):.3f}")
                    self.cellLine3.setText(f"{float(p01[vol_label19 + '(V)']):.3f}")
                    
                    # 数据显示
                    display_data = [
                        self.cell_temp_16,
                        self.tem_other,
                        self.cell_vol_16,
                    ]
                    for index in range(len(display_data)):
                        for k,v in display_data[index].items():
                            if '℃' in k:
                                display_data[index][k].setText(f'{float(p01[k]):.1f}')
                            else:
                                display_data[index][k].setText(f'{float(p01[k]):.3f}')
                            
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
            
            # 蜂鸣器状态
            elif res[:6] == f'{bms_beep[:4]}02' and len(res) == 14 and self.beep_tag:
                print('蜂鸣器状态')
                self.beep_tag = False
                
                num = int(res[6:10], 16)
                self.buzzer_sw.blockSignals(True)
                
                if num == 0:
                    self.buzzer_sw.setChecked(False)
                elif num == 1:
                    self.buzzer_sw.setChecked(True)
                    
                self.buzzer_sw.blockSignals(False)
            
            # 参数设置
            elif res[:6] == f'{bms_setting[:4]}b6' and len(res) == 374:
                print('参数设置')
                self.p03 = pars_data(res, bms_setting + calc_crc(bms_setting))
                if len(self.p03) == 2:
                    crc_error = True
                else:
                    for k,v in self.tab3_form_dic.items():
                        self.tab3_form_dic[k].blockSignals(True)

                    for k,v in self.p03.items():
                        try:
                            print(k, v)
                            self.tab3_form_dic[k].setValue(float(v))
                        except KeyError as e:
                            print(f'参数设置 KeyError：{e}')
                            continue
                        except Exception:
                            self.tab3_form_dic[k].setValue(int(v))
                    
                    for k,v in self.tab3_form_dic.items():
                        self.tab3_form_dic[k].blockSignals(False)
                        
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
                        # 记录历史数据
                        if ',' in p06[k]:
                            p06[k] = p06[k].replace(',', '/')
                        self.export_history_csv += p06[k] + ','
                        count += 1
                    self.export_history_csv += '\n'
            
            # 读取版本号
            elif res[:6] == f'{bms_version[:4]}04' and len(res) == 18 and self.ver == True:
                print('读取版本号')
                # v1 = res[6:8]
                v2 = res[8:10]
                v3 = res[10:12]
                v4 = res[12:14]
                
                ver2 = int(v2, 16) if int(v2, 16) <= 9 else v2
                ver3 = int(v3, 16) if int(v3, 16) <= 9 else v3
                ver4 = int(v4, 16) if int(v4, 16) <= 9 else v4
                
                self.version.setText(f'{ver_label1}：{ver2}.{ver3}.{ver4}')
                self.ver = False
            
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
            elif res[:6] == f'{bms_sys_set1[:4]}04' and len(res) == 18 and self.sys_status_2 == True:
                print('读取系统设置-电量数据')
                ele_data = pars_data(res, bms_sys_set1 + calc_crc(bms_sys_set1))
                self.remainCap.setText(ele_data[f'{battery_label3}(AH)'])
                self.fullCap_Line.setText(ele_data[f'总容量(AH)'])
                self.sys_status_2 = False
            
            # 读取系统设置-电量数据2
            elif res[:6] == f'{bms_sys_set2[:4]}02' and len(res) == 14 and self.sys_status_1 == True:
                print('读取系统设置-电量数据2')
                ele_data = pars_data(res, bms_sys_set2 + calc_crc(bms_sys_set2))
                self.designCap.setText(ele_data[f'设计容量(AH)'])
                self.sys_status_1 = False
            
            # 读取系统设置-通信协议选择
            elif res[:6] == f'{bms_sys_protocol[:4]}02' and len(res) == 14 and self.Pro_status == True:
                self.Pro_status = False
                # 01 03 02 0b 02 3e b5
                print('读取系统设置-通讯协议')
                res_can = int(res[6:8], 16)
                res_485 = int(res[8:10], 16)
                self.Pro_can_combox.setCurrentIndex(res_can)
                self.Pro_485_combox.setCurrentIndex(res_485)
            
            # 历史数据总数 
            elif res[:6] == f'{bms_recent_history[:4]}02' and len(res) == 14:
                print('历史数据总数')
                # print(res[6:10])
                self.num_max = int(res[6:10], 16)
                # print('self.num_max: {}'.format(self.num_max))
            
            # CRC16 校验失败
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
                    self.pal_many_repeat = False    # 重置循环发送的状态
                    self.pal_start_time_setp += 1   # 跳过获取告警量
                    
                    self.add_tableItem('↑', res)
                    return 0
            
            # 获取 PACK 模拟量响应信息 42 (未获取电压温度个数)
            elif res[26:30] == '3432' and self.get_parallel_vol_tmp == False:
                
                # 完整协议示例：
                # self.json_rs485
                
                # 电压个数 3130 → 16
                vol_num = res[34:38]
                vol_asc2hex = chr(int(vol_num[:2], 16)) + chr(int(vol_num[2:], 16))
                vol_hex2dec = int(vol_asc2hex, 16)
                print(f'电压个数：{vol_hex2dec}')
                
                # 温度个数 3039 → 09
                tmp_num = res[vol_hex2dec*8+38 : vol_hex2dec*8+42]
                tmp_asc2hex = chr(int(tmp_num[:2], 16)) + chr(int(tmp_num[2:], 16))
                tmp_hex2dec = int(tmp_asc2hex, 16)
                print(f'温度个数：{tmp_hex2dec}')
                
                # 创建 PACK 模拟量协议
                self.parallel_pack_simulate = {
                    "Command":[0, 4, 1, ""],
                    "电池单体个数":[4, 4, 1, ""]
                }
                
                # 动态生成电压个数
                for i in range(1, vol_hex2dec+1):
                    self.parallel_pack_simulate[f"Cell{palnum_label1}_{i}"] = [i*8, 8, 1, "mV"]
                
                # 动态生成温度个数
                self.parallel_pack_simulate["监测温度个数"] = [(vol_hex2dec+1)*8, 4, 1, ""]
                tmp_num_index = (vol_hex2dec+1)*8+4
                for i in range(0, tmp_hex2dec):
                    self.parallel_pack_simulate[f"{palnum_label2}_{i+1}"] = [i*8+tmp_num_index, 8, -10, "℃"]
                
                tmp_end_index = (tmp_hex2dec-1)*8+tmp_num_index
                
                # 添加 PACK模拟量 结尾部分的协议
                self.parallel_pack_simulate[palnum_label3] = [tmp_end_index+8, 8, -100, "A"]                    # PACK电流
                self.parallel_pack_simulate[f"PACK {paldata_label4}"] = [tmp_end_index+8+8, 8, -100, "V"]       # 总电压
                self.parallel_pack_simulate[f"PACK {battery_label3}"] = [tmp_end_index+8+8+8, 8, 100, "AH"]     # 剩余容量
                self.parallel_pack_simulate["用户自定义个数"] = [tmp_end_index+8+8+8+8, 4, 1, ""]
                self.parallel_pack_simulate[f"PACK {battery_label4}"] = [tmp_end_index+8+8+8+8+4, 8, 100, "AH"] # 充满容量
                self.parallel_pack_simulate[palnum_label7] = [tmp_end_index+8+8+8+8+4+8, 8, 1, ""]              # 充放电循环次数
                self.parallel_pack_simulate[palnum_label8] = [tmp_end_index+8+8+8+8+4+8+8, 8, 100, "AH"]        # PACK设计容量
                self.parallel_pack_simulate["PACK SOC"] = [tmp_end_index+8+8+8+8+4+8+8+8, 8, 1, "%"]
                
                # --------------------------------------------------------------------- #
                
                # 创建 告警量 协议
                self.parallel_pack_tmp = {
                    "Command2":[0, 4, 1, ""],
                    "电池单体告警个数":[4, 4, 1, ""],
                }
                
                # 动态生成电压个数
                for i in range(1, vol_hex2dec+1):
                    self.parallel_pack_tmp[f"Cell{palnum_label9}_{i}"] = [i*4+4, 4, 1, ""]
                
                # 动态生成温度个数
                tmp_warn_index = (vol_hex2dec+1)*4+4
                self.parallel_pack_tmp["监测温度告警个数"] = [tmp_warn_index, 4, 1, ""]
                
                for i in range(1, tmp_hex2dec+1):
                    self.parallel_pack_tmp[f"{palnum_label2}{palnum_label9}_{i}"] = [i*4+tmp_warn_index, 4, 1, ""]
                
                # 添加 PACK告警量 结尾部分的协议
                tmp_warn_end = (tmp_hex2dec+1)*4+tmp_warn_index
                self.parallel_pack_tmp[palnum_label10] = [tmp_warn_end, 4, 1, ""]
                self.parallel_pack_tmp[palnum_label11] = [tmp_warn_end+4, 4, 1, ""]
                self.parallel_pack_tmp[palnum_label12] = [tmp_warn_end+4+4, 4, 1, ""]
                self.parallel_pack_tmp[f"{group_tabel10}_1"] = [tmp_warn_end+4+4+4, 4, 1, "", {
                    "0":bms_rs485_label1,
                    "1":parset2_label2,
                    "2":bms_rs485_label2,
                    "3":bms_rs485_label3,
                    "4":bms_rs485_label4,
                    "5":bms_rs485_label5,
                    "6":bms_rs485_label6
                }]
                self.parallel_pack_tmp[f"{group_tabel10}_2"] = [tmp_warn_end+4+4+4+4, 4, 1, "", {
                    "0":parset5_label2,
                    "1":parset5_label5,
                    "2":parset6_label2,
                    "3":parset6_label5,
                    "4":bms_parse_label7,
                    "5":bms_parse_label8,
                    "6":bms_parse_label9,
                    "7":bms_rs485_label7
                }]
                self.parallel_pack_tmp[palnum_label14] = [tmp_warn_end+4+4+4+4+4, 4, 1, "", {
                    "0":bms_rs485_label8,
                    "1":"CFET",
                    "2":"DFET",
                    "3":bms_rs485_label9,
                    "4":bms_history_label20,
                    "5":"ACin",
                    
                    "7":bms_rs485_label10
                    }]
                self.parallel_pack_tmp[palnum_label15] = [tmp_warn_end+4+4+4+4+4+4, 4, 1, "", {
                    "0":bms_rs485_label11,

                    "4":bms_rs485_label12,
                    "5":f"LED{palnum_label9}"
                }]
                self.parallel_pack_tmp[group_tabel8] = [tmp_warn_end+4+4+4+4+4+4+4, 4, 1, "", {
                    "0":bms_rs485_label13,
                    "1":bms_rs485_label14,
                    "2":bms_parse_label17,
                    
                    "4":bms_rs485_label15,
                    "5":bms_parse_label19
                }]
                self.parallel_pack_tmp[f"{palnum_label16}_1"] = [tmp_warn_end+4+4+4+4+4+4+4+4, 4, 1, ""]
                self.parallel_pack_tmp[f"{palnum_label16}_2"] = [tmp_warn_end+4+4+4+4+4+4+4+4+4, 4, 1, ""]
                self.parallel_pack_tmp[f"{group_tabel9}_1"] = [tmp_warn_end+4+4+4+4+4+4+4+4+4+4, 4, 1, "", {
                    "0":bms_rs485_label16,
                    "1":bms_rs485_label17,
                    "2":bms_rs485_label18,
                    "3":bms_rs485_label19,
                    "4":bms_parse_label36,
                    "5":bms_parse_label37
                }]
                self.parallel_pack_tmp[f"{group_tabel9}_2"] = [tmp_warn_end+4+4+4+4+4+4+4+4+4+4+4, 4, 1, "", {
                    "0":bms_parse_label28,
                    "1":bms_parse_label29,
                    "2":bms_parse_label30,
                    "3":bms_parse_label31,
                    "4":bms_parse_label32,
                    "5":bms_parse_label33,
                    "6":bms_parse_label34,
                    "7":bms_rs485_label20
                }]
                
                # print(self.parallel_pack_simulate)
                # print(self.parallel_pack_tmp)
                
                # 已获得电压与温度个数
                self.get_parallel_vol_tmp = True
            
            # 获取 PACK 模拟量响应信息 42 (已获取电压温度个数)
            elif res[26:30] == '3432' and self.get_parallel_vol_tmp:
                msg = res[30:-10]  # 去掉前缀报文和校验码
                adr = ''
                for k,v in self.parallel_pack_simulate.items():
                    temp = ''
                    for i in range(v[0], v[0]+v[1], 2):
                        temp += chr(int(msg[i:i + 2], 16))
                    if k == 'Command':
                        adr = int(temp, 16)
                    elif k == palnum_label3:
                        num = Common.format_num(Common.signBit_func(temp) / abs(v[2]))
                        data = f'{num} {v[3]}'
                    
                        # 如果开启并联轮询，则总电流累加
                        if self.pal_loop_status.isChecked():
                            self.pal_count_elc += num
                    
                    elif palnum_label2 in k or bms_history_label3 in k: # 温度、电流
                        data = f'{Common.format_num(Common.signBit_func(temp) / abs(v[2]))} {v[3]}'
                    else:
                        data = f'{Common.format_num(int(temp, 16) / abs(v[2]))} {v[3]}'
                    if k in self.col_labels:
                        self.palTable.setItem(self.col_labels.index(k), int(adr)-1, QTableWidgetItem(str(data)))

            # 获取 PACK 告警量 44 (已获取电压温度个数)
            elif res[26:30] == '3434' and self.get_parallel_vol_tmp:
                msg = res[30:-10]
                adr = ''
                for k,v in self.parallel_pack_tmp.items():
                    pack_warn = False
                    temp = ''
                    for i in range(v[0], v[0]+v[1], 2):
                        # ASCII 转成 十六进制
                        temp += chr(int(msg[i:i + 2], 16))
                    data = int(temp, 16)
                    if k == 'Command2':
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

            # 获取电池系统运行模拟量信息
            elif res[26:30] == '3631':
                msg = res[34:-10]
                # print(msg)
                for k,v in self.json_rs485['获取电池系统运行模拟量信息'].items():
                    temp = ''
                    for i in range(v[0], v[0]+v[1], 2):
                        # ASCII 转成 十六进制
                        temp += chr(int(msg[i:i + 2], 16))
                    data = int(temp, 16)
                    # print(k, data)
                    if k == '电池组系统总电流':
                        self.total_elc.setText(str(round(self.pal_count_elc, 2)))
                    elif k == '电池组系统SOC':
                        self.bin_avg_soc.setValue(data)
                    elif k == '电池组系统总平均电压':
                        data = f'{Common.format_num(data / abs(v[2]))}'
                        self.avg_voltage.setText(data)
                    elif k == '单芯最高电压':
                        self.cell_max.setText(str(data))
                    elif k == '单芯最高电压所在模块':
                        self.cell_max_posi.setText(str(data))
                    elif k == '单芯最低电压':
                        self.cell_min.setText(str(data))
                    elif k == '单芯最低电压所在模块':
                        self.cell_min_posi.setText(str(data))
                    elif k == '单芯最高温度':
                        data = f'{Common.format_num(Common.signBit_func(temp) / abs(v[2]))}'
                        self.cell_max_tmp.setText(data)
                    elif k == '单芯最高温度所在模块':
                        self.cell_max_tmp_posi.setText(str(data))
                    elif k == '单芯最低温度':
                        data = f'{Common.format_num(Common.signBit_func(temp) / abs(v[2]))}'
                        self.cell_min_tmp.setText(data)
                    elif k == '单芯最低温度所在模块':
                        self.cell_min_tmp_posi.setText(str(data))
                        
            self.add_tableItem('↑', res)
    