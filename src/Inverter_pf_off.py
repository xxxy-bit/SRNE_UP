import serial, functools, datetime, os
from .OrderList import *
from utils.Common import Common
from utils.CRC16Util import calc_crc
from .dataAnalysis.ivpo_DA import ivpo_data_analysis
from settings.ivpo_modbus import ivpo_data_list
from ui.pf_off_inverter_layout import Ui_MainWindow as invt_off_layout
from PyQt5 import QtWidgets, QtCore

class Invt_pf_off_layout(QtWidgets.QMainWindow, invt_off_layout):
    
    def __init__(self):
        super(Invt_pf_off_layout, self).__init__()
        self.setupUi(self)
        self.Invt_pf_off_layout_init()
        # self.Invt_pf_off_i18n_init()
        self.setWindowTitle(f'{self.windowTitle()} v0.1.3')
        
    # 初始化加载所需
    def Invt_pf_off_layout_init(self):
        
        self.ivpo_open_port.setStyleSheet(color_close)
        self.ivpo_open_moni.setStyleSheet(color_close)
        
        # 标志位
        self.ivpo_port_switch = False   # 串口开关
        self.ivpo_moni_switch = False   # 监控开关
        
        # 加载日志目录
        self.log_name = Common.creat_log_file('log')
        
        # 加载串口对象
        self.invt_po_ser = serial.Serial()
        
        # 加载串口列表
        self.ivpo_port_list.addItems(Common.load_serial_list())
        
        # 加载数据校准列表
        self.ivpo_calibrate_addr = {
            '校准逆变电压': 'ff700216',
            '校准BAT电压': 'ff700101',
            '校准逆变电流': 'ff700217',
            '校准市电电压': 'ff700229',
            '校准市电电流': 'ff70022a',
            '校准EXITBAT电压': 'ff700201'
        }
        self.ivpo_calibrate_list.addItems([k for k, v in  self.ivpo_calibrate_addr.items()])
        
        # 创建监控日志文件
        self.ivpo_now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        self.pd_csv = ''
        self.ct_csv = ''
        self.iv_csv = ''
        
        # 加载-实时监控信号槽
        self.ivpo_monitor_slots()
        
        # 存储修改过的参数
        self.ivpo_setting_dic = {}
        
        # 参数设置框的对象
        self.ivpo_setting_edit = [
            self.ivpo_char_cur_set,
            self.ivpo_bat_type,
            self.ivpo_over_vol,
            self.ivpo_char_limit_vol,
            self.ivpo_eq_char_vol,
            self.ivpo_boost_char_vol,
            self.ivpo_float_char_vol,
            self.ivpo_float_char_vol,
            self.ivpo_op_returnvol,
            self.ivpo_odc_vol,
            self.ivpo_boost_char_time,
            self.ivpo_eq_char_interval,
            self.ivpo_tmp_comp_coe,
            self.ivpo_bat_char_low_tmp,
            self.ivpo_full_stop_cur,
            self.ivpo_lead_active,
            self.ivpo_libat_low_tmp_char,
            self.ivpo_relay_out_func,
            self.ivpo_out_pri,
            self.ivpo_fan_start_tmp,
            self.ivpo_eco_start_power,
            self.ivpo_acout_vol,
            self.ivpo_acout_fre_2,
            self.ivpo_eco_start_time,
            self.ivpo_inv_state_mode,
            self.ivpo_buzz_set,
            self.ivpo_out_switch_vol,
            self.inpo_acinput_cur_set
        ]
        
        # 写入数据 Enable：False
        self.ivpo_write_data.setEnabled(False)
        
        # 加载-参数设置信号槽
        self.ivpo_parameter_slots()
        
        # 创建发送与接收数据总数
        self.ivpo_send_data_count = 0
        self.ivpo_recv_data_count = 0
        
        # 加载-串口数据信号槽
        self.ivpo_clear_port_msg.clicked.connect(functools.partial(self.ivpo_clearRow_btn, self.ivpo_port_tableWidget))

        # 加载系统设置信号槽
        self.ivpo_sys_setting_slots()
        
        # 隐藏行序号
        self.ivpo_port_tableWidget.verticalHeader().setVisible(False)
        
        # 设置串口数据单元格的长度
        self.ivpo_port_tableWidget.setColumnWidth(0,180)
        self.ivpo_port_tableWidget.setColumnWidth(1,100)
        self.ivpo_port_tableWidget.setColumnWidth(2,760)
        
    # 系统设置信号槽
    def ivpo_sys_setting_slots(self):
        self.ivpo_calibrate_btn.clicked.connect(self.ivpo_calibrate_btn_func)

    # 系统设置-数据校准
    def ivpo_calibrate_btn_func(self):
        if self.ivpo_port_switch == False:
            return QtWidgets.QMessageBox.information(self, 'tips', '串口未打开', QtWidgets.QMessageBox.Ok)
        
        # 检测监控是否已开启，开启则自动关闭，校准完毕重新自动打开        
        try:
            if self.ivpo_timer_get_monitor.isActive():
                self.ivpo_timer_get_monitor.stop()
                self.ivpo_moni_switch = True
        except Exception as e:
            print(e)
            self.ivpo_moni_switch = False
        
        txt = self.ivpo_calibrate_list.currentText()
        hex_addr = self.ivpo_calibrate_addr[txt]
        if '电流' in txt:
            # 电流倍率 0.01
            hex_num = format(int(float(self.ivpo_calibrate_data.text()) * 100), '04x')
        else:
            # 电压倍率 0.1
            hex_num = format(int(float(self.ivpo_calibrate_data.text()) * 10), '04x')
        print(hex_num)
        print(hex_addr, txt)
        
        self.ivpo_calibrate_msg = hex_addr + hex_num + '000'
        print(self.ivpo_calibrate_msg)
        
        self.ivpo_calibrate_time = QtCore.QTimer()
        self.ivpo_calibrate_time_setp = 1
        self.ivpo_calibrate_time.timeout.connect(self.ivpo_calibrate_btn_timer)
        self.ivpo_calibrate_time.start(1000)
        
    # 系统设置-数据校准-定时器
    def ivpo_calibrate_btn_timer(self):
        msg = self.ivpo_calibrate_msg + str(self.ivpo_calibrate_time_setp)
        self.ivpo_send_msg(msg + calc_crc(msg))
        
        self.ivpo_calibrate_pro.setValue(self.ivpo_calibrate_time_setp)
        
        self.ivpo_calibrate_time_setp += 1
        if self.ivpo_calibrate_time_setp == 7:
            if self.ivpo_moni_switch:
                self.ivpo_timer_get_monitor.start(int(self.ivpo_send_time.text()))
            self.ivpo_calibrate_time.stop()
        
    # 实时监控信号槽
    def ivpo_monitor_slots(self):
        self.ivpo_open_port.clicked.connect(self.ivpo_open_port_func)
        self.ivpo_power_on.clicked.connect(self.ivpo_power_on_func)
        self.ivpo_factory_reset.clicked.connect(self.ivpo_factory_reset_func)
        self.ivpo_reset.clicked.connect(self.ivpo_reset_func)
        self.ivpo_open_moni.clicked.connect(self.ivpo_open_moni_func)
        self.ivpo_export_monit_data.clicked.connect(self.ivpo_export_monit_data_func)
    
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
            self.ivpo_port_switch = True
            
            # 开启接收数据定时器
            self.ivpo_timer_recevice = QtCore.QTimer()
            self.ivpo_timer_recevice.timeout.connect(self.ivpo_timer_recevice_func)
            self.ivpo_timer_recevice.start(1000)
        else:
            try:
                self.invt_po_ser.close()
            except Exception as e:
                print(e)
            self.ivpo_open_port.setText('打开串口')
            self.ivpo_open_port.setStyleSheet(color_close)
            self.ivpo_port_list.setEnabled(True)
            self.ivpo_port_switch = False
            self.ivpo_timer_recevice.stop()
    
    # 导出数据
    def ivpo_export_monit_data_func(self):
        # 创建监控日志
        log_monitor_dir = os.path.join('log', f'ivpo_monitor_{self.ivpo_now}')
        log_monitor_product_name = os.path.join(log_monitor_dir, f'product_{self.ivpo_now}.csv')
        log_monitor_control_name = os.path.join(log_monitor_dir, f'control_{self.ivpo_now}.csv')
        log_monitor_inverter_name = os.path.join(log_monitor_dir, f'inverter_{self.ivpo_now}.csv')
        if os.path.exists(log_monitor_dir) == False:
            os.makedirs(log_monitor_dir)
            
        if os.path.exists(log_monitor_product_name) == False:
            with open(log_monitor_product_name, 'w') as f:
                pd_txt = '系统最高支持电压,产品类型,产品型号,软件版本,硬件版本,产品序列号,设备地址,设备名称,原始数据(Hex)'
                f.write(pd_txt + '\n')
                
        if os.path.exists(log_monitor_control_name) == False:
            with open(log_monitor_control_name, 'w') as f:
                ct_txt = '蓄电池电压,充电电流,充电状态,原始数据(Hex)'
                f.write(ct_txt + '\n')
                
        if os.path.exists(log_monitor_inverter_name) == False:
            with open(log_monitor_inverter_name, 'w') as f:
                iv_txt = '当前时间,交流输出有功功率,交流输出电压1,交流输出电流,交流输出频率,温度A,温度B,温度C,温度D,外部温度,交流输入频率,交流输入有功功率,交流输入电压A,交流输入电流A,交流输出电压2,当前故障码,原始数据(Hex)'
                f.write(iv_txt + '\n')
                
        # 写入监控日志
        try:
            with open(log_monitor_product_name, 'a') as f:
                f.write(self.pd_csv)
            with open(log_monitor_control_name, 'a') as f:
                f.write(self.ct_csv)
            with open(log_monitor_inverter_name, 'a') as f:
                f.write(self.iv_csv)
        except PermissionError:
            return QtWidgets.QMessageBox.critical(self, 'Error', '文件被占用，请关闭Excel文件后重试.', QtWidgets.QMessageBox.Ok)  
        except Exception as e:
            return QtWidgets.QMessageBox.critical(self, 'Error', f'{e}\n未知错误，请联系相关开发人员.', QtWidgets.QMessageBox.Ok)  
        
        # 是否需要主动打开目录
        open_dir =os.path.join(os.getcwd(), log_monitor_dir)
        if QtWidgets.QMessageBox.question(self, 'Tips', f'导出成功，目录位置为：{open_dir}\n是否需要打开该目录?', 
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            os.startfile(open_dir)
            
    # 参数设置信号槽
    def ivpo_parameter_slots(self):
        self.ivpo_read_data.clicked.connect(self.ivpo_read_data_func)
        self.ivpo_write_data.clicked.connect(self.ivpo_write_data_func)

        for s in self.ivpo_setting_edit:
            try:
                s.valueChanged.connect(functools.partial(self.ivpo_setting_edit_func, s))
            except AttributeError:
                s.currentIndexChanged.connect(functools.partial(self.ivpo_setting_edit_func, s))
                
    # 获取修改过的参数
    def ivpo_setting_edit_func(self, set_text):
        try:
            temp = set_text.value()
        except AttributeError:
            current_text = set_text.currentText()
            # 查找文本的下标
            temp = set_text.findText(current_text)
            
        if temp != '':
            name = set_text.whatsThis()[22:-18]
            # print(name)
            
            if name == '温度补偿系数(mV/℃/2V)':
                temp = abs(temp)
            elif name == '电池充电下限温度(℃)':
                if temp < 0:
                    temp = abs(temp) + 128
                
            try:
                send_msg = ivpo_setting1
                name_data = int(temp) * int(ivpo_data_list[send_msg][name][2])
            except KeyError:
                send_msg = ivpo_setting2
                name_data = int(temp) * int(ivpo_data_list[send_msg][name][2])
                
            print(name_data)
            
            # 获取地址位
            addr = ivpo_data_list[send_msg][name][3]
            send_setting_txt = f'{send_msg[:2]}06{addr}{name_data:04X}'
            # 组合成发送的地址
            self.ivpo_setting_dic[name] = f'{send_setting_txt}{calc_crc(send_setting_txt)}'
            print(self.ivpo_setting_dic[name])
            
    # 参数设置-写入数据
    def ivpo_write_data_func(self):
        if len(self.ivpo_setting_dic) != 0:
            self.ivpo_timer_txt = []
            for k,v in self.ivpo_setting_dic.items():
                self.ivpo_timer_txt.append(v)
            self.ivpo_send_setting_timer = QtCore.QTimer()
            self.ivpo_send_setting_timer_step = 0
            self.ivpo_send_setting_timer.timeout.connect(self.ivpo_send_setting_timer_func)
            self.ivpo_send_setting_timer.start(1000)
        else:
            return QtWidgets.QMessageBox.critical(self, 'Error', '请先修改参数', QtWidgets.QMessageBox.Ok)
        print(self.ivpo_setting_dic)
    
    # 写入参数定时器
    def ivpo_send_setting_timer_func(self):
        if self.ivpo_send_setting_timer_step < len(self.ivpo_timer_txt):
            self.ivpo_send_msg(self.ivpo_timer_txt[self.ivpo_send_setting_timer_step])
            self.ivpo_send_setting_timer_step += 1
            self.ivpo_write_data.setEnabled(False)
        else:
            self.ivpo_send_setting_timer.stop()
            self.ivpo_write_data.setEnabled(True)
            return QtWidgets.QMessageBox.about(self, 'Tips', '数据已写入，请重新获取数据.')
            
    # 参数设置-读取数据
    def ivpo_read_data_func(self):
        if self.ivpo_port_switch == False:
            return QtWidgets.QMessageBox.information(self, 'tips', '串口未打开', QtWidgets.QMessageBox.Ok)
        
        # 记录实时监控是否在运行
        self.monit_status = True
        
        # 存储修改过的参数
        self.ivpo_setting_dic = {}
        
        # 创建定时器
        self.ivpo_timer_get_setting = QtCore.QTimer()
        self.ivpo_timer_get_setting.timeout.connect(self.ivpo_timer_get_setting_func)
        self.ivpo_timer_get_setting_step = 1
        self.ivpo_timer_get_setting.start(1000)
    
    # 参数设置-读取数据-定时器
    def ivpo_timer_get_setting_func(self):
        if self.ivpo_timer_get_setting_step == 1:
            # 如果监控已开启，则先停止，然后获取参数数据，获取完成后再启动监控
            try:
                if self.ivpo_timer_get_monitor.isActive():
                    self.ivpo_timer_get_monitor.stop()
                    self.monit_status = False
            except Exception as e:
                print(e)
        elif self.ivpo_timer_get_setting_step == 2:
            self.ivpo_send_msg(ivpo_setting1 + calc_crc(ivpo_setting1))
        else:
            self.ivpo_send_msg(ivpo_setting2 + calc_crc(ivpo_setting2))
            self.ivpo_timer_get_setting.stop()
            if self.monit_status == False:
                self.monit_status = True
                self.ivpo_timer_get_monitor.start(1500)
            self.ivpo_write_data.setEnabled(True)
            return QtWidgets.QMessageBox.about(self, 'Tips', '读取完成')
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
            self.ivpo_timer_get_monitor.start(int(self.ivpo_send_time.text()))
            
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

        # 统计收发数据总数
        if status == 'send':
            self.ivpo_send_data_count += 1
            self.ivpo_send_sum.setText(str(self.ivpo_send_data_count))
        else:
            self.ivpo_recv_data_count += 1
            self.ivpo_receive_sum.setText(str(self.ivpo_recv_data_count))
        
        # 写入日志文件
        with open(log_name, 'a+', encoding='utf-8') as f:
            f.write(f'{now}\t{status}\t{hexdata}\n')
        
        # 添加数据
        tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(hexdata))
        # 滚动条滚动到最下方
        tableWidget.verticalScrollBar().setSliderPosition(tableWidget.rowCount())

    # 清空表格
    def ivpo_clearRow_btn(self, tableWidget):
        
        # 收发总数归零
        self.ivpo_send_data_count = 0
        self.ivpo_recv_data_count = 0
        self.ivpo_send_sum.setText('')
        self.ivpo_receive_sum.setText('')
        
        rowPosition = tableWidget.rowCount()
        for rows in range(rowPosition)[::-1]:
            tableWidget.removeRow(rows)
    
    # 发送数据
    def ivpo_send_msg(self, data: str):
        hex_data = bytes.fromhex(data)
        try:
            self.invt_po_ser.write(hex_data)
        except Exception as e:
            self.invt_po_ser.close()
            print(e)
            return False
        # 在表格中输出
        self.ivpo_add_tableItem('send', bytes.hex(hex_data), self.ivpo_port_tableWidget, self.log_name)
    
    # 接收数据定时器
    def ivpo_timer_recevice_func(self):
        
        try:
            # res = self.invt_po_ser.readline()
            res = self.invt_po_ser.read_all()
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
                    temp1 = result['系统最高支持电压']
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
            
                self.pd_csv += f'{temp1},{temp2},{temp3},{temp4},{temp5},{temp6},{temp7},{temp8},{arg[1]}\n'
            
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
            
                self.ct_csv += f'{temp1},{temp2},{temp3},{arg[1]}\n'
            
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
                    self.ivpo_add_tableItem('receive', res, self.ivpo_port_tableWidget, self.log_name)
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

                self.iv_csv += f'{temp1},{temp2},{temp3},{temp4},{temp5},{temp6},{temp7},{temp8},{temp9},{temp10},{temp11},{temp12},{temp13},{temp14},{temp15},{temp16},{arg[1]}\n'
                
            # 用户设置区1
            elif res[:6] == f'{ivpo_setting1[:4]}40' and len(res) == 138:
                arg = ivpo_data_analysis(res, ivpo_setting1)
                result = arg[0]
                
                try:
                    temp1 = float(result['充电电流设置(A)'])
                    temp2 = int(result['蓄电池类型'])
                    temp3 = float(result['超压电压(V)'])
                    temp4 = float(result['充电限制电压(V)'])
                    temp5 = float(result['均衡充电电压(V)'])
                    temp6 = float(result['提升充电电压(V)'])
                    temp7 = float(result['浮充充电电压(V)'])
                    temp8 = float(result['提升充电返回电压(V)'])
                    temp9 = float(result['过放返回电压(V)'])
                    temp10 = float(result['过放电压(V)'])
                    temp11 = int(result['提升充电时间(Min)'])
                    temp12 = int(result['均衡充电间隔(day)'])
                    temp13 = int(result['温度补偿系数(mV/℃/2V)'])
                    temp14 = int(result['电池充电下限温度(℃)'])
                    temp15 = int(result['充满截止电流(A)'])
                    temp16 = int(result['铅酸激活'])
                    temp17 = int(result['锂电池低温充电(℃)'])
                    temp18 = int(result['接地继电器'])
                except Exception:
                    self.ivpo_add_tableItem('receive', res, self.ivpo_port_tableWidget, self.log_name)
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)  
                
                print(result)
                
                # 阻止信号发送的对象
                for obj in self.ivpo_setting_edit:
                    obj.blockSignals(True)
                
                self.ivpo_char_cur_set.setValue(temp1)
                self.ivpo_bat_type.setCurrentIndex(temp2)
                self.ivpo_over_vol.setValue(temp3)
                self.ivpo_char_limit_vol.setValue(temp4)
                self.ivpo_eq_char_vol.setValue(temp5)
                self.ivpo_boost_char_vol.setValue(temp6)
                self.ivpo_float_char_vol.setValue(temp7)
                self.ivpo_inchar_rerturn_vol.setValue(temp8)
                self.ivpo_op_returnvol.setValue(temp9)
                self.ivpo_odc_vol.setValue(temp10)
                self.ivpo_boost_char_time.setValue(temp11)
                self.ivpo_eq_char_interval.setValue(temp12)
                self.ivpo_tmp_comp_coe.setValue(temp13)
                self.ivpo_bat_char_low_tmp.setValue(temp14)
                self.ivpo_full_stop_cur.setValue(temp15)
                self.ivpo_lead_active.setCurrentIndex(temp16)
                self.ivpo_libat_low_tmp_char.setCurrentIndex(temp17)
                self.ivpo_relay_out_func.setCurrentIndex(temp18)
                
                for obj in self.ivpo_setting_edit:
                    obj.blockSignals(False)
                
            # 用户设置区2
            elif res[:6] == f'{ivpo_setting2[:4]}26' and len(res) == 86:
                arg = ivpo_data_analysis(res, ivpo_setting2)
                result = arg[0]
                
                try:
                    temp1 = int(result['输出优先级'])
                    temp2 = int(result['风扇启动温度(℃)'])
                    temp3 = int(result['ECO启动功率(W)'])
                    temp4 = int(result['交流输出电压(V)'])
                    temp5 = int(result['交流输出频率(Hz)'])
                    temp6 = int(result['ECO启动时间(S)'])
                    temp7 = int(result['逆变状态模式'])
                    temp8 = int(result['蜂鸣器设置'])
                    temp9 = int(result['输出切换电压(V)'])
                    temp10 = int(result['AC输入电流设置(A)'])
                except Exception:
                    self.ivpo_add_tableItem('receive', res, self.ivpo_port_tableWidget, self.log_name)
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)  
                
                print(result)
                
                # 阻止信号发送的对象
                for obj in self.ivpo_setting_edit:
                    obj.blockSignals(True)
                
                self.ivpo_out_pri.setCurrentIndex(temp1)
                self.ivpo_fan_start_tmp.setValue(temp2)
                self.ivpo_eco_start_power.setValue(temp3)
                self.ivpo_acout_vol.setValue(temp4)
                self.ivpo_acout_fre_2.setValue(temp5)
                self.ivpo_eco_start_time.setValue(temp6)
                self.ivpo_inv_state_mode.setCurrentIndex(temp7)
                self.ivpo_buzz_set.setCurrentIndex(temp8)
                self.ivpo_out_switch_vol.setValue(temp9)
                self.inpo_acinput_cur_set.setValue(temp10)

                for obj in self.ivpo_setting_edit:
                    obj.blockSignals(False)
            
            # 数据校准
            elif res[2:4] == '70':
                if res[10:12] == '01':
                    QtWidgets.QMessageBox.information(self, 'tips', '校准成功。', QtWidgets.QMessageBox.Ok)
                else:
                    QtWidgets.QMessageBox.information(self, 'tips', '校准失败。', QtWidgets.QMessageBox.Ok)
            self.ivpo_add_tableItem('receive', res, self.ivpo_port_tableWidget, self.log_name)
