# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\svn\SrneUpperComputer\ui\ac_layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1058, 451)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ac_tabwidget = QtWidgets.QTabWidget(self.centralwidget)
        self.ac_tabwidget.setGeometry(QtCore.QRect(0, 0, 1061, 421))
        self.ac_tabwidget.setObjectName("ac_tabwidget")
        self.ac_monitor_now = QtWidgets.QWidget()
        self.ac_monitor_now.setObjectName("ac_monitor_now")
        self.msg_show = QtWidgets.QGroupBox(self.ac_monitor_now)
        self.msg_show.setGeometry(QtCore.QRect(11, 10, 671, 231))
        self.msg_show.setObjectName("msg_show")
        self.gridLayoutWidget = QtWidgets.QWidget(self.msg_show)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 651, 201))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 10, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_24 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 3, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 1, 0, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 2, 4, 1, 1)
        self.soft_ver = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.soft_ver.setObjectName("soft_ver")
        self.gridLayout.addWidget(self.soft_ver, 1, 1, 1, 1)
        self.prod_type = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.prod_type.setObjectName("prod_type")
        self.gridLayout.addWidget(self.prod_type, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 1, 4, 1, 1)
        self.hard_ver = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.hard_ver.setObjectName("hard_ver")
        self.gridLayout.addWidget(self.hard_ver, 1, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 1, 2, 1, 1)
        self.prod_spec = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.prod_spec.setObjectName("prod_spec")
        self.gridLayout.addWidget(self.prod_spec, 0, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 0, 4, 1, 1)
        self.charg_current = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.charg_current.setObjectName("charg_current")
        self.gridLayout.addWidget(self.charg_current, 3, 1, 1, 1)
        self.prod_adder = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.prod_adder.setObjectName("prod_adder")
        self.gridLayout.addWidget(self.prod_adder, 2, 5, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 2, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 0, 2, 1, 1)
        self.sys_current = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.sys_current.setObjectName("sys_current")
        self.gridLayout.addWidget(self.sys_current, 2, 1, 1, 1)
        self.rate_charg_current = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.rate_charg_current.setObjectName("rate_charg_current")
        self.gridLayout.addWidget(self.rate_charg_current, 2, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.prod_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.prod_name.setObjectName("prod_name")
        self.gridLayout.addWidget(self.prod_name, 1, 5, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 2, 2, 1, 1)
        self.prod_num = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.prod_num.setObjectName("prod_num")
        self.gridLayout.addWidget(self.prod_num, 0, 5, 1, 1)
        self.clearMonitor = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.clearMonitor.setObjectName("clearMonitor")
        self.gridLayout.addWidget(self.clearMonitor, 4, 5, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 3, 2, 1, 1)
        self.prod_tp = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.prod_tp.setObjectName("prod_tp")
        self.gridLayout.addWidget(self.prod_tp, 3, 3, 1, 1)
        self.battery_current = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.battery_current.setObjectName("battery_current")
        self.gridLayout.addWidget(self.battery_current, 3, 5, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 3, 4, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_28.setObjectName("label_28")
        self.gridLayout.addWidget(self.label_28, 4, 0, 1, 1)
        self.battery_tp = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.battery_tp.setObjectName("battery_tp")
        self.gridLayout.addWidget(self.battery_tp, 4, 1, 1, 1)
        self.char_status = QtWidgets.QGroupBox(self.ac_monitor_now)
        self.char_status.setGeometry(QtCore.QRect(10, 253, 331, 131))
        self.char_status.setObjectName("char_status")
        self.charge_status = QtWidgets.QTextEdit(self.char_status)
        self.charge_status.setGeometry(QtCore.QRect(20, 23, 291, 91))
        self.charge_status.setObjectName("charge_status")
        self.msg1 = QtWidgets.QGroupBox(self.ac_monitor_now)
        self.msg1.setGeometry(QtCore.QRect(351, 253, 331, 131))
        self.msg1.setObjectName("msg1")
        self.error_msg = QtWidgets.QTextEdit(self.msg1)
        self.error_msg.setGeometry(QtCore.QRect(20, 23, 291, 91))
        self.error_msg.setObjectName("error_msg")
        self.control = QtWidgets.QGroupBox(self.ac_monitor_now)
        self.control.setGeometry(QtCore.QRect(690, 9, 361, 231))
        self.control.setObjectName("control")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.control)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 341, 201))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(10, 0, 10, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.port_cmb = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.port_cmb.setObjectName("port_cmb")
        self.gridLayout_2.addWidget(self.port_cmb, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.login = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.login.setObjectName("login")
        self.gridLayout_2.addWidget(self.login, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.ac_port_refresh = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.ac_port_refresh.setObjectName("ac_port_refresh")
        self.gridLayout_2.addWidget(self.ac_port_refresh, 2, 2, 1, 1)
        self.pwd = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.pwd.setObjectName("pwd")
        self.gridLayout_2.addWidget(self.pwd, 0, 1, 1, 1)
        self.port_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.port_btn.setObjectName("port_btn")
        self.gridLayout_2.addWidget(self.port_btn, 1, 2, 1, 1)
        self.baud_cmb = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.baud_cmb.setObjectName("baud_cmb")
        self.baud_cmb.addItem("")
        self.baud_cmb.addItem("")
        self.baud_cmb.addItem("")
        self.baud_cmb.addItem("")
        self.gridLayout_2.addWidget(self.baud_cmb, 3, 1, 1, 1)
        self.startMonitor_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.startMonitor_btn.setObjectName("startMonitor_btn")
        self.gridLayout_2.addWidget(self.startMonitor_btn, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.ac_output_monitor = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.ac_output_monitor.setObjectName("ac_output_monitor")
        self.gridLayout_2.addWidget(self.ac_output_monitor, 4, 2, 1, 1)
        self.control2 = QtWidgets.QGroupBox(self.ac_monitor_now)
        self.control2.setGeometry(QtCore.QRect(690, 253, 361, 131))
        self.control2.setObjectName("control2")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.control2)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 341, 101))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(10, 0, 10, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.reset_default_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.reset_default_btn.setObjectName("reset_default_btn")
        self.gridLayout_3.addWidget(self.reset_default_btn, 1, 1, 1, 1)
        self.clear_history_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.clear_history_btn.setObjectName("clear_history_btn")
        self.gridLayout_3.addWidget(self.clear_history_btn, 1, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.switch_machine_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.switch_machine_btn.setObjectName("switch_machine_btn")
        self.gridLayout_3.addWidget(self.switch_machine_btn, 0, 1, 1, 1)
        self.ac_testmode_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.ac_testmode_btn.setObjectName("ac_testmode_btn")
        self.gridLayout_3.addWidget(self.ac_testmode_btn, 0, 3, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_40.setObjectName("label_40")
        self.gridLayout_3.addWidget(self.label_40, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)
        self.prod_reset_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.prod_reset_btn.setObjectName("prod_reset_btn")
        self.gridLayout_3.addWidget(self.prod_reset_btn, 2, 1, 1, 1)
        self.ac_tabwidget.addTab(self.ac_monitor_now, "")
        self.ac_param_set = QtWidgets.QWidget()
        self.ac_param_set.setObjectName("ac_param_set")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.ac_param_set)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(2, 0, 1051, 391))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_41 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_41.setObjectName("label_41")
        self.gridLayout_4.addWidget(self.label_41, 6, 1, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_37.setObjectName("label_37")
        self.gridLayout_4.addWidget(self.label_37, 4, 3, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 1, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_30.setObjectName("label_30")
        self.gridLayout_4.addWidget(self.label_30, 2, 5, 1, 1)
        self.label_36 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_36.setObjectName("label_36")
        self.gridLayout_4.addWidget(self.label_36, 5, 3, 1, 1)
        self.label_38 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_38.setObjectName("label_38")
        self.gridLayout_4.addWidget(self.label_38, 5, 5, 1, 1)
        self.ac_powerMode_enable = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.ac_powerMode_enable.setEnabled(False)
        self.ac_powerMode_enable.setToolTip("")
        self.ac_powerMode_enable.setObjectName("ac_powerMode_enable")
        self.ac_powerMode_enable.addItem("")
        self.ac_powerMode_enable.addItem("")
        self.gridLayout_4.addWidget(self.ac_powerMode_enable, 6, 4, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_20.setObjectName("label_20")
        self.gridLayout_4.addWidget(self.label_20, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        self.label_34 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_34.setObjectName("label_34")
        self.gridLayout_4.addWidget(self.label_34, 4, 1, 1, 1)
        self.ac_chgmode = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.ac_chgmode.setEnabled(False)
        self.ac_chgmode.setToolTip("")
        self.ac_chgmode.setObjectName("ac_chgmode")
        self.ac_chgmode.addItem("")
        self.ac_chgmode.addItem("")
        self.gridLayout_4.addWidget(self.ac_chgmode, 6, 2, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_35.setObjectName("label_35")
        self.gridLayout_4.addWidget(self.label_35, 5, 1, 1, 1)
        self.set_battery_type = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.set_battery_type.setToolTip("")
        self.set_battery_type.setObjectName("set_battery_type")
        self.set_battery_type.addItem("")
        self.set_battery_type.addItem("")
        self.set_battery_type.addItem("")
        self.set_battery_type.addItem("")
        self.set_battery_type.addItem("")
        self.set_battery_type.addItem("")
        self.gridLayout_4.addWidget(self.set_battery_type, 1, 2, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_33.setObjectName("label_33")
        self.gridLayout_4.addWidget(self.label_33, 3, 5, 1, 1)
        self.label_45 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_45.setObjectName("label_45")
        self.gridLayout_4.addWidget(self.label_45, 7, 3, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_39.setObjectName("label_39")
        self.gridLayout_4.addWidget(self.label_39, 4, 5, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_43.setObjectName("label_43")
        self.gridLayout_4.addWidget(self.label_43, 7, 1, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_32.setObjectName("label_32")
        self.gridLayout_4.addWidget(self.label_32, 3, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 1, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 5, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_29.setObjectName("label_29")
        self.gridLayout_4.addWidget(self.label_29, 2, 3, 1, 1)
        self.set_zero_stop = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.set_zero_stop.setToolTip("")
        self.set_zero_stop.setObjectName("set_zero_stop")
        self.set_zero_stop.addItem("")
        self.set_zero_stop.addItem("")
        self.gridLayout_4.addWidget(self.set_zero_stop, 5, 6, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 0, 3, 1, 1)
        self.label_44 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_44.setObjectName("label_44")
        self.gridLayout_4.addWidget(self.label_44, 7, 5, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_42.setObjectName("label_42")
        self.gridLayout_4.addWidget(self.label_42, 6, 3, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_31.setObjectName("label_31")
        self.gridLayout_4.addWidget(self.label_31, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 7, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 1, 5, 1, 1)
        self.set_full_stop = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.set_full_stop.setEnabled(False)
        self.set_full_stop.setToolTip("")
        self.set_full_stop.setObjectName("set_full_stop")
        self.set_full_stop.addItem("")
        self.gridLayout_4.addWidget(self.set_full_stop, 5, 2, 1, 1)
        self.clear_set_data = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.clear_set_data.setObjectName("clear_set_data")
        self.gridLayout_4.addWidget(self.clear_set_data, 8, 6, 1, 1)
        self.write_set_data = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.write_set_data.setObjectName("write_set_data")
        self.gridLayout_4.addWidget(self.write_set_data, 8, 4, 1, 1)
        self.read_set_data = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.read_set_data.setObjectName("read_set_data")
        self.gridLayout_4.addWidget(self.read_set_data, 8, 2, 1, 1)
        self.set_battery_cap = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_battery_cap.setMinimumSize(QtCore.QSize(150, 0))
        self.set_battery_cap.setMaximum(9999)
        self.set_battery_cap.setObjectName("set_battery_cap")
        self.gridLayout_4.addWidget(self.set_battery_cap, 0, 4, 1, 1)
        self.set_sys_current = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_sys_current.setMinimumSize(QtCore.QSize(150, 0))
        self.set_sys_current.setMinimum(12)
        self.set_sys_current.setMaximum(255)
        self.set_sys_current.setProperty("value", 12)
        self.set_sys_current.setObjectName("set_sys_current")
        self.gridLayout_4.addWidget(self.set_sys_current, 0, 6, 1, 1)
        self.set_balanced_time = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_balanced_time.setMaximum(60)
        self.set_balanced_time.setObjectName("set_balanced_time")
        self.gridLayout_4.addWidget(self.set_balanced_time, 3, 4, 1, 1)
        self.set_promote_time = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_promote_time.setMinimum(10)
        self.set_promote_time.setMaximum(600)
        self.set_promote_time.setObjectName("set_promote_time")
        self.gridLayout_4.addWidget(self.set_promote_time, 3, 6, 1, 1)
        self.set_charge_floor_tp = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_charge_floor_tp.setMinimum(-35)
        self.set_charge_floor_tp.setMaximum(10)
        self.set_charge_floor_tp.setObjectName("set_charge_floor_tp")
        self.gridLayout_4.addWidget(self.set_charge_floor_tp, 4, 6, 1, 1)
        self.set_tp_redress = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_tp_redress.setEnabled(False)
        self.set_tp_redress.setMinimum(-5)
        self.set_tp_redress.setMaximum(0)
        self.set_tp_redress.setObjectName("set_tp_redress")
        self.gridLayout_4.addWidget(self.set_tp_redress, 4, 4, 1, 1)
        self.set_balanced_space = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_balanced_space.setMaximum(255)
        self.set_balanced_space.setObjectName("set_balanced_space")
        self.gridLayout_4.addWidget(self.set_balanced_space, 4, 2, 1, 1)
        self.set_full_stop_delay = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.set_full_stop_delay.setMaximum(10)
        self.set_full_stop_delay.setObjectName("set_full_stop_delay")
        self.gridLayout_4.addWidget(self.set_full_stop_delay, 5, 4, 1, 1)
        self.set_charge_elec = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.set_charge_elec.setMinimumSize(QtCore.QSize(150, 0))
        self.set_charge_elec.setMaximum(25.0)
        self.set_charge_elec.setObjectName("set_charge_elec")
        self.gridLayout_4.addWidget(self.set_charge_elec, 0, 2, 1, 1)
        self.ac_powerMode_stopV = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.ac_powerMode_stopV.setDecimals(1)
        self.ac_powerMode_stopV.setMinimum(10.0)
        self.ac_powerMode_stopV.setMaximum(16.0)
        self.ac_powerMode_stopV.setObjectName("ac_powerMode_stopV")
        self.gridLayout_4.addWidget(self.ac_powerMode_stopV, 7, 6, 1, 1)
        self.ac_powerMode_startV = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.ac_powerMode_startV.setDecimals(1)
        self.ac_powerMode_startV.setMinimum(11.0)
        self.ac_powerMode_startV.setMaximum(17.0)
        self.ac_powerMode_startV.setObjectName("ac_powerMode_startV")
        self.gridLayout_4.addWidget(self.ac_powerMode_startV, 7, 4, 1, 1)
        self.ac_powerMode_outV = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.ac_powerMode_outV.setDecimals(1)
        self.ac_powerMode_outV.setMinimum(10.0)
        self.ac_powerMode_outV.setMaximum(30.0)
        self.ac_powerMode_outV.setObjectName("ac_powerMode_outV")
        self.gridLayout_4.addWidget(self.ac_powerMode_outV, 7, 2, 1, 1)
        self.set_float_current = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.set_float_current.setDecimals(1)
        self.set_float_current.setMinimum(9.0)
        self.set_float_current.setMaximum(17.0)
        self.set_float_current.setObjectName("set_float_current")
        self.gridLayout_4.addWidget(self.set_float_current, 2, 6, 1, 1)
        self.set_charge_limit = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.set_charge_limit.setDecimals(1)
        self.set_charge_limit.setMinimum(9.0)
        self.set_charge_limit.setMaximum(17.0)
        self.set_charge_limit.setObjectName("set_charge_limit")
        self.gridLayout_4.addWidget(self.set_charge_limit, 1, 6, 1, 1)
        self.set_promote_current = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.set_promote_current.setDecimals(1)
        self.set_promote_current.setMinimum(9.0)
        self.set_promote_current.setMaximum(17.0)
        self.set_promote_current.setObjectName("set_promote_current")
        self.gridLayout_4.addWidget(self.set_promote_current, 2, 4, 1, 1)
        self.set_battery_overpressure = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.set_battery_overpressure.setDecimals(1)
        self.set_battery_overpressure.setMinimum(9.0)
        self.set_battery_overpressure.setMaximum(17.0)
        self.set_battery_overpressure.setProperty("value", 9.0)
        self.set_battery_overpressure.setObjectName("set_battery_overpressure")
        self.gridLayout_4.addWidget(self.set_battery_overpressure, 1, 4, 1, 1)
        self.set_store_current = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.set_store_current.setDecimals(1)
        self.set_store_current.setMinimum(9.0)
        self.set_store_current.setMaximum(17.0)
        self.set_store_current.setObjectName("set_store_current")
        self.gridLayout_4.addWidget(self.set_store_current, 3, 2, 1, 1)
        self.set_even_current = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_4)
        self.set_even_current.setDecimals(1)
        self.set_even_current.setMinimum(9.0)
        self.set_even_current.setMaximum(17.0)
        self.set_even_current.setObjectName("set_even_current")
        self.gridLayout_4.addWidget(self.set_even_current, 2, 2, 1, 1)
        self.ac_tabwidget.addTab(self.ac_param_set, "")
        self.ac_tab_data = QtWidgets.QWidget()
        self.ac_tab_data.setObjectName("ac_tab_data")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.ac_tab_data)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(2, 2, 1051, 391))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ac_clear_tab_data = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ac_clear_tab_data.setObjectName("ac_clear_tab_data")
        self.verticalLayout.addWidget(self.ac_clear_tab_data)
        self.ac_show_tab_data = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.ac_show_tab_data.setRowCount(0)
        self.ac_show_tab_data.setColumnCount(3)
        self.ac_show_tab_data.setObjectName("ac_show_tab_data")
        item = QtWidgets.QTableWidgetItem()
        self.ac_show_tab_data.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ac_show_tab_data.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ac_show_tab_data.setHorizontalHeaderItem(2, item)
        self.ac_show_tab_data.horizontalHeader().setDefaultSectionSize(100)
        self.ac_show_tab_data.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.ac_show_tab_data)
        self.ac_tabwidget.addTab(self.ac_tab_data, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1058, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.ac_tabwidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AC-DC 充电器"))
        self.msg_show.setTitle(_translate("MainWindow", "信息显示"))
        self.label_24.setText(_translate("MainWindow", "充电电流"))
        self.label_14.setText(_translate("MainWindow", "软件版本"))
        self.label_23.setText(_translate("MainWindow", "设备地址"))
        self.label_16.setText(_translate("MainWindow", "设备名称"))
        self.label_15.setText(_translate("MainWindow", "硬件版本"))
        self.label_13.setText(_translate("MainWindow", "产品序列号"))
        self.label_21.setText(_translate("MainWindow", "系统电压"))
        self.label_12.setText(_translate("MainWindow", "产品规格"))
        self.label_11.setText(_translate("MainWindow", "产品类型"))
        self.label_22.setText(_translate("MainWindow", "额定充电电流"))
        self.clearMonitor.setText(_translate("MainWindow", "清屏"))
        self.label_26.setText(_translate("MainWindow", "设备温度"))
        self.label_27.setText(_translate("MainWindow", "蓄电池电压"))
        self.label_28.setText(_translate("MainWindow", "蓄电池温度"))
        self.char_status.setTitle(_translate("MainWindow", "充电状态"))
        self.msg1.setTitle(_translate("MainWindow", "故障/告警信息"))
        self.control.setTitle(_translate("MainWindow", "操作台"))
        self.label_3.setText(_translate("MainWindow", "波特率(bps)"))
        self.login.setText(_translate("MainWindow", "登录"))
        self.label_2.setText(_translate("MainWindow", "串口号"))
        self.ac_port_refresh.setText(_translate("MainWindow", "刷新串口"))
        self.port_btn.setText(_translate("MainWindow", "打开串口"))
        self.baud_cmb.setItemText(0, _translate("MainWindow", "9600"))
        self.baud_cmb.setItemText(1, _translate("MainWindow", "19200"))
        self.baud_cmb.setItemText(2, _translate("MainWindow", "57600"))
        self.baud_cmb.setItemText(3, _translate("MainWindow", "115200"))
        self.startMonitor_btn.setText(_translate("MainWindow", "开启数据监控"))
        self.label.setText(_translate("MainWindow", "管理员密码"))
        self.ac_output_monitor.setText(_translate("MainWindow", "导出监控数据"))
        self.control2.setTitle(_translate("MainWindow", "开关控制"))
        self.reset_default_btn.setText(_translate("MainWindow", "发送"))
        self.clear_history_btn.setText(_translate("MainWindow", "发送"))
        self.label_7.setText(_translate("MainWindow", "清除历史记录"))
        self.label_4.setText(_translate("MainWindow", "开关机"))
        self.label_6.setText(_translate("MainWindow", "恢复出厂"))
        self.switch_machine_btn.setText(_translate("MainWindow", "开启"))
        self.ac_testmode_btn.setText(_translate("MainWindow", "开启"))
        self.label_40.setText(_translate("MainWindow", "测试模式"))
        self.label_5.setText(_translate("MainWindow", "设备复位"))
        self.prod_reset_btn.setText(_translate("MainWindow", "发送"))
        self.ac_tabwidget.setTabText(self.ac_tabwidget.indexOf(self.ac_monitor_now), _translate("MainWindow", "实时监控"))
        self.label_41.setText(_translate("MainWindow", "充电模式"))
        self.label_37.setText(_translate("MainWindow", "温度补偿系数(mV/℃/2V)"))
        self.label_17.setText(_translate("MainWindow", "蓄电池类型"))
        self.label_30.setText(_translate("MainWindow", "浮充充电电压(V)"))
        self.label_36.setText(_translate("MainWindow", "充满截止延时(S)"))
        self.label_38.setText(_translate("MainWindow", "锂电池零度禁止充"))
        self.ac_powerMode_enable.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>电源模式输出使能</p></body></html>"))
        self.ac_powerMode_enable.setItemText(0, _translate("MainWindow", "0 - 禁止输出"))
        self.ac_powerMode_enable.setItemText(1, _translate("MainWindow", "1 - 使能使出"))
        self.label_20.setText(_translate("MainWindow", "均衡充电电压(V)"))
        self.label_34.setText(_translate("MainWindow", "均衡充电间隔(day)"))
        self.ac_chgmode.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>充电模式</p></body></html>"))
        self.ac_chgmode.setItemText(0, _translate("MainWindow", "0 - 充电模式"))
        self.ac_chgmode.setItemText(1, _translate("MainWindow", "1 - 电源模式"))
        self.label_35.setText(_translate("MainWindow", "充满截止电流(A)"))
        self.set_battery_type.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>蓄电池类型</p></body></html>"))
        self.set_battery_type.setItemText(0, _translate("MainWindow", "自定义铅酸"))
        self.set_battery_type.setItemText(1, _translate("MainWindow", "开口(FLD)"))
        self.set_battery_type.setItemText(2, _translate("MainWindow", "密封(SLD)"))
        self.set_battery_type.setItemText(3, _translate("MainWindow", "胶体(GEL)"))
        self.set_battery_type.setItemText(4, _translate("MainWindow", "锂电池(LI)"))
        self.set_battery_type.setItemText(5, _translate("MainWindow", "自定义锂电池(Li-ion)"))
        self.label_33.setText(_translate("MainWindow", "提升充电时间(min)"))
        self.label_45.setText(_translate("MainWindow", "电源模式启动充电电压"))
        self.label_39.setText(_translate("MainWindow", "电池充电下限温度(℃)"))
        self.label_43.setText(_translate("MainWindow", "电源模式输出电压"))
        self.label_32.setText(_translate("MainWindow", "均衡充电时间(min)"))
        self.label_18.setText(_translate("MainWindow", "超压电压(V)"))
        self.label_8.setText(_translate("MainWindow", "充电电流设置(A)"))
        self.label_10.setText(_translate("MainWindow", "系统电压设置(V)"))
        self.label_29.setText(_translate("MainWindow", "提升充电电压(V)"))
        self.set_zero_stop.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>锂电池零度禁止充</p></body></html>"))
        self.set_zero_stop.setItemText(0, _translate("MainWindow", "0 - 关闭"))
        self.set_zero_stop.setItemText(1, _translate("MainWindow", "1 - 开启"))
        self.label_9.setText(_translate("MainWindow", "蓄电池标称容量(AH)"))
        self.label_44.setText(_translate("MainWindow", "电源模式停止充电电压"))
        self.label_42.setText(_translate("MainWindow", "电源模式输出使能"))
        self.label_31.setText(_translate("MainWindow", "储存充电电压(V)"))
        self.label_19.setText(_translate("MainWindow", "充电限制电压(V)"))
        self.set_full_stop.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>充满截止电流(A)</p></body></html>"))
        self.set_full_stop.setItemText(0, _translate("MainWindow", "0 - 关闭"))
        self.clear_set_data.setText(_translate("MainWindow", "清屏"))
        self.write_set_data.setText(_translate("MainWindow", "写入数据"))
        self.read_set_data.setText(_translate("MainWindow", "读取数据"))
        self.set_battery_cap.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>蓄电池标称容量(AH)</p></body></html>"))
        self.set_sys_current.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>系统电压设置(V)</p></body></html>"))
        self.set_balanced_time.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>均衡充电时间(min)</p></body></html>"))
        self.set_promote_time.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>提升充电时间(min)</p></body></html>"))
        self.set_charge_floor_tp.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>电池充电下限温度(℃)</p></body></html>"))
        self.set_tp_redress.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>温度补偿系数(mV/℃/2V)</p></body></html>"))
        self.set_balanced_space.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>均衡充电间隔(day)</p></body></html>"))
        self.set_full_stop_delay.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>充满截止延时(S)</p></body></html>"))
        self.set_charge_elec.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>充电电流设置(A)</p></body></html>"))
        self.ac_powerMode_stopV.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>电源模式停止充电电压</p></body></html>"))
        self.ac_powerMode_startV.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>电源模式启动充电电压</p></body></html>"))
        self.ac_powerMode_outV.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>电源模式输出电压</p></body></html>"))
        self.set_float_current.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>浮充充电电压(V)</p></body></html>"))
        self.set_charge_limit.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>充电限制电压(V)</p></body></html>"))
        self.set_promote_current.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>提升充电电压(V)</p></body></html>"))
        self.set_battery_overpressure.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>超压电压(V)</p></body></html>"))
        self.set_store_current.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>储存充电电压(V)</p></body></html>"))
        self.set_even_current.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>均衡充电电压(V)</p></body></html>"))
        self.ac_tabwidget.setTabText(self.ac_tabwidget.indexOf(self.ac_param_set), _translate("MainWindow", "参数设置"))
        self.ac_clear_tab_data.setText(_translate("MainWindow", "清空内容"))
        item = self.ac_show_tab_data.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Time"))
        item = self.ac_show_tab_data.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Direction"))
        item = self.ac_show_tab_data.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Send/Receive Data(Hex)"))
        self.ac_tabwidget.setTabText(self.ac_tabwidget.indexOf(self.ac_tab_data), _translate("MainWindow", "串口数据"))
