import serial, functools, gettext
from .OrderList import *
from utils.Common import Common
from utils.CRC16Util import calc_crc
from ui.pf_off_inverter_layout import Ui_MainWindow as invt_off_layout
from PyQt5 import QtWidgets

class Invt_pf_off_layout(QtWidgets.QMainWindow, invt_off_layout):
    
    def __init__(self):
        super(Invt_pf_off_layout, self).__init__()
        self.setupUi(self)
        self.Invt_pf_off_layout_init()
        # self.Invt_pf_off_i18n_init()
        self.setWindowTitle(f'{self.windowTitle()} v0.0.1')
        
    # 初始化加载所需
    def Invt_pf_off_layout_init(self):
        
        self.ivpo_open_port.setStyleSheet(color_close)
        self.ivpo_open_moni.setStyleSheet(color_close)
        
        # 加载串口对象
        self.invt_po_ser = serial.Serial()
        
        # 加载串口列表
        self.ivpo_port_list.addItems(Common.load_serial_list())
        
        # 加载-实时监控信号槽
        self.ivpo_monitor_slots()
        
    # 实时监控信号槽
    def ivpo_monitor_slots(self):
        self.ivpo_open_port.clicked.connect(self.ivpo_open_port_func)
        
    # 开/关串口信号
    def ivpo_open_port_func(self):
        if self.ivpo_open_port.text() == '打开串口':
            self.invt_po_ser.port = self.ivpo_port_list.currentText()
            self.invt_po_ser.timeout = 0.07
            self.invt_po_ser.baudrate = int(self.ivpo_baud_list.currentText())
            try:
                self.invt_po_ser.open()
            except serial.SerialException:
                QtWidgets.QMessageBox.information(self, 'Error', "串口打卡失败", QtWidgets.QMessageBox.Ok)
                return self.invt_po_ser.close()
            self.ivpo_open_port.setText('关闭串口')
            self.ivpo_open_port.setStyleSheet(color_open)
            self.ivpo_port_list.setEnabled(False)
        else:
            try:
                self.invt_po_ser.close()
            except Exception as e:
                print(e)
            self.ivpo_open_port.setText('打开串口')
            self.ivpo_open_port.setStyleSheet(color_close)
            self.ivpo_port_list.setEnabled(True)
        