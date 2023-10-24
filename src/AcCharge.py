# -*- coding: utf-8 -*-

import serial, functools, datetime, os, gettext
from .OrderList import *
from utils.Common import Common
from settings.ac_modbus import get_ac_data_list
from utils.CRC16Util import calc_crc
from utils.DataPars import pars_data
from ui.ac_layout import Ui_MainWindow as ac_layout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings


class AcLayout(QtWidgets.QMainWindow, ac_layout):
    
    def __init__(self):
        super(AcLayout, self).__init__()
        self.setupUi(self)
        self.ac_layout_init()
        self.i18n_init()
        self.setWindowTitle(f'{self.windowTitle()} v0.0.5')
    
    # 加载国际化i18n
    def i18n_init(self):
        # 加载设置项，根据设置参数切换语言
        set_dir = os.path.join(os.getcwd(), 'settings', 'settings.ini')
        setting = QSettings(set_dir, QSettings.IniFormat)
        
        lang_zh = gettext.translation('AcCharge', localedir=os.path.join(os.getcwd(), 'locales'), languages=[setting.value('language')])
        lang_zh.install('AcCharge')
        _ = lang_zh.gettext
        # 串口相关
        self.open_port_i18n = _('打开串口')
        self.close_port_i18n = _('关闭串口')
        self.erro_port_i18n = _('打开串口失败')
        # 开/关监控相关
        self.open_monitor_i18n = _('开启数据监控')
        self.close_monitor_i18n = _('关闭数据监控')
        # 写入监控日志相关
        self.write_monitor1_i18n = _('产品类型,产品规格,产品序列号,设备名称,设备地址,硬件版本,软件版本,系统电压,额定充电电流,额定放电电流,原始数据(Hex)')
        self.write_monitor2_i18n = _('充电电流,设备温度,蓄电池电压,蓄电池温度,充电状态,故障/告警信息,原始数据(Hex)')
        # 错误提示相关
        self.file_occupy_error = _('文件被占用，请关闭Excel文件后重试.')
        self.file_unknow_error = _('未知错误，请截图并联系相关开发人员.')
        # 打开目录相关
        self.open_dir_txt1 = _('导出成功，目录位置为')
        self.open_dir_txt2 = _('是否需要打开该目录?')
        # 其他的一些提示
        self.stop_monitor_tips = _('为保准数据准确性，请在实时监控中停止数据监控，需要暂停吗?')
        self.write_data_tips = _('请输入参数')
        self.mdf_data_tips = _('请修改参数.')
        self.writing_data_tips = _('写入中...')
        self.write_param_tips = _('写入数据')
        self.sure_param_tips = _('是否要写入以下参数:')
        self.write_data_ok_tips = _('数据已写入，请重新获取数据.')
        self.port_nostart_tips = _('请先打开串口.')
        self.setting_tips = _('请输入正确的数值.')
    
    # 加载界面所需参数
    def ac_layout_init(self):
        
        # 暂时隐藏参数设置中的清屏按钮，目前无用
        self.clear_set_data.hide()
        
        # 初始化-实时监控
        self.ser = serial.Serial()
        self.port_btn.setStyleSheet(color_close)
        self.startMonitor_btn.setStyleSheet(color_close)
        self.ac_monitor_on = False
        
        
        # 加载-串口
        self.port_cmb.addItems(Common.load_serial_list())
        
        # 加载-实时监控信号槽
        self.ac_monitor_slots()
        
        # 初始化-参数设置
        self.setting_dic = {}
        # self.setting_show = {}
        
        # 接收框的内存地址
        self.setting_edit = [
            self.set_charge_elec,
            self.set_battery_type,
            self.set_even_current,
            self.set_store_current,
            self.set_balanced_space,
            self.set_full_stop,   # 充满截止电流
            self.set_battery_cap,
            self.set_battery_overpressure,
            self.set_promote_current,
            self.set_balanced_time,
            self.set_tp_redress,
            self.set_full_stop_delay,
            self.set_sys_current,
            self.set_charge_limit,
            self.set_float_current,
            self.set_promote_time,
            self.set_charge_floor_tp,
            self.set_zero_stop,    # 锂电池零度禁止充
            self.ac_chgmode,
            self.ac_powerMode_enable,
            self.ac_powerMode_outV,
            self.ac_powerMode_startV,
            self.ac_powerMode_stopV
        ]
        
        # 加载-参数设置信号槽
        self.ac_set_slots()
        
        # 初始化-实时数据
        self.ac_show_tab_data.setColumnWidth(0,180)
        self.ac_show_tab_data.setColumnWidth(1,100)
        self.ac_show_tab_data.setColumnWidth(2,765)
        
        # 创建日志目录
        if os.path.exists('log') == False:
            os.mkdir('log')
        
        # 创建日志文件
        self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        self.log_name = f'log/{self.now}.txt'
        
        # 创建监控日志文件
        self.m1_csv = ''
        self.m2_csv = ''
        
        # 加载-实时数据信号槽
        self.ac_nowData_slots()
    
    # 信号槽-实时监控
    def ac_monitor_slots(self):
        self.port_btn.clicked.connect(self.ac_openPort)
        self.ac_port_refresh.clicked.connect(self.ac_port_refresh_func)
        self.startMonitor_btn.clicked.connect(self.ac_get_monitor)
        self.switch_machine_btn.clicked.connect(self.ac_switch_onoff)
        self.prod_reset_btn.clicked.connect(self.ac_resetting)
        self.reset_default_btn.clicked.connect(self.ac_reset_factory)
        self.clear_history_btn.clicked.connect(self.ac_clear_history)
        self.clearMonitor.clicked.connect(self.ac_clear_monitor)
        self.ac_testmode_btn.clicked.connect(self.ac_testmode_func)
        
    # 信号槽-实时数据
    def ac_nowData_slots(self):
        self.ac_clear_tab_data.clicked.connect(functools.partial(self.clearRow_btn, self.ac_show_tab_data))
    
    # 信号槽-参数设置
    def ac_set_slots(self):
        self.read_set_data.clicked.connect(self.ac_read_data)
        self.write_set_data.clicked.connect(self.ac_write_data)
        self.clear_set_data.clicked.connect(self.ac_clear_data)
        self.ac_output_monitor.clicked.connect(self.ac_output_monitor_func)
        
        for s in self.setting_edit:
            try:
                s.currentIndexChanged.connect(functools.partial(self.setting_edit_func, s))
                # s.textEdited.connect(functools.partial(self.setting_edit_func, s))
            except AttributeError:
                s.valueChanged.connect(functools.partial(self.setting_edit_func, s))
                # s.valueChanged.connect(functools.partial(self.setting_edit_func, s))
                
    # 创建监控日志
    def ac_output_monitor_func(self):
        # 创建监控日志
        log_monitor_dir = f'log/monitor_{self.now}'
        log_monitor_m1_name = f'{log_monitor_dir}/m1_{self.now}.csv'
        log_monitor_m2_name = f'{log_monitor_dir}/m2_{self.now}.csv'
        if os.path.exists(log_monitor_dir) == False:
            os.makedirs(log_monitor_dir)
        if os.path.exists(log_monitor_m1_name) == False:
            with open(log_monitor_m1_name, 'w') as f:
                f.write(self.write_monitor1_i18n + '\n')
                # f.write('产品类型,产品规格,产品序列号,设备名称,设备地址,硬件版本,软件版本,系统电压,额定充电电流,额定放电电流,原始数据Hex\n')
        if os.path.exists(log_monitor_m2_name) == False:
            with open(log_monitor_m2_name, 'w') as f:
                f.write(self.write_monitor2_i18n + '\n')
                # f.write('充电电流,设备温度,蓄电池电压,蓄电池温度,充电状态,故障/告警信息,原始数据Hex\n')
        
        # 写入监控日志
        try:
            with open(log_monitor_m1_name, 'a') as f:
                f.write(self.m1_csv)
            with open(log_monitor_m2_name, 'a') as f:
                f.write(self.m2_csv)
        except PermissionError:
            return QtWidgets.QMessageBox.critical(self, 'Error', self.file_occupy_error, QtWidgets.QMessageBox.Ok)  
        except Exception as e:
            return QtWidgets.QMessageBox.critical(self, 'Error', f'{e}\n{self.file_unknow_error}', QtWidgets.QMessageBox.Ok)  
        
        # 是否需要主动打开目录
        open_dir =os.path.join(os.getcwd(), log_monitor_dir)
        if QtWidgets.QMessageBox.question(self, 'Tips', f'{self.open_dir_txt1}：{open_dir}\n{self.open_dir_txt2}', \
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            os.startfile(open_dir)
    
    # 发送数据
    def send_msg(self, data: str):
        hex_data = bytes.fromhex(data)
        try:
            self.ser.write(hex_data)
        except serial.serialutil.PortNotOpenError as e:
            self.ser.close()
            print(e)
            return False
        self.add_tableItem('send', bytes.hex(hex_data), self.ac_show_tab_data)    # 在表格中输出

    # 清空表格
    def clearRow_btn(self, tableWidget):
        rowPosition = tableWidget.rowCount()
        for rows in range(rowPosition)[::-1]:
            tableWidget.removeRow(rows)

    # 增加一行数据收发
    def add_tableItem(self, status: str, hexdata: str, tableWidget: QtWidgets.QTabWidget):
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
        with open(self.log_name, 'a+', encoding='utf-8') as f:
            f.write(f'{now}\t{status}\t{hexdata}\n')
        
        # 添加数据
        tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(hexdata))
        # 滚动条滚动到最下方
        tableWidget.verticalScrollBar().setSliderPosition(tableWidget.rowCount())

    # 定时器方法-写入参数
    def ac_send_setting_timer_func(self):
        if self.ac_send_setting_timer_step < len(self.setting_dic):
            self.send_msg(self.timer_txt[self.ac_send_setting_timer_step])
            self.ac_send_setting_timer_step += 1
            self.write_set_data.setText(self.writing_data_tips)
            self.write_set_data.setEnabled(False)
        else:
            self.ac_send_setting_timer.stop()
            self.write_set_data.setText(self.write_param_tips)
            self.write_set_data.setEnabled(True)
            return QtWidgets.QMessageBox.about(self, 'Tips', self.write_data_ok_tips)
    
    # 关闭实时监控定时器
    def ac_close_monitor(self):
        if self.ac_monitor_on:
            if QtWidgets.QMessageBox.information(self, 'Tips', self.stop_monitor_tips,
                # '为保证数据准确性，需要先停止实时监控中的数据监控，是否停止？', \
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
                self.timer_get_monitor.stop()
                self.ac_monitor_on = False
                self.startMonitor_btn.setText(self.open_monitor_i18n)
                self.startMonitor_btn.setStyleSheet(color_close)
                return True
            return False
        return True
    
    # 按钮-打开/关闭串口
    def ac_openPort(self):
        # if self.port_btn.text() == '打开串口':
        if self.port_btn.text() == self.open_port_i18n:
            self.ser.port = self.port_cmb.currentText()
            self.ser.timeout = 0.07
            self.ser.baudrate = int(self.baud_cmb.currentText())
            try:
                self.ser.open()
            except serial.SerialException:
                QtWidgets.QMessageBox.information(self, 'Error', self.erro_port_i18n, QtWidgets.QMessageBox.Ok)
                return self.ser.close()
            # self.port_btn.setText('关闭串口')
            self.port_btn.setText(self.close_port_i18n)
            self.port_btn.setStyleSheet(color_open)
            self.port_cmb.setEnabled(False)

            self.rate_charge_monitor = False
            # 定时器-开启接收数据
            self.timer_recevice = QtCore.QTimer()
            self.timer_recevice.timeout.connect(self.timer_recevice_func)
            self.timer_recevice.start(100)
        else:
            try:
                self.ser.close()
                self.timer_recevice.stop()
            except Exception as e:
                print(e)
            
            # self.port_btn.setText('打开串口')
            self.port_btn.setText(self.open_port_i18n)
            self.port_btn.setStyleSheet(color_close)
            self.port_cmb.setEnabled(True)
    
    # 按钮-刷新串口
    def ac_port_refresh_func(self):
        self.port_cmb.clear()
        self.port_cmb.addItems(Common.load_serial_list())
    
    # 提示语-串口未打开
    def ac_port_nostart_tips(self):
        if self.ser.isOpen() == False:
            QtWidgets.QMessageBox.critical(self, 'Error', self.port_nostart_tips, QtWidgets.QMessageBox.Ok)  
            return False
    
    # 按钮-开启/关闭数据监控
    def ac_get_monitor(self):
        self.timer_get_monitor = QtCore.QTimer()
        if self.startMonitor_btn.text() == self.open_monitor_i18n:
            if self.ac_port_nostart_tips() == False: return 0
            self.startMonitor_btn.setText(self.close_monitor_i18n)
            self.startMonitor_btn.setStyleSheet(color_open)
            self.ac_monitor_on = True
            self.ac_sys_vol_on = False    # 系统电压是否已获取
            
            # 定时器-开启数据监控
            self.timer_get_monitor.timeout.connect(self.timer_get_monitor_func)
            self.timer_get_monitor_step = 1
            self.timer_get_monitor.start(1500)
        else:
            self.startMonitor_btn.setText(self.open_monitor_i18n)
            self.startMonitor_btn.setStyleSheet(color_close)
            self.ac_monitor_on = False
            self.timer_get_monitor.stop()
    
    # 定时器方法-开启数据监控
    def timer_get_monitor_func(self):
        if self.timer_get_monitor_step == 1:
            # 发 实时监控数据1
            self.send_msg(f'{ac_monitor1}{calc_crc(ac_monitor1)}')
        elif self.timer_get_monitor_step == 2:
            # 发 实时监控数据2
            self.send_msg(f'{ac_monitor2}{calc_crc(ac_monitor2)}')
        elif self.timer_get_monitor_step == 3:
            # 发 开关机状态数据
            self.send_msg(f'{ac_get_chgstatus}{calc_crc(ac_get_chgstatus)}')
        else:
            # 发 测试模式状态数据
            self.send_msg(f'{ac_get_testmode}{calc_crc(ac_get_testmode)}')
            self.timer_get_monitor_step = 1
            return 0
        self.timer_get_monitor_step += 1

    # 接收数据定时器
    def timer_recevice_func(self):
        try:
            # res = self.ser.read_all()
            res = self.ser.readline()
            res = res.hex()
        except Exception as e:
            print(e)
            return False
        if res != '':
            # 实时监控1
            if res[:6] == f'{ac_monitor1[:4]}be' and len(res) == 390:
                arg = pars_data(res, ac_monitor1)
                result = arg[0]
                temp1 = result['产品类型']
                if temp1[:2] == 'DC':
                    self.ac_chgmode.setEnabled(True)
                else:
                    self.ac_chgmode.setEnabled(False)
                    
                temp2 = result['产品规格']
                temp3 = result['产品序列号']
                temp4 = result['设备名称']
                temp5 = result['设备地址']
                temp6 = result['硬件版本']
                temp7 = result['软件版本']
                
                """
                    从 12/24/48/AUTO(255) 里面取，
                    额定系统电压值如果是24，则显示12/24/AUTO;
                    12则只显示12，不显示AUTO;
                    电池类型为Li，系统电压不显示AUTO
                """
                temp8 = result['系统电压']
                if self.ac_sys_vol_on == False:
                    temp8_vol = ['12', '24', '48', 'AUTO']
                    num = temp8[:-2]
                    if num != '12':
                        # 清空下拉项会触发改变数值的信号，此处拦截信号
                        self.set_sys_current.blockSignals(True)
                        
                        # 下拉项的列表
                        temp8_vol_list = temp8_vol[:temp8_vol.index(num) + 1]
                        temp8_vol_list.append(temp8_vol[-1])
                        
                        self.set_sys_current.clear()
                        self.set_sys_current.addItems(temp8_vol_list)

                        # 下拉项内容添加完成，释放信号
                        self.set_sys_current.blockSignals(False)
                    else:
                        # 12则只显示12，不显示AUTO
                        self.set_sys_current.blockSignals(True)
                        self.set_sys_current.clear()
                        self.set_sys_current.addItem('12')
                        self.set_sys_current.blockSignals(False)
                        
                    # 系统电压设置下拉项添加完成，不再设置
                    self.ac_sys_vol_on = True
                    
                temp9 = result['额定充电电流']
                # 保存 额定充电电流，提供给 充满截止电流 使用
                # 充满截止电流可选范围最大值 为 额定充电电流 %40
                if self.rate_charge_monitor == False:
                    self.set_full_stop.setEnabled(True)
                    ls = [i for i in range(1, int(int(result['额定充电电流'][:-2]) * 0.4)+1)]
                    self.set_full_stop.addItems([str(i) for i in ls])
                    self.rate_charge_monitor = True
                
                # temp10 = result['额定放电电流']   # 不显示
                self.prod_type.setText(temp1)
                self.prod_spec.setText(temp2)
                self.prod_num.setText(temp3)
                self.prod_name.setText(temp4)
                self.prod_adder.setText(temp5)
                self.hard_ver.setText(temp6)
                self.soft_ver.setText(temp7)
                self.sys_current.setText(temp8)
                self.rate_charg_current.setText(temp9)
                # self.rate_discharg_current.setText(temp10)
                # 写入监控日志
                self.m1_csv += f'{temp1},{temp2},{temp3},{temp4},{temp5},{temp6},{temp7},{temp8},{temp9},{arg[1]}\n'
            # 实时监控2
            elif res[:6] == f'{ac_monitor2[:4]}46' and len(res) == 150:
                arg = pars_data(res, ac_monitor2)
                result = arg[0]
                temp1 = result['充电电流']
                temp2 = result['设备温度']
                temp3 = result['蓄电池电压']
                temp4 = result['蓄电池温度']
                temp5 = result['充电状态']
                temp6 = result['故障/告警信息']
                self.charg_current.setText(temp1)
                self.prod_tp.setText(temp2)
                self.battery_current.setText(temp3)
                self.battery_tp.setText(temp4)
                self.charge_status.setText(temp5)
                self.error_msg.setText(temp6)
                temp6 = temp6.replace('\n', ' | ')
                self.m2_csv += f'{temp1},{temp2},{temp3},{temp4},{temp5},{temp6},{arg[1]}\n'
            elif res[:6] == f'{ac_get_chgstatus[:4]}02' and self.timer_get_monitor_step == 4:
                arg = pars_data(res, ac_get_chgstatus)[0]['开关机']
                if arg == 1:
                    self.switch_machine_btn.setText('关闭')
                    self.switch_machine_btn.setStyleSheet(color_open)
                else:
                    self.switch_machine_btn.setText('开启')
                    self.switch_machine_btn.setStyleSheet(color_close)
            elif res[:6] == f'{ac_get_testmode[:4]}02' and self.timer_get_monitor_step == 1:
                arg = pars_data(res, ac_get_testmode)[0]['测试模式']
                if arg == 8888:
                    self.ac_testmode_btn.setText('关闭')
                    self.ac_testmode_btn.setStyleSheet(color_open)
                else:
                    self.ac_testmode_btn.setText('开启')
                    self.ac_testmode_btn.setStyleSheet(color_close)
            # 参数设置
            elif res[:6] == f'{ac_get_setting[:4]}74' and len(res) == 242:
                # 解析的数据
                arg = pars_data(res, ac_get_setting)
                result = arg[0]
                
                # 阻止信号发送的对象
                for obj in self.setting_edit:
                    obj.blockSignals(True)
                
                self.set_charge_elec.setValue(float(result['充电电流设置(A)']))
                self.set_battery_type.setCurrentIndex(int(result['蓄电池类型']))
                self.set_even_current.setValue(float(result['均衡充电电压(V)']))
                self.set_store_current.setValue(float(result['储存充电电压(V)']))
                self.set_balanced_space.setValue(int(result['均衡充电间隔(day)']))
                
                if self.rate_charge_monitor == True:
                    self.set_full_stop.setCurrentIndex(int(result['充满截止电流(A)']))
                
                self.set_battery_cap.setValue(int(result['蓄电池标称容量(AH)']))
                self.set_battery_overpressure.setValue(float(result['超压电压(V)']))
                self.set_promote_current.setValue(float(result['提升充电电压(V)']))
                self.set_balanced_time.setValue(int(result['均衡充电时间(min)']))
                self.set_tp_redress.setValue(int(result['温度补偿系数(mV/℃/2V)']))
                self.set_full_stop_delay.setValue(int(result['充满截止延时(S)']))
                
                if result['系统电压设置(V)'] == '255':
                    self.set_sys_current.setCurrentText('AUTO')
                else:
                    self.set_sys_current.setCurrentText(result['系统电压设置(V)'])
                
                self.set_charge_limit.setValue(float(result['充电限制电压(V)']))
                self.set_float_current.setValue(float(result['浮充充电电压(V)']))
                self.set_promote_time.setValue(int(result['提升充电时间(min)']))
                self.set_charge_floor_tp.setValue(int(result['电池充电下限温度(℃)']))
                self.set_zero_stop.setCurrentIndex(int(int(result['锂电池零度禁止充'])))
                if int(result['充电模式']) == 1:
                    # 当设备类型为 DC-DC充电器,充电模式才能操作；当启动电源模式时，电源模式相关数据才能更改
                    self.ac_powerMode_enable.setEnabled(True)
                    self.ac_powerMode_outV.setReadOnly(False)
                    self.ac_powerMode_startV.setReadOnly(False)
                    self.ac_powerMode_stopV.setReadOnly(False)
                else:
                    self.ac_powerMode_enable.setEnabled(False)
                    self.ac_powerMode_outV.setReadOnly(True)
                    self.ac_powerMode_startV.setReadOnly(True)
                    self.ac_powerMode_stopV.setReadOnly(True)
                    
                self.ac_chgmode.setCurrentIndex(int(result['充电模式']))
                self.ac_powerMode_enable.setCurrentIndex(int(result['电源模式输出使能']))
                self.ac_powerMode_outV.setValue(float(result['电源模式输出电压']))
                self.ac_powerMode_startV.setValue(float(result['电源模式启动充电电压']))
                self.ac_powerMode_stopV.setValue(float(result['电源模式停止充电电压']))

                # 解除信号的阻止
                for obj in self.setting_edit:
                    obj.blockSignals(False)
            
            self.add_tableItem('receive', res, self.ac_show_tab_data)

    # 按钮-开关控制-开关机
    def ac_switch_onoff(self):
        if self.ac_port_nostart_tips() == False: return 0
        # 1 开机， 0 关机
        if self.switch_machine_btn.text() == '开启':
            self.send_msg(f'{ac_sw_on}{calc_crc(ac_sw_on)}')
        else:
            self.send_msg(f'{ac_sw_off}{calc_crc(ac_sw_off)}')

    # 按钮-开关控制-设备复位
    def ac_resetting(self):
        if self.ac_port_nostart_tips() == False: return 0
        self.send_msg(f'{ac_device_reset}{calc_crc(ac_device_reset)}')
    
    # 按钮-开关控制-恢复出厂
    def ac_reset_factory(self):
        if self.ac_port_nostart_tips() == False: return 0
        self.send_msg(f'{ac_fact_reset}{calc_crc(ac_fact_reset)}')

    # 按钮-开关控制-清除历史记录
    def ac_clear_history(self):
        if self.ac_port_nostart_tips() == False: return 0
        self.send_msg(f'{ac_cl_history}{calc_crc(ac_cl_history)}')

    # 按钮-开关控制-测试模式
    def ac_testmode_func(self):
        if self.ac_port_nostart_tips() == False: return 0
        if self.ac_testmode_btn.text() == '开启':
            self.send_msg(f'{ac_testmode_on}{calc_crc(ac_testmode_on)}')
        else:
            self.send_msg(f'{ac_device_reset}{calc_crc(ac_device_reset)}')

    # 按钮-参数设置-读取数据
    def ac_read_data(self):
        if self.ac_port_nostart_tips() == False: return 0
        self.setting_dic = {}
        self.send_msg(f'{ac_get_setting}{calc_crc(ac_get_setting)}')

    # 按钮-参数设置-清屏
    def ac_clear_data(self):
        self.setting_dic = {}
        for s in self.setting_edit:
            try:
                s.setText('')
            except AttributeError:
                pass

    # 按钮-实时监控清屏
    def ac_clear_monitor(self):
        self.prod_type.setText('')
        self.soft_ver.setText('')
        self.sys_current.setText('')
        self.charg_current.setText('')
        self.battery_current.setText('')
        self.prod_spec.setText('')
        self.hard_ver.setText('')
        self.rate_charg_current.setText('')
        # self.rate_discharg_current.setText('')
        self.battery_tp.setText('')
        self.prod_num.setText('')
        self.prod_name.setText('')
        self.prod_adder.setText('')
        self.prod_tp.setText('')
        self.charge_status.setText('')
        self.error_msg.setText('')

    # 按钮-参数设置-写入参数1-获取修改过的参数
    def setting_edit_func(self, set_text):
        try:
            temp = set_text.value()
        except AttributeError:
            try:
                temp = int(set_text.currentText())
            except Exception:
                temp = set_text.currentText()[0]
                
        if temp != '':
            ac_data_list = get_ac_data_list()
            name = set_text.whatsThis()[22:-18]
            print(name)
            if name == '蓄电池类型':
                name_data = self.set_battery_type.currentIndex()
                if name_data == self.set_battery_type.count() - 1:
                    name_data = 11
            elif name == '电池充电下限温度(℃)':
                name_data = self.set_charge_floor_tp.value()
                if name_data < 0:
                    name_data = abs(name_data) + 128
            elif name == '系统电压设置(V)':
                name_data = self.set_sys_current.currentText()
                if name_data == 'AUTO':
                    name_data = 255
                else:
                    name_data = int(temp) * int(ac_data_list[ac_get_setting][name][2])
            else:
                try:
                    name_data = int(temp) * int(ac_data_list[ac_get_setting][name][2])
                except ValueError:
                    return QtWidgets.QMessageBox.critical(self, 'Error', self.setting_tips, QtWidgets.QMessageBox.Ok)  
            
            # self.setting_show[name] = temp  # 存储修改过的参数名称和值，点击写入后用于展示(暂时停用)
            addr = ac_data_list[ac_get_setting][name][3]
            send_setting_txt = f'{ac_get_setting[:2]}06{addr}{name_data:04X}'
            self.setting_dic[name] = f'{send_setting_txt}{calc_crc(send_setting_txt)}'
            print(self.setting_dic[name])
        else:
            return QtWidgets.QMessageBox.critical(self, 'Error', self.write_data_tips, QtWidgets.QMessageBox.Ok)  
    
    # 按钮-参数设置-写入数据
    def ac_write_data(self):
        if self.ac_port_nostart_tips() == False: return 0
        if len(self.setting_dic) != 0:
            self.timer_txt = []
            for k, v in self.setting_dic.items():
                self.timer_txt.append(v)
            self.ac_send_setting_timer = QtCore.QTimer()
            self.ac_send_setting_timer_step = 0
            self.ac_send_setting_timer.timeout.connect(self.ac_send_setting_timer_func)
            self.ac_send_setting_timer.start(500)
