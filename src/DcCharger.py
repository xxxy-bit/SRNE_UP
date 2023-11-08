import serial, functools, gettext, datetime, os
from ui.dc_layout import Ui_MainWindow as dc_layout
from .OrderList import *
from utils.Common import Common
from utils.CRC16Util import calc_crc

from PyQt5 import QtWidgets, QtCore


class DCLayout(QtWidgets.QMainWindow, dc_layout):
    
    def __init__(self):
        super(DCLayout, self).__init__()

        self.setupUi(self)
        self.dc_layout_init()
        # self.dc_i18n_init()
        self.setWindowTitle(f'{self.windowTitle()} v0.0.1')
    
    # 初始化
    def dc_layout_init(self):
        
        self.dc_open_port.setStyleSheet(color_close)
        self.dc_open_monitor.setStyleSheet(color_close)
        
        # 加载日志目录
        self.log_name = Common.creat_log_file('log')
        
        # 加载串口对象
        self.dccharger_ser = serial.Serial()
        
        # 加载串口列表
        self.dc_port_list.addItems(Common.load_serial_list())
        
        # 创建监控日志文件
        self.dccharger_now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        
        # 加载-实时监控信号槽
        self.dc_monitor_slots()

    # 实时监控信号槽
    def dc_monitor_slots(self):
        self.dc_open_port.clicked.connect(self.dc_open_port_func)
        self.dc_refresh_port.clicked.connect(self.dc_refresh_port_func)
        self.dc_open_monitor.clicked.connect(self.dc_open_monitor_func)
        self.dc_export_monitor.clicked.connect(self.dc_export_monitor_func)
        self.dc_onoff_power.clicked.connect(self.dc_onoff_power_func)
        self.dc_reset.clicked.connect(self.dc_reset_func)
        self.dc_factory_setting.clicked.connect(self.dc_factory_setting_func)
        self.dc_clear_alarm.clicked.connect(self.dc_clear_alarm_func)
        self.dc_clear_statistic.clicked.connect(self.dc_clear_statistic_func)
        self.dc_clear_his.clicked.connect(self.dc_clear_his_func)
    
    # 打开串口
    def dc_open_port_func(self):
        if self.dc_open_port.text() == '打开串口':
            self.dccharger_ser.port = self.dc_port_list.currentText()
            self.dccharger_ser.baudrate = int(self.dc_baud_list.currentText())
            self.dccharger_ser.timeout = 0.07
            try:
                self.dccharger_ser.open()
            except serial.SerialException:
                QtWidgets.QMessageBox.information(self, 'Error', ' 串口打开失败', QtWidgets.QMessageBox.Ok)
                return self.dccharger_ser.close()
            self.dc_open_port.setText('关闭串口')
            self.dc_open_port.setStyleSheet(color_open)
            self.dc_port_list.setEnabled(False)

            # 开启接收数据的定时器
        
        else:
            try:
                self.dccharger_ser.close()
            except Exception as e:
                print(e)
            self.dc_open_port.setText('打开串口')
            self.dc_open_port.setStyleSheet(color_close)
            self.dc_port_list.setEnabled(True)
        
    # 刷新串口
    def dc_refresh_port_func(self):
        self.dc_port_list.clear()
        self.dc_port_list.addItems(Common.load_serial_list())
    
    # 开启监控
    def dc_open_monitor_func(self):
        ...
        
    # 导出监控数据
    def dc_export_monitor_func(self):
        ...
    
    # 开关机
    def dc_onoff_power_func(self):
        ...
        
    # 复位
    def dc_reset_func(self):
        ...
        
    # 恢复出厂
    def dc_factory_setting_func(self):
        ...
        
    # 清除当前告警
    def dc_clear_alarm_func(self):
        ...
        
    # 清除统计量
    def dc_clear_statistic_func(self):
        ...

    # 清除历史记录
    def dc_clear_his_func(self):
        ...