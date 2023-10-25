# -*- coding: utf-8 -*-

import serial, functools, datetime, os, gettext, sys
from .OrderList import *
from utils.Common import Common
# from settings.ac_modbus import get_ac_data_list
# from utils.CRC16Util import calc_crc
# from utils.DataPars import pars_data
from ui.invt_layout import Ui_MainWindow as invt_layout
from PyQt5 import QtWidgets
# from PyQt5.QtCore import QSettings


class InvLayout(QtWidgets.QMainWindow, invt_layout):
    def __init__(self):
        super(InvLayout, self).__init__()
        self.setupUi(self)
        self.inverter_layout_init()
        # self.ivt_i18n_init()
        self.setWindowTitle(f'{self.windowTitle()} v0.0.1')

    def inverter_layout_init(self):
        # 初始化-实时监控
        self.ivt_ser = serial.Serial()
        self.ivt_open_port_btn.setStyleSheet(color_close)
        self.ivt_open_monitor_btn.setStyleSheet(color_close)
        # self.ac_monitor_on = False
        
        # 加载串口列表
        self.ivt_port_list.addItems(Common.load_serial_list())
        
        # 加载-实时监控信号槽
        self.ivt_monitor_slots()
    
    # 实时监控信号槽
    def ivt_monitor_slots(self):
        self.ivt_open_port_btn.clicked.connect(self.ivt_open_port_btn_func)
    
    # 按钮-打开/关闭串口
    def ivt_open_port_btn_func(self):
        ...