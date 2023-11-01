import serial, functools, gettext, datetime, os
from .OrderList import *
from utils.Common import Common
from utils.CRC16Util import calc_crc
from .dataAnalysis.ivpo_DA import ivpo_data_analysis
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
        
        # 加载-参数设置信号槽
        self.ivpo_parameter_slots()
        
        # 加载-串口数据信号槽
        self.ivpo_clear_port_msg.clicked.connect(functools.partial(self.ivpo_clearRow_btn, self.ivpo_port_tableWidget))
        
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
            
            # 开启接收数据定时器
            self.ivpo_timer_recevice = QtCore.QTimer()
            self.ivpo_timer_recevice.timeout.connect(self.ivpo_timer_recevice_func)
            self.ivpo_timer_recevice.start(500)
        else:
            try:
                self.invt_po_ser.close()
            except Exception as e:
                print(e)
            self.ivpo_open_port.setText('打开串口')
            self.ivpo_open_port.setStyleSheet(color_close)
            self.ivpo_port_list.setEnabled(True)
            self.ivpo_timer_recevice.stop()
    
    # 参数设置信号槽
    def ivpo_parameter_slots(self):
        self.ivpo_read_data.clicked.connect(self.ivpo_read_data_func)
    
    # 参数设置-读取数据
    def ivpo_read_data_func(self):
        self.ivpo_timer_get_setting = QtCore.QTimer()
        self.ivpo_timer_get_setting.timeout.connect(self.ivpo_timer_get_setting_func)
        self.ivpo_timer_get_setting_step = 1
        self.ivpo_timer_get_setting.start(1000)
    
    # 参数设置-读取数据-定时器
    def ivpo_timer_get_setting_func(self):
        if self.ivpo_timer_get_setting_step == 1:
            self.ivpo_send_msg(ivpo_setting1 + calc_crc(ivpo_setting1))
        else:
            self.ivpo_send_msg(ivpo_setting2 + calc_crc(ivpo_setting2))
            self.ivpo_timer_get_setting.stop()
            return 0
        self.ivpo_timer_get_setting_step += 1
    
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
            self.ivpo_send_msg(ivpo_history_days + calc_crc(ivpo_history_days))
        elif self.ivpo_timer_get_monitor_step == 3:
            self.ivpo_send_msg(ivpo_control_msg + calc_crc(ivpo_control_msg))
        elif self.ivpo_timer_get_monitor_step == 4:
            self.ivpo_send_msg(ivpo_ivt_msg + calc_crc(ivpo_ivt_msg))
            self.ivpo_timer_get_monitor_step = 1
            return 0
        self.ivpo_timer_get_monitor_step += 1

    # 增加一行数据收发
    def ivpo_add_tableItem(self, status: str, hexdata: str, tableWidget: QtWidgets.QTabWidget, log_name):
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
        with open(log_name, 'a+', encoding='utf-8') as f:
            f.write(f'{now}\t{status}\t{hexdata}\n')
        
        # 添加数据
        tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(hexdata))
        # 滚动条滚动到最下方
        tableWidget.verticalScrollBar().setSliderPosition(tableWidget.rowCount())

        # 发送数据
    
    # 清空表格
    def ivpo_clearRow_btn(self, tableWidget):
        rowPosition = tableWidget.rowCount()
        for rows in range(rowPosition)[::-1]:
            tableWidget.removeRow(rows)
    
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
    
    # 接收数据定时器
    def ivpo_timer_recevice_func(self):
        
        try:
            res = self.invt_po_ser.readline()
            res = res.hex()
        except Exception as e:
            print(e)
            return False
        
        if res != '':
            # print(res)
            # 实时监控
            if res[:6] == f'{ivpo_product_msg[:4]}c4' and len(res) == 402:
                arg = ivpo_data_analysis(res, ivpo_product_msg)
                result = arg[0]

                # 异常后打印问题字段，防止程序崩溃
                try:
                    temp1 = result['系统电压']
                    temp2 = result['产品类型']
                    temp3 = result['产品型号']
                    temp4 = result['软件版本']
                    temp5 = result['硬件版本']
                    temp6 = result['产品序列号']
                    temp7 = result['设备地址']
                    temp8 = result['设备名称']
                except Exception as e:
                    self.ivpo_add_tableItem('receive', res, self.ivpo_port_tableWidget, self.log_name)
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)  
                
                self.ivpo_sys_vol.setText(temp1)
                self.ivpo_product_type.setText(temp2)
                self.ivpo_product_model.setText(temp3)
                self.ivpo_software_ver.setText(temp4)
                self.ivpo_hardware_ver.setText(temp5)
                self.ivpo_serial_num.setText(temp6)
                self.ivpo_dev_addr.setText(temp7)
                self.ivpo_dev_name.setText(temp8)
            
            # 总运行天数
            elif res[:6] == f'{ivpo_history_days[:4]}02' and len(res) == 14:
                arg = ivpo_data_analysis(res, ivpo_history_days)
                result = arg[0]
                self.ivpo_total_runner_days.setText(result['总运行天数'])
            
            # 控制器数据区
            elif res[:6] == f'{ivpo_control_msg[:4]}08' and len(res) == 26:
                arg = ivpo_data_analysis(res, ivpo_control_msg)
                result = arg[0]
                
                try:
                    temp1 = result['蓄电池电压']
                    temp2 = result['充电电流']
                    temp3 = result['充电状态']
                except Exception as e:
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)  
                
                self.ivpo_bat_vol.setText(temp1)
                self.ivpo_char_cur.setText(temp2)
                self.ivpo_char_status.setText(temp3)
            
            # 逆变数据区
            elif res[:6] == f'{ivpo_ivt_msg[:4]}50' and len(res) == 170:
                arg = ivpo_data_analysis(res, ivpo_ivt_msg)
                result = arg[0]
                
                try:
                    temp1 = result['当前时间']
                    temp2 = result['交流输出有功功率']
                    temp3 = result['交流输出电压1']
                    temp4 = result['交流输出电流']
                    temp5 = result['交流输出频率']
                    temp6 = result['温度A']
                    temp7 = result['温度B']
                    temp8 = result['温度C']
                    temp9 = result['温度D']
                    temp10 = result['外部温度']
                    temp11 = result['交流输入频率']
                    temp12 = result['交流输入有功功率']
                    temp13 = result['交流输入电压A']
                    temp14 = result['交流输入电流A']
                    temp15 = result['交流输出电压2']
                    temp16 = result['当前故障码']
                except Exception as e:
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)  
                
                self.ivpo_now_time.setText(temp1)
                self.ivpo_acout_active_power.setText(temp2)
                self.ivpo_acout_vol1.setText(temp3)
                self.ivpo_acout_cur.setText(temp4)
                self.ivpo_acout_fre.setText(temp5)
                self.ivpo_tmpA.setText(temp6)
                self.ivpo_tmpB.setText(temp7)
                self.ivpo_tmpC.setText(temp8)
                self.ivpo_tmpD.setText(temp9)
                self.ivpo_outside_tmp.setText(temp10)
                self.ivpo_acinput_fre.setText(temp11)
                self.ivpo_acinput_active_power.setText(temp12)
                self.ivpo_acinput_volA.setText(temp13)
                self.ivpo_acinput_curA.setText(temp14)
                self.ivpo_acout_vol2.setText(temp15)
                self.ivpo_now_error.setText(temp16)
            
            # 用户设置区1
            elif res[:6] == f'{ivpo_setting1[:4]}40':
                arg = ivpo_data_analysis(res, ivpo_setting1)
                result = arg[0]
                
                self.ivpo_char_cur_set.setValue(float(result['充电电流设置(A)']))
                self.ivpo_bat_type.setCurrentIndex(int(result['蓄电池类型']))
                self.ivpo_over_vol.setValue(float(result['超压电压(V)']))
                self.ivpo_char_limit_vol.setValue(float(result['充电限制电压(V)']))
                self.ivpo_eq_char_vol.setValue(float(result['均衡充电电压(V)']))
                self.ivpo_boost_char_vol.setValue(float(result['提升充电电压(V)']))
                self.ivpo_float_char_vol.setValue(float(result['浮充充电电压(V)']))
                self.ivpo_inchar_rerturn_vol.setValue(float(result['提升充电返回电压(V)']))
                self.ivpo_op_returnvol.setValue(float(result['过放返回电压(V)']))
                self.ivpo_odc_vol.setValue(float(result['过放电压(V)']))
                self.ivpo_boost_char_time.setValue(int(result['提升充电时间(Min)']))
                self.ivpo_eq_char_interval.setValue(int(result['均衡充电间隔(day)']))
                self.ivpo_tmp_comp_coe.setValue(int(result['温度补偿系数(mV/℃/2V)']))
                self.ivpo_bat_char_low_tmp.setValue(int(result['电池充电下限温度(℃)']))
                self.ivpo_full_stop_cur.setValue(int(result['充满截止电流(A)']))
                self.ivpo_lead_active.setCurrentIndex(int(result['铅酸激活']))
                self.ivpo_libat_low_tmp_char.setCurrentIndex(int(result['锂电池低温充电(℃)']))
                self.ivpo_relay_out_func.setCurrentIndex(int(result['继电器输出功能']))
                
            # 用户设置区2
            elif res[:6] == f'{ivpo_setting2[:4]}26':
                arg = ivpo_data_analysis(res, ivpo_setting2)
                result = arg[0]

                print(result)
                
                self.ivpo_out_pri.setCurrentIndex(int(result['输出优先级']))
                self.ivpo_fan_start_tmp.setValue(int(result['风扇启动温度(℃)']))
                self.ivpo_eco_start_power.setValue(int(result['ECO启动功率(W)']))
                self.ivpo_acout_vol.setValue(int(result['交流输出电压(V)']))
                self.ivpo_acout_fre_2.setValue(int(result['交流输出频率(Hz)']))
                self.ivpo_eco_start_time.setValue(int(result['ECO启动时间(S)']))
                self.ivpo_inv_state_mode.setCurrentIndex(int(result['逆变状态模式']))
                self.ivpo_buzz_set.setCurrentIndex(int(result['蜂鸣器设置']))
                self.ivpo_out_switch_vol.setValue(int(result['输出切换电压(V)']))
                self.inpo_acinput_cur_set.setValue(int(result['AC输入电流设置(A)']))
            
            self.ivpo_add_tableItem('receive', res, self.ivpo_port_tableWidget, self.log_name)
            
            