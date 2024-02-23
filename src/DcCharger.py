import serial, functools, gettext, datetime, os
from ui.dc_layout import Ui_MainWindow as dc_layout
from .OrderList import *
from utils.Common import Common
from utils.CRC16Util import calc_crc
from .dataAnalysis.DcCharge_DA import dc_data_analysis
from settings.dc_modbus import dc_data_list

from PyQt5 import QtWidgets, QtCore


class DCLayout(QtWidgets.QMainWindow, dc_layout):
    
    def __init__(self):
        super(DCLayout, self).__init__()

        self.setupUi(self)
        self.dc_layout_init()
        # self.dc_i18n_init()
        self.setWindowTitle(f'{self.windowTitle()} v0.0.2')
    
    # 初始化
    def dc_layout_init(self):
        
        self.dc_open_port.setStyleSheet(color_close)
        self.dc_open_monitor.setStyleSheet(color_close)
        
        # 加载日志目录
        self.log_name = Common.creat_log_file('log')
        
        # 获取系统电压
        self.sys_vol_power = 2
        
        # 加载串口对象
        self.dccharger_ser = serial.Serial()
        
        # 加载串口列表
        self.dc_port_list.addItems(Common.load_serial_list())
        
        # 加载电池类型
        self.dc_set_battery_type.addItems(['自定义', '开口(FLD)', '密封(SLD)', '胶体(GEL)', '锂电池(LI)'])
        
        # 加载充电模式
        self.dc_ChgMode.addItems(['充电模式', '电源模式'])
        
        # 加载波特率列表
        self.dc_baud_list.addItems(['9600', '19200', '57600', '115200'])
        
        # 创建监控日志文件
        self.dc_now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        self.dc_pd_csv = ''
        self.dc_ct_csv = ''
        
        # 加载-实时监控信号槽
        self.dc_monitor_slots()
        
        # 参数设置框的对象
        self.dc_setting_edit = [
            self.dc_charge_elec_set,
            self.dc_set_battery_cap,
            # self.dc_set_sys_current,
            self.dc_set_battery_type,   # 蓄电池类型
            self.dc_set_battery_overpressure,
            self.dc_set_charge_limit,
            self.dc_set_even_current,
            self.dc_set_promote_current,
            self.dc_set_float_current,
            self.dc_set_promote_current_retrun,
            self.dc_BatUnderVolt,
            self.dc_BatConstChgTime,
            self.dc_BatImprovChgTime,
            self.dc_BatConstChgGapTime,
            self.dc_ChgMode,            # 充电模式
            self.dc_ChgModeInMaxWorkVolt,
            self.dc_ChgModeInLowWorkVolt,
            self.dc_CvModeOutVolt,
            self.dc_CvModeInMaxWorkVolt,
            self.dc_CVModeInLowWorkVolt
        ]
        
        # 存储修改过的参数
        self.dc_setting_dic = {}
        
        # 加载-参数设置信号槽
        self.dc_setting_slots()
        
        # 隐藏行序号
        self.dc_tableWidget.verticalHeader().setVisible(False)
        
        # 设置串口数据单元格的长度
        self.dc_tableWidget.setColumnWidth(0,180)
        self.dc_tableWidget.setColumnWidth(1,100)
        self.dc_tableWidget.setColumnWidth(2,760)

    # 参数设置信号槽
    def dc_setting_slots(self):
        self.dc_read_set.clicked.connect(self.dc_read_set_func)
        self.dc_write_set.clicked.connect(self.dc_write_set_func)
        
        for s in self.dc_setting_edit:
            try:
                s.currentIndexChanged.connect(functools.partial(self.dc_setting_edit_func, s))
            except Exception:
                s.valueChanged.connect(functools.partial(self.dc_setting_edit_func, s))

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
    
    # 参数设置-读取数据
    def dc_read_set_func(self):
        # 存储修改过的参数
        self.dc_setting_dic = {}
        
        self.dc_send_msg(dc_setting + calc_crc(dc_setting))
    
    # 参数设置-写入数据
    def dc_write_set_func(self):
        if len(self.dc_setting_dic) != 0:
            self.dc_timer_txt = []
            for k,v in self.dc_setting_dic.items():
                print(k, v)
                self.dc_timer_txt.append(v)
            self.dc_send_setting_timer = QtCore.QTimer()
            self.dc_send_setting_timer_step = 0
            self.dc_send_setting_timer.timeout.connect(self.dc_send_setting_timer_func)
            self.dc_send_setting_timer.start(1000)
        else:
            return QtWidgets.QMessageBox.critical(self, 'Error', '请先修改参数', QtWidgets.QMessageBox.Ok)
        
    # 写入参数定时器
    def dc_send_setting_timer_func(self):
        if self.dc_send_setting_timer_step < len(self.dc_timer_txt):
            self.dc_send_msg(self.dc_timer_txt[self.dc_send_setting_timer_step])
            self.dc_send_setting_timer_step += 1
            self.dc_write_set.setEnabled(False)
        else:
            self.dc_send_setting_timer.stop()
            self.dc_write_set.setEnabled(True)
            return QtWidgets.QMessageBox.about(self, 'Tips', '数据已写入，请重新获取数据.')
        
    # 参数设置-获取修改过的参数
    def dc_setting_edit_func(self, set_obj):
        try:
            temp = set_obj.value()
        except AttributeError:
            curr_text = set_obj.currentText()
            temp = set_obj.findText(curr_text)
        
        if temp != '':
            name = set_obj.whatsThis()[22:-18]
            data = int(temp) * int(dc_data_list[dc_setting][name][2])
            print(data)
            
            if name == '超压电压(V)' or name == '充电限制电压(V)' or name == '均衡充电电压(V)' \
                or name == '提升充电电压(V)' or name == '浮充充电电压(V)' or name == '提升充电返回电压(V)' \
                    or name == '欠压警告电压(V)':
                data = int((data / self.sys_vol_power) * 10)
                print(data)

            # 获取地址位
            addr = dc_data_list[dc_setting][name][3]
            send_setting_txt = f'{dc_setting[:2]}06{addr}{data:04X}'
            # 组合成发送的地址
            self.dc_setting_dic[name] = f'{send_setting_txt}{calc_crc(send_setting_txt)}'
            # print(self.dc_setting_dic[name])
    
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
            self.dc_timer_recevice = QtCore.QTimer()
            self.dc_timer_recevice.timeout.connect(self.dc_timer_recevice_func)
            self.dc_timer_recevice.start(500)
        else:
            try:
                self.dccharger_ser.close()
                self.dc_timer_recevice.stop()
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
        self.dc_timer_get_monitor = QtCore.QTimer()
        if self.dc_open_monitor.text() == '开启监控':
            self.dc_open_monitor.setText('关闭监控')
            self.dc_open_monitor.setStyleSheet(color_open)
            
            self.dc_timer_get_monitor.timeout.connect(self.dc_timer_get_monitor_func)
            self.dc_timer_get_monitor_step = 1
            self.dc_timer_get_monitor.start(1500)
            
        else:
            self.dc_open_monitor.setText('开启监控')
            self.dc_open_monitor.setStyleSheet(color_close)
            self.dc_timer_get_monitor.stop()
    
    # 开启监控-定时器
    def dc_timer_get_monitor_func(self):
        if self.dc_timer_get_monitor_step == 1:
            self.dc_send_msg(dc_product_monitor + calc_crc(dc_product_monitor))
        elif self.dc_timer_get_monitor_step == 2:
            self.dc_send_msg(dc_control_monitor + calc_crc(dc_control_monitor))
            self.dc_timer_get_monitor_step = 1
            return 0
        self.dc_timer_get_monitor_step += 1
     
    # 导出监控数据
    def dc_export_monitor_func(self):
        # 创建监控日志
        log_monitor_dir = os.path.join('log', f'dc_monitor_{self.dc_now}')
        log_monitor_product_name = os.path.join(log_monitor_dir, f'product_{self.dc_now}.csv')
        log_monitor_control_name = os.path.join(log_monitor_dir, f'control_{self.dc_now}.csv')
        
        if os.path.exists(log_monitor_dir) == False:
            os.makedirs(log_monitor_dir)
            
        if os.path.exists(log_monitor_product_name) == False:
            with open(log_monitor_product_name, 'w') as f:
                pd_txt = '系统电压,额定充电电流,产品类型,产品规格,软件版本,硬件版本,产品序列号,设备地址,CAN程序版本,设备名字,原始数据(Hex)'
                f.write(pd_txt + '\n')
        
        if os.path.exists(log_monitor_control_name) == False:
            with open(log_monitor_control_name, 'w') as f:
                ct_txt = '蓄电池电压,充电电流,设备温度,蓄电池温度,输入电压,充电功率,输出端开机以来最低电压,输出端开机以来最高电压,开机以来充电最大电流,当天充电安时数,当天发电量,总运行天数,蓄电池总充满次数,蓄电池总充电安时数,累计发电量,充电状态,控制器/告警信息1,原始数据(Hex)'
                f.write(ct_txt + '\n')
        
        # 写入监控日志
        try:
            with open(log_monitor_product_name, 'a') as f:
                f.write(self.dc_pd_csv)
            with open(log_monitor_control_name, 'a') as f:
                f.write(self.dc_ct_csv)
        except PermissionError:
            return QtWidgets.QMessageBox.critical(self, 'Error', '文件被占用，请关闭Excel文件后重试.', QtWidgets.QMessageBox.Ok)  
        except Exception as e:
            return QtWidgets.QMessageBox.critical(self, 'Error', f'{e}\n未知错误，请联系相关开发人员.', QtWidgets.QMessageBox.Ok)  
        
        # 是否需要主动打开目录
        open_dir =os.path.join(os.getcwd(), log_monitor_dir)
        if QtWidgets.QMessageBox.question(self, 'Tips', f'导出成功，目录位置为：{open_dir}\n是否需要打开该目录?', 
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            os.startfile(open_dir)
        
    # 开关机
    def dc_onoff_power_func(self):
        if self.dc_onoff_power.text() == '开机':
            self.dc_send_msg(dc_sw_on + calc_crc(dc_sw_on))
            self.dc_onoff_power.setText('关机')
            self.dc_onoff_power.setStyleSheet(color_open)
        else:
            self.dc_send_msg(dc_sw_off + calc_crc(dc_sw_off))
            self.dc_onoff_power.setText('开机')
            self.dc_onoff_power.setStyleSheet(color_close)
        
    # 复位
    def dc_reset_func(self):
        self.dc_send_msg(dc_device_reset + calc_crc(dc_device_reset))
        
    # 恢复出厂
    def dc_factory_setting_func(self):
        self.dc_send_msg(dc_fact_reset + calc_crc(dc_fact_reset))
        
    # 清除当前告警
    def dc_clear_alarm_func(self):
        self.dc_send_msg(dc_cl_alarm + calc_crc(dc_cl_alarm))
        
    # 清除统计量
    def dc_clear_statistic_func(self):
        self.dc_send_msg(dc_cl_statistic + calc_crc(dc_cl_statistic))

    # 清除历史记录
    def dc_clear_his_func(self):
        self.dc_send_msg(dc_cl_history + calc_crc(dc_cl_history))
        
    # 发送数据
    def dc_send_msg(self, data: str):
        hex_data = bytes.fromhex(data)
        try:
            self.dccharger_ser.write(hex_data)
        except serial.serialutil.PortNotOpenError as e:
            self.dccharger_ser.close()
            print(e)
            return False
        self.dc_add_tableItem('send', bytes.hex(hex_data), self.dc_tableWidget, self.log_name)
        
    # 增加一行数据收发
    def dc_add_tableItem(self, status: str, hexdata: str, tableWidget: QtWidgets.QTabWidget, log_name):
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

    # 接收数据的定时器
    def dc_timer_recevice_func(self):
        try:
            res = self.dccharger_ser.readline()
            res = res.hex()
        except Exception as e:
            print(e)
            return False
        
        if res != '':
            # 实时监控-产品信息区域
            if res[:6] == f'{dc_product_monitor[:4]}be' and len(res) == 390:
                arg = dc_data_analysis(res, dc_product_monitor)
                result = arg[0]
            
                # 异常后打印问题字段，防止程序崩溃
                try:
                    temp1 = result['系统电压']
                    self.sys_vol_power = int(int(temp1) / 12)   # 12=1,24=2,48=4
                    
                    temp2 = result['额定充电电流']
                    temp3 = result['产品类型']
                    temp4 = result['产品规格']
                    temp5 = result['软件版本']
                    temp6 = result['硬件版本']
                    temp7 = result['产品序列号']
                    temp8 = result['设备地址']
                    temp9 = result['CAN程序版本']
                    temp10 = result['设备名字']
                except Exception as e:
                    self.dc_add_tableItem('receive', res, self.dc_tableWidget, self.log_name)
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)  
                
                self.dc_sys_vol.setText(temp1)
                self.dc_rate_charg_cur.setText(temp2)
                self.dc_product_type.setText(temp3)
                self.dc_product_spec.setText(temp4)
                self.dc_software_ver.setText(temp5)
                self.dc_hardware_ver.setText(temp6)
                self.dc_product_sn.setText(temp7)
                self.dc_dev_addr.setText(temp8)
                self.dc_can_ver.setText(temp9)
                self.dc_dev_name.setText(temp10)
                
                self.dc_pd_csv += f'{temp1},{temp2},{temp3},{temp4},{temp5},{temp6},{temp7},{temp8},{temp9},{temp10},{arg[1]}\n'
                
            # 实时监控-控制器区域
            elif res[:6] == f'{dc_control_monitor[:4]}56' and len(res) == 182:
                arg = dc_data_analysis(res, dc_control_monitor)
                result = arg[0]

                try:
                    temp1 = result['蓄电池电压']
                    temp2 = result['充电电流']
                    temp3 = result['设备温度']
                    temp4 = result['蓄电池温度']
                    temp5 = result['输入电压']
                    temp6 = result['充电功率']
                    temp7 = result['输出端开机以来最低电压']
                    temp8 = result['输出端开机以来最高电压']
                    temp9 = result['开机以来充电最大电流']
                    temp10 = result['当天充电安时数']
                    temp11 = result['当天发电量']
                    temp12 = result['总运行天数']
                    temp13 = result['蓄电池总充满次数']
                    temp14 = result['蓄电池总充电安时数']
                    temp15 = result['累计发电量']
                    temp16 = result['充电状态']
                    temp17 = result['控制器故障/告警信息1']
                    # temp18 = result['Mos管温度']
                    # temp19 = result['散热器']
                except Exception as e:
                    self.dc_add_tableItem('receive', res, self.dc_tableWidget, self.log_name)
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)  
                
                self.dc_bat_vol.setText(temp1)
                self.dc_charge_curr.setText(temp2)
                self.dc_dev_tmp.setText(temp3)
                self.dc_bat_tmp.setText(temp4)
                self.dc_input_vol.setText(temp5)
                self.dc_charge_power.setText(temp6)
                self.dc_open_min_vol.setText(temp7)
                self.dc_open_max_vol.setText(temp8)
                self.dc_open_max_chg_curr.setText(temp9)
                self.dc_today_chgAH.setText(temp10)
                self.dc_today_genera.setText(temp11)
                self.dc_total_work_day.setText(temp12)
                self.dc_bat_overchg_times.setText(temp13)
                self.dc_total_bat_chgAH.setText(temp14)
                self.dc_total_genera.setText(temp15)
                self.dc_chg_state.setText(temp16)
                self.dc_fail_info.setText(temp17)
                # self.dc_mos_tmp.setText(temp18)
                # self.dc_radiator.setText(temp19)
                
                self.dc_ct_csv += f'{temp1},{temp2},{temp3},{temp4},{temp5},{temp6},{temp7},{temp8},{temp9},{temp10},{temp11},{temp12},{temp13},{temp14},{temp15},{temp16},{temp17},{arg[1]}\n'
            
            # 参数设置区域
            elif res[:6] == f'{dc_setting[:4]}74' and len(res) == 242:
                arg = dc_data_analysis(res, dc_setting)
                result = arg[0]
                
                try:
                    temp1 = float(result['充电电流设置(A)'])
                    temp2 = int(result['蓄电池标称容量(AH)'])
                    temp3 = int(result['系统电压设置(V)'])
                    temp4 = int(result['蓄电池类型'])
                    temp5 = float(result['超压电压(V)']) * self.sys_vol_power
                    temp6 = float(result['充电限制电压(V)']) * self.sys_vol_power
                    temp7 = float(result['均衡充电电压(V)']) * self.sys_vol_power
                    temp8 = float(result['提升充电电压(V)']) * self.sys_vol_power
                    temp9 = float(result['浮充充电电压(V)']) * self.sys_vol_power
                    temp10 = float(result['提升充电返回电压(V)']) * self.sys_vol_power
                    temp11 = float(result['欠压警告电压(V)']) * self.sys_vol_power
                    temp12 = int(result['均衡充电时间(Min)'])
                    temp13 = int(result['提升充电时间(Min)'])
                    temp14 = int(result['均衡充电间隔(day)'])
                    temp15 = int(result['充电模式'])
                    temp16 = float(result['充电模式高于此电压充电(V)'])
                    temp17 = float(result['充电模式低于此电压停冲(V)'])
                    temp18 = float(result['电源模式的输出电压(V)'])
                    temp19 = float(result['电源模式高于此电压充电(V)'])
                    temp20 = float(result['电源模式低于此电压停冲(V)'])
                    temp21 = int(result['充满截止电流(A)'])
                    temp22 = int(result['充满截止延时(s)'])
                except Exception as e:
                    self.dc_add_tableItem('receive', res, self.dc_tableWidget, self.log_name)
                    return QtWidgets.QMessageBox.critical(self, 'Error', str(e), QtWidgets.QMessageBox.Ok)
                
                if temp15 == 0: # 充电模式
                    
                    # 默认开启
                    self.dc_set_battery_type.setEnabled(True)       # 蓄电池类型
                    self.dc_set_battery_cap.setEnabled(True)        # 标称容量
                    self.dc_set_sys_current.setEnabled(True)        # 系统电压
                    self.dc_ChgModeInMaxWorkVolt.setEnabled(True)   # 充电模式启动电压
                    self.dc_ChgModeInLowWorkVolt.setEnabled(True)   # 充电模式停止电压
                    
                    self.dc_CvModeInMaxWorkVolt.setEnabled(False)   # 电源模式启动电压
                    self.dc_CVModeInLowWorkVolt.setEnabled(False)   # 电源模式停止电压
                    self.dc_CvModeOutVolt.setEnabled(False)         # 电源模式输出电压
                    
                    if temp4 == 0:  # 自定义
                        self.dc_charge_elec_set.setEnabled(True)            # 最大充电电流
                        self.dc_set_battery_overpressure.setEnabled(True)   # 超压电压
                        self.dc_set_charge_limit.setEnabled(True)           # 充电限制电压
                        self.dc_set_even_current.setEnabled(True)           # 均衡充电电压
                        self.dc_set_promote_current.setEnabled(True)        # 提升充电电压
                        self.dc_set_float_current.setEnabled(True)          #浮充充电电压
                        self.dc_set_promote_current_retrun.setEnabled(True) # 提升充电返回电压
                        self.dc_BatConstChgTime.setEnabled(True)            # 均衡充电时间
                        self.dc_BatImprovChgTime.setEnabled(True)           # 提升充电时间
                        self.dc_BatConstChgGapTime.setEnabled(True)         # 均衡充电间隔
                        self.dc_BatUnderVolt.setEnabled(True)               # 欠压警告电压
                        self.dc_StopChgDelayTim.setEnabled(True)            # 充满截止延时
                        self.dc_StopChgCurrSet.setEnabled(True)             # 充满截止电流
                        
                    elif temp4 == 4:    # 锂电池
                        self.dc_charge_elec_set.setEnabled(True)            # 最大充电电流
                        self.dc_set_battery_overpressure.setEnabled(False)   # 超压电压
                        self.dc_set_charge_limit.setEnabled(False)           # 充电限制电压
                        self.dc_set_even_current.setEnabled(False)           # 均衡充电电压
                        self.dc_set_promote_current.setEnabled(True)        # 提升充电电压
                        self.dc_set_float_current.setEnabled(False)          #浮充充电电压
                        self.dc_set_promote_current_retrun.setEnabled(True) # 提升充电返回电压
                        self.dc_BatConstChgTime.setEnabled(False)            # 均衡充电时间
                        self.dc_BatImprovChgTime.setEnabled(False)           # 提升充电时间
                        self.dc_BatConstChgGapTime.setEnabled(False)         # 均衡充电间隔
                        self.dc_BatUnderVolt.setEnabled(True)               # 欠压警告电压
                        self.dc_StopChgDelayTim.setEnabled(True)            # 充满截止延时
                        self.dc_StopChgCurrSet.setEnabled(True)             # 充满截止电流
                        
                    else:   # 其他类型
                        self.dc_charge_elec_set.setEnabled(True)            # 最大充电电流
                        self.dc_set_battery_overpressure.setEnabled(False)   # 超压电压
                        self.dc_set_charge_limit.setEnabled(False)           # 充电限制电压
                        self.dc_set_even_current.setEnabled(False)           # 均衡充电电压
                        self.dc_set_promote_current.setEnabled(False)        # 提升充电电压
                        self.dc_set_float_current.setEnabled(False)          #浮充充电电压
                        self.dc_set_promote_current_retrun.setEnabled(False) # 提升充电返回电压
                        self.dc_BatConstChgTime.setEnabled(False)            # 均衡充电时间
                        self.dc_BatImprovChgTime.setEnabled(False)           # 提升充电时间
                        self.dc_BatConstChgGapTime.setEnabled(False)         # 均衡充电间隔
                        self.dc_BatUnderVolt.setEnabled(False)               # 欠压警告电压
                        self.dc_StopChgDelayTim.setEnabled(True)            # 充满截止延时
                        self.dc_StopChgCurrSet.setEnabled(True)             # 充满截止电流
                    
                elif temp15 == 1:   # 电源模式
                    self.dc_charge_elec_set.setEnabled(True)
                    self.dc_CvModeOutVolt.setEnabled(True)
                    self.dc_CvModeInMaxWorkVolt.setEnabled(True)
                    self.dc_CVModeInLowWorkVolt.setEnabled(True)
                    
                    self.dc_set_battery_cap.setEnabled(False)
                    self.dc_set_sys_current.setEnabled(False)
                    self.dc_set_battery_type.setEnabled(False)
                    self.dc_set_battery_overpressure.setEnabled(False)
                    self.dc_set_charge_limit.setEnabled(False)
                    self.dc_set_even_current.setEnabled(False)
                    self.dc_set_promote_current.setEnabled(False)
                    self.dc_set_float_current.setEnabled(False)
                    self.dc_set_promote_current_retrun.setEnabled(False)
                    self.dc_BatUnderVolt.setEnabled(False)
                    self.dc_BatConstChgTime.setEnabled(False)
                    self.dc_BatImprovChgTime.setEnabled(False)
                    self.dc_BatConstChgGapTime.setEnabled(False)
                    self.dc_ChgModeInMaxWorkVolt.setEnabled(False)
                    self.dc_ChgModeInLowWorkVolt.setEnabled(False)
                    self.dc_StopChgDelayTim.setEnabled(False)
                    self.dc_StopChgCurrSet.setEnabled(False)
                
                # 阻止信号发送
                for obj in self.dc_setting_edit:
                    obj.blockSignals(True)
                
                self.dc_charge_elec_set.setValue(temp1)
                self.dc_set_battery_cap.setValue(temp2)
                self.dc_set_sys_current.setValue(temp3)
                self.dc_set_battery_type.setCurrentIndex(temp4)
                self.dc_set_battery_overpressure.setValue(temp5)
                self.dc_set_charge_limit.setValue(temp6)
                self.dc_set_even_current.setValue(temp7)
                self.dc_set_promote_current.setValue(temp8)
                self.dc_set_float_current.setValue(temp9)
                self.dc_set_promote_current_retrun.setValue(temp10)
                self.dc_BatUnderVolt.setValue(temp11)
                self.dc_BatConstChgTime.setValue(temp12)
                self.dc_BatImprovChgTime.setValue(temp13)
                self.dc_BatConstChgGapTime.setValue(temp14)
                self.dc_ChgMode.setCurrentIndex(temp15)
                self.dc_ChgModeInMaxWorkVolt.setValue(temp16)
                self.dc_ChgModeInLowWorkVolt.setValue(temp17)
                self.dc_CvModeOutVolt.setValue(temp18)
                self.dc_CvModeInMaxWorkVolt.setValue(temp19)
                self.dc_CVModeInLowWorkVolt.setValue(temp20)
                self.dc_StopChgCurrSet.setValue(temp21)
                self.dc_StopChgDelayTim.setValue(temp22)
                
                # 允许信号发送
                for obj in self.dc_setting_edit:
                    obj.blockSignals(False)
                
            self.dc_add_tableItem('receive', res, self.dc_tableWidget, self.log_name)