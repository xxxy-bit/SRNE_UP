import serial, functools, gettext, datetime, os
from .OrderList import *
from utils.Common import Common
from utils.CRC16Util import calc_crc
from ui.pf_off_inverter_layout import Ui_MainWindow as invt_off_layout
from PyQt5 import QtWidgets, QtCore

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
        
        # 加载日志目录
        self.log_name = Common.creat_log_file('log')
        
        # 加载串口对象
        self.invt_po_ser = serial.Serial()
        
        # 加载串口列表
        self.ivpo_port_list.addItems(Common.load_serial_list())
        
        # 加载-实时监控信号槽
        self.ivpo_monitor_slots()
        
        # 设置串口数据单元格的长度
        self.ivpo_port_tableWidget.setColumnWidth(0,180)
        self.ivpo_port_tableWidget.setColumnWidth(1,100)
        self.ivpo_port_tableWidget.setColumnWidth(2,765)
        
    # 实时监控信号槽
    def ivpo_monitor_slots(self):
        self.ivpo_open_port.clicked.connect(self.ivpo_open_port_func)
        self.ivpo_power_on.clicked.connect(self.ivpo_power_on_func)
        self.ivpo_factory_reset.clicked.connect(self.ivpo_factory_reset_func)
        self.ivpo_reset.clicked.connect(self.ivpo_reset_func)
        self.ivpo_open_moni.clicked.connect(self.ivpo_open_moni_func)
        
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
    
    # 开/关机
    def ivpo_power_on_func(self):
        if self.ivpo_power_on.text() == '开启':
            self.ivpo_send_msg(ivpo_sw_on + calc_crc(ivpo_sw_on))
            self.ivpo_power_on.setText('关闭')
        else:
            self.ivpo_send_msg(ivpo_sw_off + calc_crc(ivpo_sw_off))
            self.ivpo_power_on.setText('开启')
            
    # 恢复出厂
    def ivpo_factory_reset_func(self):
        self.ivpo_send_msg(ivpo_fact_reset + calc_crc(ivpo_fact_reset))
    
    # 设备复位
    def ivpo_reset_func(self):
        self.ivpo_send_msg(ivpo_resetting + calc_crc(ivpo_resetting))

    # 开/关数据监控
    def ivpo_open_moni_func(self):
        self.ivpo_timer_get_monitor = QtCore.QTimer()
        if self.ivpo_open_moni.text() == '开启监控':
            self.ivpo_open_moni.setText('关闭监控')
            self.ivpo_open_moni.setStyleSheet(color_open)
            
            self.ivpo_timer_get_monitor.timeout.connect(self.ivpo_timer_get_monitor_func)
            self.ivpo_timer_get_monitor_step = 1
            self.ivpo_timer_get_monitor.start(1500)
            
        else:
            self.ivpo_open_moni.setText('开启监控')
            self.ivpo_open_moni.setStyleSheet(color_close)
            self.ivpo_timer_get_monitor.stop()
    
    # 开启监控定时器
    def ivpo_timer_get_monitor_func(self):
        if self.ivpo_timer_get_monitor_step == 1:
            self.ivpo_send_msg(ivpo_product_msg + calc_crc(ivpo_product_msg))
        elif self.ivpo_timer_get_monitor_step == 2:
            self.ivpo_send_msg(ivpo_control_msg + calc_crc(ivpo_control_msg))
        elif self.ivpo_timer_get_monitor_step == 3:
            self.ivpo_send_msg(ivpo_ivt_msg + calc_crc(ivpo_ivt_msg))
            self.ivpo_timer_get_monitor_step = 1
            return 0
        self.ivpo_timer_get_monitor_step += 1


    # 增加一行数据收发
    def ivpo_add_tableItem(self, status: str, hexdata: str, tableWidget: QtWidgets.QTabWidget, log_dir):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        rows = tableWidget.rowCount()
        # 最大行数
        if rows > 50:
            tableWidget.removeRow(0)
            rows = tableWidget.rowCount()
        tableWidget.setRowCount(rows + 1)

        # 添加时间
        tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(str(now)))

        # 添加↑↓标志并居中
        DirectionItem = QtWidgets.QTableWidgetItem(status)
        DirectionItem.setTextAlignment(QtCore.Qt.AlignCenter)
        # DirectionItem.setFont(QFont('times', 14))
        tableWidget.setItem(rows, 1, DirectionItem)
        
        # 每两个字节增加一个空格
        space_hexdata = list(hexdata)
        for i in range(len(space_hexdata)-1)[::-1]:
            if i % 2 != 0:
                space_hexdata.insert(i+1, ' ')
        hexdata = ''.join(space_hexdata)

        # 写入日志文件
        with open(log_dir, 'a+', encoding='utf-8') as f:
            f.write(f'{now}\t{status}\t{hexdata}\n')
        
        # 添加数据
        tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(hexdata))
        # 滚动条滚动到最下方
        tableWidget.verticalScrollBar().setSliderPosition(tableWidget.rowCount())

        # 发送数据
    
    # 发送数据
    def ivpo_send_msg(self, data: str):
        hex_data = bytes.fromhex(data)
        try:
            self.invt_po_ser.write(hex_data)
        except serial.serialutil.PortNotOpenError as e:
            self.invt_po_ser.close()
            print(e)
            return False
        # 在表格中输出
        self.ivpo_add_tableItem('send', bytes.hex(hex_data), self.ivpo_port_tableWidget, self.log_name)
    
    # 接收数据
    