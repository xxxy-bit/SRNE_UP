#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.i18n.Bms_i18n import *
from settings.bms_modbus import get_bms_modbus_list
from settings.bms_RS485 import get_bms_rs485_list
from PyQt5.QtWidgets import QTableWidget, QFrame, QTextEdit, QHeaderView, QProgressBar, QLineEdit, QTabWidget, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton, QLabel, QGridLayout, QFormLayout
from PyQt5.QtCore import Qt
from .QssStyle import *
from utils.Common import Common
from src.OrderList import *
from qfluentwidgets import DoubleSpinBox, DateTimeEdit, ProgressRing, SwitchButton, ComboBox, TableWidget, PushButton


class BmsLayout(QWidget):

    def __init__(self):
        super().__init__()

    def initUI(self):

        # 读取 modbus 解析列表
        self.json_modbus = get_bms_modbus_list()

        # 读取 rs485 解析列表
        self.json_rs485 = get_bms_rs485_list()

        self.setWindowTitle('Portbms')
        self.resize(1150, 765)   # 可拉伸
        # self.setFixedSize(1800, 950)   # 固定界面大小，不可拉伸

        # 外层
        self.V_layout = QVBoxLayout()
        self.V_layout.setContentsMargins(0, 0, 0, 0)

        self.tabWidget = QTabWidget()
        self.tab_monitor = QWidget()
        self.tab_monitor.setStyleSheet(table_bg)

        self.pal_monitor = QWidget()
        self.pal_monitor.setStyleSheet(table_bg)

        self.tab_data = QWidget()

        self.tab_setParams = QWidget()
        self.tab_setParams.setStyleSheet(table_bg)

        self.sys_seting = QWidget()
        self.sys_seting.setStyleSheet(table_bg)

        self.tab_hisdata = QWidget()

        self.tabWidget.addTab(self.tab_monitor, tab_tabel1)
        self.tabWidget.addTab(self.pal_monitor, tab_tabel2)
        self.tabWidget.addTab(self.tab_setParams, tab_tabel3)
        self.tabWidget.addTab(self.sys_seting, tab_tabel4)
        self.tabWidget.addTab(self.tab_hisdata, tab_tabel5)
        # self.tabWidget.addTab(self.tab_data,self.tab_tabel6)   # 输入密码后才可显示

        self.tab_monitorUI()
        self.pal_monitorUI()
        self.tab_dataUI()
        self.tab_setParamsUI()
        self.sys_setingUI()
        self.tab_hisdataUI()

        self.status_hlayout = QHBoxLayout()
        self.status_Ui()

        self.V_layout.addWidget(self.tabWidget)
        self.V_layout.addLayout(self.status_hlayout)

        self.setLayout(self.V_layout)
        self.center()

    # 并机监控
    def pal_monitorUI(self):
        # 最外层
        pal_layout = QVBoxLayout()

        # 上方
        pal_layout_top = QHBoxLayout()

        # 并联连接
        pal_sys_groupBox = QGroupBox(pal_label1)
        pal_sys_groupBox.setStyleSheet(white_bg)
        pal_sys_groupBox_grid = QGridLayout()

        self.pack_total = ComboBox()
        self.pack_total.addItems([str(i) for i in range(1, 16)])
        self.pal_start = QPushButton(palset_label2)
        self.pal_start.setStyleSheet(open_Button)

        ed4 = [
            QLabel(palset_label1 + '：'), self.pack_total,
            '', self.pal_start
        ]
        positions4 = [(i, j) for i in range(2) for j in range(2)]
        for positions4, ed4 in zip(positions4, ed4):
            if ed4 != '':
                pal_sys_groupBox_grid.addWidget(ed4, *positions4)

        pal_sys_groupBox.setLayout(pal_sys_groupBox_grid)
        pal_layout_top.addWidget(pal_sys_groupBox)
        pal_layout_top.setStretch(0, 1)

        # 并联数据table
        data_groupBox = QGroupBox(pal_label3)
        data_groupBox.setStyleSheet(white_bg)
        data_groupBox_h = QHBoxLayout()

        # 平均soc
        data_groupBox_h_left = QHBoxLayout()
        self.bin_avg_soc = ProgressRing()
        self.bin_avg_soc.setTextVisible(True)
        self.bin_avg_soc.setFormat(paldata_label2 + '\n%p%')

        data_groupBox_h_left.addWidget(self.bin_avg_soc)

        data_groupBox_h_rightV = QVBoxLayout()

        # 总电流
        self.total_elc = QLineEdit()
        self.total_elc.setStyleSheet('border: 0px')
        self.total_elc.setAlignment(Qt.AlignRight)

        data_groupBox_h_right_elc = QHBoxLayout()
        data_groupBox_h_right_elc.addWidget(QLabel(paldata_label3 + '(A)：'))
        data_groupBox_h_right_elc.addWidget(self.total_elc)

        # 平均电压
        self.avg_voltage = QLineEdit()
        self.avg_voltage.setStyleSheet('border: 0px')
        self.avg_voltage.setAlignment(Qt.AlignRight)

        data_groupBox_h_right_vol = QHBoxLayout()
        data_groupBox_h_right_vol.addWidget(QLabel(paldata_label1 + '(V)：'))
        data_groupBox_h_right_vol.addWidget(self.avg_voltage)

        data_groupBox_h_rightV.addLayout(data_groupBox_h_right_elc)
        data_groupBox_h_rightV.addLayout(data_groupBox_h_right_vol)

        data_groupBox_h.addLayout(data_groupBox_h_left)
        data_groupBox_h.addLayout(data_groupBox_h_rightV)

        data_groupBox.setLayout(data_groupBox_h)
        pal_layout_top.addWidget(data_groupBox)
        pal_layout_top.setStretch(1, 1)

        # 电芯数据
        celldata_groupBox = QGroupBox(pal_label4)
        celldata_groupBox.setStyleSheet(white_bg)
        celldata_groupBox_v = QVBoxLayout()
        celldata_groupBox_v_h1 = QHBoxLayout()

        # 最高电芯电压
        self.cell_max = QLineEdit()
        self.cell_max.setStyleSheet(bin_cell_LineEdit)
        self.cell_max_posi = QLineEdit()
        self.cell_max_posi.setStyleSheet(bin_cell_LineEdit)

        celldata_groupBox_v_h1_h1 = QHBoxLayout()
        cell_form_bg = QWidget()
        cell_form_bg.setStyleSheet('background-color:#FFFBF8')
        cell_form = QFormLayout(cell_form_bg)
        cell_form.addRow(QLabel(celldata_label1 + '(mV)：'), self.cell_max)
        cell_form.addRow(QLabel(celldata_label2), self.cell_max_posi)
        celldata_groupBox_v_h1_h1.addWidget(cell_form_bg)

        # 最高电芯温度
        self.cell_max_tmp = QLineEdit()
        self.cell_max_tmp.setStyleSheet(bin_cell_LineEdit)
        self.cell_max_tmp_posi = QLineEdit()
        self.cell_max_tmp_posi.setStyleSheet(bin_cell_LineEdit)

        celldata_groupBox_v_h1_h2 = QHBoxLayout()
        cell_form2_bg = QWidget()
        cell_form2_bg.setStyleSheet('background-color:#FFFBF8')
        cell_form2 = QFormLayout(cell_form2_bg)
        cell_form2.addRow(QLabel(celldata_label5 + '(℃)：'), self.cell_max_tmp)
        cell_form2.addRow(QLabel(celldata_label6), self.cell_max_tmp_posi)
        celldata_groupBox_v_h1_h2.addWidget(cell_form2_bg)

        celldata_groupBox_v_h1.addLayout(celldata_groupBox_v_h1_h1)
        celldata_groupBox_v_h1.addLayout(celldata_groupBox_v_h1_h2)

        celldata_groupBox_v_h2 = QHBoxLayout()

        # 最低电芯电压
        self.cell_min = QLineEdit()
        self.cell_min.setStyleSheet(bin_cell2_LineEdit)
        self.cell_min_posi = QLineEdit()
        self.cell_min_posi.setStyleSheet(bin_cell2_LineEdit)

        celldata_groupBox_v_h2_h1 = QHBoxLayout()
        cell_form3_bg = QWidget()
        cell_form3_bg.setStyleSheet('background-color:#F9FCFF')
        cell_form3 = QFormLayout(cell_form3_bg)
        cell_form3.addRow(QLabel(celldata_label3 + '(mV)：'), self.cell_min)
        cell_form3.addRow(QLabel(celldata_label4), self.cell_min_posi)
        celldata_groupBox_v_h2_h1.addWidget(cell_form3_bg)

        # 最低电芯温度
        self.cell_min_tmp = QLineEdit()
        self.cell_min_tmp.setStyleSheet(bin_cell2_LineEdit)
        self.cell_min_tmp_posi = QLineEdit()
        self.cell_min_tmp_posi.setStyleSheet(bin_cell2_LineEdit)

        celldata_groupBox_v_h2_h2 = QHBoxLayout()
        cell_form4_bg = QWidget()
        cell_form4_bg.setStyleSheet('background-color:#F9FCFF')
        cell_form4 = QFormLayout(cell_form4_bg)
        cell_form4.addRow(QLabel(celldata_label7 + '(℃)：'), self.cell_min_tmp)
        cell_form4.addRow(QLabel(celldata_label8), self.cell_min_tmp_posi)
        celldata_groupBox_v_h2_h2.addWidget(cell_form4_bg)

        celldata_groupBox_v_h2.addLayout(celldata_groupBox_v_h2_h1)
        celldata_groupBox_v_h2.addLayout(celldata_groupBox_v_h2_h2)

        celldata_groupBox_v.addLayout(celldata_groupBox_v_h1)
        celldata_groupBox_v.addLayout(celldata_groupBox_v_h2)

        celldata_groupBox.setLayout(celldata_groupBox_v)
        pal_layout_top.addWidget(celldata_groupBox)
        pal_layout_top.setStretch(2, 2)

        # 下方
        # pack具体数据
        pal_layout_bottom = QHBoxLayout()
        self.palTable = QTableWidget()
        self.palTable.setStyleSheet(white_bg)
        # self.palTable.setColumnCount(4)
        # self.palTable.setHorizontalHeaderLabels(['11','12','13','14'])
        self.col_labels = [
            'Cell' + palnum_label1 + '_1', 'Cell' + palnum_label1 +
            '_2', 'Cell' + palnum_label1 + '_3', 'Cell' + palnum_label1 + '_4',
            'Cell' + palnum_label1 + '_5', 'Cell' + palnum_label1 +
            '_6', 'Cell' + palnum_label1 + '_7', 'Cell' + palnum_label1 + '_8',
            'Cell' + palnum_label1 + '_9', 'Cell' + palnum_label1 + '_10', 'Cell' +
            palnum_label1 + '_11', 'Cell' + palnum_label1 + '_12',
            'Cell' + palnum_label1 + '_13', 'Cell' + palnum_label1 + '_14', 'Cell' +
            palnum_label1 + '_15', 'Cell' + palnum_label1 + '_16',
            palnum_label2 + '_1', palnum_label2 + '_2', palnum_label2 +
            '_3', palnum_label2 + '_4', palnum_label2 + '_5',
            palnum_label2 + '_6', palnum_label2 +
            '_7', palnum_label2 + '_8', palnum_label2 + '_9',
            palnum_label3, 'PACK' + paldata_label4, 'PACK' +
            battery_label3, 'PACK' + battery_label4,
            palnum_label7, palnum_label8, 'PACK SOC',
            'Cell' + palnum_label9 + '_1', 'Cell' + palnum_label9 +
            '_2', 'Cell' + palnum_label9 + '_3', 'Cell' + palnum_label9 + '_4',
            'Cell' + palnum_label9 + '_5', 'Cell' + palnum_label9 +
            '_6', 'Cell' + palnum_label9 + '_7', 'Cell' + palnum_label9 + '_8',
            'Cell' + palnum_label9 + '_9', 'Cell' + palnum_label9 + '_10', 'Cell' +
            palnum_label9 + '_11', 'Cell' + palnum_label9 + '_12',
            'Cell' + palnum_label9 + '_13', 'Cell' + palnum_label9 + '_14', 'Cell' +
            palnum_label9 + '_15', 'Cell' + palnum_label9 + '_16',
            palnum_label2 + palnum_label9 + '_1', palnum_label2 + palnum_label9 + '_2', palnum_label2 +
            palnum_label9 + '_3', palnum_label2 + palnum_label9 +
            '_4', palnum_label2 + palnum_label9 + '_5',
            palnum_label2 + palnum_label9 + '_6', palnum_label2 + palnum_label9 +
            '_7', palnum_label2 + palnum_label9 + '_8', palnum_label2 + palnum_label9 + '_9',
            palnum_label10, palnum_label11, palnum_label12, f'{group_tabel10}_1',
            f'{group_tabel10}_2', palnum_label14, palnum_label15, group_tabel8,
            palnum_label16 + '_1', palnum_label16 +
            '_2', f'{group_tabel9}_1', f'{group_tabel9}_2',
        ]
        self.palTable.setRowCount(len(self.col_labels))
        self.palTable.setVerticalHeaderLabels(self.col_labels)

        pal_layout_bottom.addWidget(self.palTable)

        pal_layout.addLayout(pal_layout_top)
        pal_layout.addLayout(pal_layout_bottom)

        self.pal_monitor.setLayout(pal_layout)

    # 系统设置
    def sys_setingUI(self):
        # 最外层
        sys_layout = QHBoxLayout()

        # 上边
        sys_layout_left = QHBoxLayout()

        # 电量
        elect_groupBox = QGroupBox(sysset_label1)
        elect_groupBox.setStyleSheet(white_bg)
        elect_groupBox.setMaximumHeight(250)
        elect_groupBox.setMaximumWidth(250)
        elect_groupBox_v = QVBoxLayout()

        elect_groupBox_v_topH = QHBoxLayout()

        # 总容量
        elect_groupBox_v_topH_leftV_bg = QWidget()
        # elect_groupBox_v_topH_leftV_bg.setStyleSheet('background-color: #FAFAFA;')

        elect_groupBox_v_topH_leftV = QVBoxLayout(
            elect_groupBox_v_topH_leftV_bg)

        self.fullCap_Line = QLineEdit()
        self.fullCap_Line.setAlignment(Qt.AlignCenter)
        self.fullCap_Line.setStyleSheet("background-color:#FFFFFF;"
                                        "font-size: 20pt;"
                                        "border: 1px solid #dcd8d8;"
                                        )

        fullCap = QLabel(f'{sysset_label4}(AH)')
        fullCap.setAlignment(Qt.AlignCenter)
        fullCap.setStyleSheet(sys_label)

        elect_groupBox_v_topH_leftV.addStretch(1)
        elect_groupBox_v_topH_leftV.addWidget(self.fullCap_Line)
        elect_groupBox_v_topH_leftV.addWidget(fullCap)
        elect_groupBox_v_topH_leftV.addStretch(1)

        elect_groupBox_v_topH_rightV = QVBoxLayout()

        elect_groupBox_v_topH_rightV_topV_bg = QWidget()
        # elect_groupBox_v_topH_rightV_topV_bg.setStyleSheet('background-color: #FAFAFA')
        elect_groupBox_v_topH_rightV_topV = QVBoxLayout(
            elect_groupBox_v_topH_rightV_topV_bg)

        # 设计容量
        dsn = QLabel(f'{sysset_label2}(AH)')
        dsn.setAlignment(Qt.AlignCenter)
        dsn.setStyleSheet(sys_label)
        self.designCap = QLineEdit()
        self.designCap.setAlignment(Qt.AlignCenter)
        self.designCap.setStyleSheet(sys_Line)

        elect_groupBox_v_topH_rightV_topV.addWidget(dsn)
        elect_groupBox_v_topH_rightV_topV.addWidget(self.designCap)

        elect_groupBox_v_topH_rightV_btmV_bg = QWidget()
        # elect_groupBox_v_topH_rightV_btmV_bg.setStyleSheet('background-color: #FAFAFA')
        elect_groupBox_v_topH_rightV_btmV = QVBoxLayout(
            elect_groupBox_v_topH_rightV_btmV_bg)

        # 剩余容量
        reCap = QLabel(battery_label3 + '(AH)')
        reCap.setAlignment(Qt.AlignCenter)
        reCap.setStyleSheet(sys_label)
        self.remainCap = QLineEdit()
        self.remainCap.setAlignment(Qt.AlignCenter)
        self.remainCap.setStyleSheet(sys_Line)

        elect_groupBox_v_topH_rightV_btmV.addWidget(reCap)
        elect_groupBox_v_topH_rightV_btmV.addWidget(self.remainCap)

        elect_groupBox_v_topH_rightV.addWidget(
            elect_groupBox_v_topH_rightV_topV_bg)
        elect_groupBox_v_topH_rightV.addWidget(
            elect_groupBox_v_topH_rightV_btmV_bg)

        elect_groupBox_v_topH.addWidget(elect_groupBox_v_topH_leftV_bg)
        elect_groupBox_v_topH.addLayout(elect_groupBox_v_topH_rightV)

        elect_groupBox_v_btmH = QHBoxLayout()
        self.readCap = QPushButton(sysset_label5)
        self.readCap.setStyleSheet(open_Button)
        self.writeCap = QPushButton('写入')
        self.writeCap.setStyleSheet(open_Button)

        elect_groupBox_v_btmH.addWidget(self.readCap)
        elect_groupBox_v_btmH.addWidget(self.writeCap)

        elect_groupBox_v.addLayout(elect_groupBox_v_topH)
        elect_groupBox_v.addLayout(elect_groupBox_v_btmH)

        elect_groupBox.setLayout(elect_groupBox_v)
        sys_layout_left.addWidget(elect_groupBox)

        # 数据校准
        datacalibration_groupBox = QGroupBox('数据校准')
        datacalibration_groupBox.setStyleSheet(white_bg)
        datacalibration_groupBox.setMaximumHeight(250)
        datacalibration_groupBox.setMaximumWidth(250)

        datacalibration_groupBox_v = QVBoxLayout()

        datacalibration_groupBox_v_h1 = QHBoxLayout()
        self.adds_combox = ComboBox()

        self.datacalibration_adds_list = {
            '电流': '01700105',
            '总压': '01700106',
            'cell_1 电压': '01700107',
            'cell_2 电压': '01700108',
            'cell_3 电压': '01700109',
            'cell_4 电压': '0170010a',
            'cell_5 电压': '0170010b',
            'cell_6 电压': '0170010c',
            'cell_7 电压': '0170010d',
            'cell_8 电压': '0170010e',
            'cell_9 电压': '0170010f',
            'cell_10 电压': '01700110',
            'cell_11 电压': '01700111',
            'cell_12 电压': '01700112',
            'cell_13 电压': '01700113',
            'cell_14 电压': '01700114',
            'cell_15 电压': '01700115',
            'cell_16 电压': '01700116',
        }

        self.adds_combox.addItems(
            [k for k, v in self.datacalibration_adds_list.items()])
        datacalibration_groupBox_v_h1.addWidget(self.adds_combox)

        datacalibration_groupBox_v_h2 = QHBoxLayout()
        self.adds_txt = DoubleSpinBox()
        self.adds_txt.setMinimum(0)
        self.adds_txt.setMaximum(999)
        self.adds_btn = PushButton('校准')
        datacalibration_groupBox_v_h2.addWidget(self.adds_txt)
        datacalibration_groupBox_v_h2.addWidget(self.adds_btn)
        datacalibration_groupBox_v_h2.setStretch(0, 1)

        datacalibration_groupBox_v_h3 = QHBoxLayout()
        self.adds_progress = QProgressBar()
        self.adds_progress.setStyleSheet(GREEN_ProgressBar)
        self.adds_progress.setMaximumWidth(250)
        self.adds_progress.setMaximum(6)
        datacalibration_groupBox_v_h3.addWidget(self.adds_progress)

        datacalibration_groupBox_v.addLayout(datacalibration_groupBox_v_h1)
        datacalibration_groupBox_v.addLayout(datacalibration_groupBox_v_h2)
        datacalibration_groupBox_v.addLayout(datacalibration_groupBox_v_h3)
        datacalibration_groupBox_v.addStretch(1)
        datacalibration_groupBox.setLayout(datacalibration_groupBox_v)
        sys_layout_left.addWidget(datacalibration_groupBox)

        # 系统时间
        time_groupBox = QGroupBox('系统时间')
        time_groupBox.setStyleSheet(white_bg)
        time_groupBox.setMaximumHeight(250)
        time_groupBox.setMaximumWidth(250)

        time_groupBox_v = QVBoxLayout()

        time_groupBox_v_toph = QVBoxLayout()
        self.now_time = DateTimeEdit()
        self.now_time.setDisplayFormat('yyyy/M/d H:mm:ss')
        
        self.sync_btn = PushButton('同步时间')

        time_groupBox_v_toph.addWidget(self.now_time)
        time_groupBox_v_toph.addWidget(self.sync_btn)

        # 同步电脑时间
        # time_groupBox_v_toph2 = QHBoxLayout()

        time_groupBox_v_bomh = QHBoxLayout()
        self.readTime = QPushButton(sysset_label5)
        self.readTime.setStyleSheet(open_Button)
        self.writeTime = QPushButton('写入')
        self.writeTime.setStyleSheet(open_Button)

        time_groupBox_v_bomh.addWidget(self.readTime)
        time_groupBox_v_bomh.addWidget(self.writeTime)

        time_groupBox_v.addLayout(time_groupBox_v_toph)
        # time_groupBox_v.addLayout(time_groupBox_v_toph2)
        time_groupBox_v.addStretch(1)
        time_groupBox_v.addLayout(time_groupBox_v_bomh)
        time_groupBox.setLayout(time_groupBox_v)
        sys_layout_left.addWidget(time_groupBox)

        # 下边
        sys_layout_right = QHBoxLayout()

        sys_layout.addLayout(sys_layout_left)
        sys_layout.addLayout(sys_layout_right)
        self.sys_seting.setLayout(sys_layout)

    # 界面居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 状态栏
    def status_Ui(self):
        self.status_hlayout.setContentsMargins(10, 0, 10, 15)
        self.version = QLabel(f'{ver_label1}:')
        # self.version.setAlignment(Qt.AlignLeft)
        self.bms_sn = QLabel('BMS S/N:')
        self.pack_sn = QLabel('PACK S/N:')
        self.connStatus = QProgressBar()
        self.connStatus.setStyleSheet(RED_ProgressBar)
        self.connStatus.setAlignment(Qt.AlignCenter)
        self.connStatus.setMaximumWidth(500)
        self.nowTime = QLabel()
        self.nowTime.setAlignment(Qt.AlignRight)

        self.status_hlayout.addWidget(self.version)
        self.status_hlayout.addWidget(self.bms_sn)
        self.status_hlayout.addWidget(self.pack_sn)
        self.status_hlayout.addWidget(self.connStatus)
        self.status_hlayout.addWidget(self.nowTime)

    # 实时监控
    def tab_monitorUI(self):
        # 最外层
        tab1_layout = QHBoxLayout()

        # 左边
        tab1_layout_left = QVBoxLayout()

        # 左边-上
        tab1_layout_left_top = QVBoxLayout()

        # 左边-上-左：电池信息
        tab1_layout_left_top_left = QVBoxLayout()
        battery_groupBox = QGroupBox(group_tabel1)
        battery_groupBox.setStyleSheet(white_bg)

        # 电池信息：竖布局
        bat_v = QVBoxLayout()

        # SOC,SOH仪表盘界面
        bat_v_Hlayout = QHBoxLayout()

        self.soc_pr = ProgressRing()
        self.soc_pr.setTextVisible(True)
        self.soc_pr.setFormat('SOC\n%p%')

        self.soh_pr = ProgressRing()
        self.soh_pr.setTextVisible(True)
        self.soh_pr.setFormat('SOH\n%p%')

        bat_v_Hlayout.addWidget(self.soc_pr)
        bat_v_Hlayout.addWidget(self.soh_pr)

        # 剩下的用grid布局, 电池电压、电池电流、剩余容量、充满容量、循环次数
        bat_v_Hlayout2 = QHBoxLayout()
        bat_v_Hlayout2_grid = QGridLayout()

        bat_v.addLayout(bat_v_Hlayout)
        bat_v.addLayout(bat_v_Hlayout2)

        bat_v_Hlayout2.addLayout(bat_v_Hlayout2_grid)

        self.battery_label1_line = QLineEdit()
        self.battery_label1_line.setAlignment(Qt.AlignCenter)
        self.battery_label1_line.setStyleSheet(batl_LineEdit)
        self.battery_label1_line.setReadOnly(True)
        self.battery_label2_line = QLineEdit()
        self.battery_label2_line.setAlignment(Qt.AlignCenter)
        self.battery_label2_line.setStyleSheet(batl_LineEdit)
        self.battery_label2_line.setReadOnly(True)
        self.battery_label3_line = QLineEdit()
        self.battery_label3_line.setAlignment(Qt.AlignCenter)
        self.battery_label3_line.setStyleSheet(batl_LineEdit)
        self.battery_label3_line.setReadOnly(True)
        self.battery_label4_line = QLineEdit()
        self.battery_label4_line.setAlignment(Qt.AlignCenter)
        self.battery_label4_line.setStyleSheet(batl_LineEdit)
        self.battery_label4_line.setReadOnly(True)
        self.battery_label5_line = QLineEdit()
        self.battery_label5_line.setAlignment(Qt.AlignCenter)
        self.battery_label5_line.setStyleSheet(batl_LineEdit)
        self.battery_label5_line.setReadOnly(True)

        bat_v_Hlayout2_grid.addWidget(self.battery_label1_line, 0, 0)
        bat_v_Hlayout2_grid.addWidget(self.battery_label2_line, 0, 1)
        bat_v_Hlayout2_grid.addWidget(self.battery_label3_line, 0, 2)
        bat_v_Hlayout2_grid.addWidget(self.battery_label4_line, 0, 3)
        bat_v_Hlayout2_grid.addWidget(self.battery_label5_line, 0, 4)

        bl1 = QLabel(battery_label1)
        bl1.setAlignment(Qt.AlignCenter)
        bl2 = QLabel(battery_label2)
        bl2.setAlignment(Qt.AlignCenter)
        bl3 = QLabel(battery_label3)
        bl3.setAlignment(Qt.AlignCenter)
        bl4 = QLabel(battery_label4)
        bl4.setAlignment(Qt.AlignCenter)
        bl5 = QLabel(battery_label5)
        bl5.setAlignment(Qt.AlignCenter)

        bat_v_Hlayout2_grid.addWidget(bl1, 1, 0)
        bat_v_Hlayout2_grid.addWidget(bl2, 1, 1)
        bat_v_Hlayout2_grid.addWidget(bl3, 1, 2)
        bat_v_Hlayout2_grid.addWidget(bl4, 1, 3)
        bat_v_Hlayout2_grid.addWidget(bl5, 1, 4)

        # 左边：温度信息
        tab1_layout_left_top_right = QVBoxLayout()
        temperature_groupBox = QGroupBox(group_tabel2)
        temperature_groupBox.setStyleSheet(white_bg)
        tem_h = QHBoxLayout()

        tem_form1_bg = QWidget()
        tem_form1_bg.setStyleSheet("background-color: #F9FCFF")
        tem_form1 = QFormLayout(tem_form1_bg)

        tem_form2_bg = QWidget()
        tem_form2_bg.setStyleSheet("background-color: #F9FCFF")
        tem_form2 = QFormLayout(tem_form2_bg)
        tem_form3 = QFormLayout()

        # 创建 cell温度 1~16 的对象
        self.cell_temp_16 = {}

        for i in range(16):
            self.cell_temp_16[f'cell_{i+1}(℃)'] = QLineEdit()
        for k, v in self.cell_temp_16.items():
            self.cell_temp_16[k].setStyleSheet(cellTmp_LineEdit)
            self.cell_temp_16[k].setReadOnly(True)
            self.cell_temp_16[k].setAlignment(Qt.AlignCenter)
            if int(k[5:-3]) <= 8:
                tem_form1.addRow(k, v)
            else:
                tem_form2.addRow(k, v)

        self.tem_other = {
            temp_label19 + '(℃)': QLineEdit(),
            temp_label20 + '(℃)': QLineEdit(),
            temp_label21 + '(℃)': QLineEdit(),
            temp_label22 + '(℃)': QLineEdit(),
            temp_label23 + '(℃)': QLineEdit(),
            temp_label24 + '(℃)': QLineEdit(),
            temp_label25 + '(℃)': QLineEdit()
        }
        for k, v in self.tem_other.items():
            self.tem_other[k].setStyleSheet(cellTmp2_LineEdit)
            self.tem_other[k].setReadOnly(True)
            self.tem_other[k].setAlignment(Qt.AlignCenter)
            tem_form3.addRow(k, v)

        # 左边-单体电压
        tab1_layout_left_mid = QHBoxLayout()
        voltage_groupBox = QGroupBox(group_tabel3)
        voltage_groupBox.setStyleSheet(white_bg)
        vol_V = QVBoxLayout()

        vol_V_H1 = QHBoxLayout()

        # cell 最大电压
        vol_V_H1_2_bg = QWidget()
        vol_V_H1_2_bg.setStyleSheet("background-color: #FFFAF5")
        vol_V_H1_2 = QHBoxLayout(vol_V_H1_2_bg)
        self.cellLine2 = QLineEdit()
        self.cellLine2.setReadOnly(True)
        self.cellLine2.setStyleSheet(cellVol1_LineEdit)
        vol_V_H1_2.addWidget(QLabel(vol_label18 + '(V)'))
        vol_V_H1_2.addWidget(self.cellLine2)
        vol_V_H1.addWidget(vol_V_H1_2_bg)

        # cell 最小电压
        vol_V_H1_3_bg = QWidget()
        vol_V_H1_3_bg.setStyleSheet("background-color: #FFFAF5")
        vol_V_H1_3 = QHBoxLayout(vol_V_H1_3_bg)
        self.cellLine3 = QLineEdit()
        self.cellLine3.setReadOnly(True)
        self.cellLine3.setStyleSheet(cellVol1_LineEdit)
        vol_V_H1_3.addWidget(QLabel(vol_label19 + '(V)'))
        vol_V_H1_3.addWidget(self.cellLine3)
        vol_V_H1.addWidget(vol_V_H1_3_bg)

        # cell 最大压差
        vol_V_H1_1_bg = QWidget()
        vol_V_H1_1_bg.setStyleSheet("background-color: #FFFAF5")
        vol_V_H1_1 = QHBoxLayout(vol_V_H1_1_bg)
        self.cellLine1 = QLineEdit()
        self.cellLine1.setReadOnly(True)
        self.cellLine1.setStyleSheet(cellVol1_LineEdit)
        vol_V_H1_1.addWidget(QLabel(vol_label17 + '(V)'))
        vol_V_H1_1.addWidget(self.cellLine1)
        vol_V_H1.addWidget(vol_V_H1_1_bg)

        vol_V_H2_bg = QWidget()
        vol_V_H2_bg.setStyleSheet("background-color: #FDFCFB")
        vol_V_H2 = QHBoxLayout(vol_V_H2_bg)

        vol_form4 = QFormLayout()
        vol_form8 = QFormLayout()
        vol_form12 = QFormLayout()
        vol_form16 = QFormLayout()

        vol_V_H2.addLayout(vol_form4)
        vol_V_H2.addLayout(vol_form8)
        vol_V_H2.addLayout(vol_form12)
        vol_V_H2.addLayout(vol_form16)

        self.cell_vol_16 = {}

        for i in range(16):
            self.cell_vol_16[f'cell_{i+1}(V)'] = QLineEdit()
        for k, v in self.cell_vol_16.items():
            self.cell_vol_16[k].setStyleSheet(cellVol2_LineEdit)
            self.cell_vol_16[k].setReadOnly(True)
            self.cell_vol_16[k].setAlignment(Qt.AlignCenter)
            if int(k[5:-3]) <= 4:
                vol_form4.addRow(k, v)
            elif int(k[5:-3]) <= 8:
                vol_form8.addRow(k, v)
            elif int(k[5:-3]) <= 12:
                vol_form12.addRow(k, v)
            elif int(k[5:-3]) <= 16:
                vol_form16.addRow(k, v)

        # 右边
        tab1_layout_right = QVBoxLayout()

        # 右边-上
        tab1_layout_right_top = QVBoxLayout()

        # 串口信息
        port_groupBox = QGroupBox(group_tabel55)
        port_groupBox.setStyleSheet(white_bg)
        port_H = QHBoxLayout()
        port_grid = QGridLayout()

        self.port_combobox = ComboBox()
        self.baud_combobox = ComboBox()
        self.pack_combobox = ComboBox()
        self.pack_combobox.setEnabled(False)
        self.pack_num_line = QLineEdit()
        self.pack_num_line.setEnabled(False)
        self.address_line = QLineEdit()
        self.address_line.setEnabled(False)
        self.space_combobox = ComboBox()
        self.open_port_btn = QPushButton(com_label6)
        self.open_port_btn.setStyleSheet(close_Button)

        self.refresh_port_btn = QPushButton('刷新串口')
        self.refresh_port_btn.setStyleSheet(open_Button)

        self.getP01_data_btn = QPushButton(com_label8)
        self.getP01_data_btn.setStyleSheet(close_Button)
        wd = [
            QLabel(group_tabel5 + ':'), self.port_combobox, QLabel(com_label2 +
                                                                   ':'), self.baud_combobox, self.open_port_btn,
            QLabel('Pack:'), self.pack_combobox, QLabel(
                com_label3 + ':'), self.pack_num_line, self.refresh_port_btn,
            QLabel(com_label4 + ':'), self.address_line, QLabel(com_label5 +
                                                                ':'), self.space_combobox, self.getP01_data_btn
        ]
        positions = [(i, j) for i in range(3) for j in range(5)]
        # wd = [
        #     QLabel(group_tabel5 + ':'), self.port_combobox, QLabel(com_label2 + ':'), self.baud_combobox, self.open_port_btn,
        #     '', '', QLabel(com_label5 + ':'), self.space_combobox, self.getP01_data_btn,
        # ]
        # positions = [(i,j) for i in range(2) for j in range(5)]

        for positions, wd in zip(positions, wd):
            if wd == '':
                continue
            port_grid.addWidget(wd, *positions)

        # 系统状态
        sysStatus_groupBox = QGroupBox(group_tabel7)
        sysStatus_groupBox.setStyleSheet(white_bg)
        sysStatus_groupBox_grid = QGridLayout()
        self.charg_status = QLabel('●' + sys_label1)
        self.disCharg_status = QLabel('●' + sys_label2)
        self.chargMos_status = QLabel('●' + sys_label3)
        self.disChargMos_status = QLabel('●' + sys_label4)
        self.batCharg_status = QLabel('●' + sys_label5)
        self.full_status = QLabel('●' + sys_label6)
        self.hot_status = QLabel('●' + '加热')
        self.twoProtTrig_status = QLabel('●' + '二次保护触发')
        sg = [
            self.charg_status, self.chargMos_status, self.batCharg_status,
            self.disCharg_status, self.disChargMos_status, self.full_status,
            self.hot_status, self.twoProtTrig_status
        ]
        sys_positions = [(i, j) for i in range(3) for j in range(3)]
        for positions, sg in zip(sys_positions, sg):
            sysStatus_groupBox_grid.addWidget(sg, *positions)
        sysStatus_groupBox.setLayout(sysStatus_groupBox_grid)

        # 其他状态（故障、告警、保护）
        otherStatus_groupBox = QGroupBox('其他状态')
        otherStatus_groupBox.setStyleSheet(white_bg)
        otherStatus_groupBox_h = QHBoxLayout()
        otherStatus_groupBox_h.setSpacing(0)

        # 故障状态布局
        error_v = QVBoxLayout()

        error_v_head_bg = QWidget()
        error_v_head_bg.setStyleSheet("background-color: #FEEFEB")
        error_v_head = QVBoxLayout(error_v_head_bg)

        # 故障状态标题
        error_title = QLabel(group_tabel8)
        error_title.setAlignment(Qt.AlignCenter)
        error_title.setStyleSheet('color: #DB6949')
        error_v_head.addWidget(error_title)

        # 故障状态内容
        error_v_body_bg = QWidget()
        error_v_body_bg.setStyleSheet("background-color: #FDFBFB")
        error_v_body = QVBoxLayout(error_v_body_bg)
        self.error_body = QTextEdit()
        self.error_body.setFrameShape(QFrame.NoFrame)
        self.error_body.setStyleSheet("color: #DB6949")

        error_v_body.addWidget(self.error_body)

        error_v.addWidget(error_v_head_bg)
        error_v.addWidget(error_v_body_bg)

        # 告警状态布局
        warn_v = QVBoxLayout()
        warn_v_head_bg = QWidget()
        warn_v_head_bg.setStyleSheet("background-color: #FEF7EB")
        warn_v_head = QHBoxLayout(warn_v_head_bg)
        warn_title = QLabel(group_tabel9)
        warn_title.setAlignment(Qt.AlignCenter)
        warn_title.setStyleSheet('color: #D9931A')
        warn_v_head.addWidget(warn_title)

        warn_v_body_bg = QWidget()
        warn_v_body_bg.setStyleSheet("background-color: #FDFDFB")
        warn_v_body = QHBoxLayout(warn_v_body_bg)

        self.warn_body = QTextEdit()
        self.warn_body.setFrameShape(QFrame.NoFrame)
        self.warn_body.setStyleSheet("color: #DB6949")
        warn_v_body.addWidget(self.warn_body)

        warn_v.addWidget(warn_v_head_bg)
        warn_v.addWidget(warn_v_body_bg)

        # 保护状态布局
        protect_v = QVBoxLayout()
        protect_v_head_bg = QWidget()
        protect_v_head_bg.setStyleSheet('background-color: #F0FAF4')
        protect_v_head = QHBoxLayout(protect_v_head_bg)
        propert_title = QLabel(group_tabel10)
        propert_title.setStyleSheet('color: #46AC6E')
        propert_title.setAlignment(Qt.AlignCenter)
        protect_v_head.addWidget(propert_title)

        protect_v_body_bg = QWidget()
        protect_v_body_bg.setStyleSheet('background-color: #FBFDFB')
        protect_v_body = QHBoxLayout(protect_v_body_bg)
        self.protect_body = QTextEdit()
        self.protect_body.setFrameShape(QFrame.NoFrame)
        self.protect_body.setStyleSheet("color: #DB6949")
        protect_v_body.addWidget(self.protect_body)

        protect_v.addWidget(protect_v_head_bg)
        protect_v.addWidget(protect_v_body_bg)

        otherStatus_groupBox_h.addLayout(error_v)
        otherStatus_groupBox_h.addLayout(warn_v)
        otherStatus_groupBox_h.addLayout(protect_v)

        otherStatus_groupBox.setLayout(otherStatus_groupBox_h)

        # 开关控制
        openStatus_groupBox = QGroupBox(group_tabel6)
        openStatus_groupBox.setStyleSheet(white_bg)
        openStatus_groupBox_grid = QGridLayout()

        # 充电
        self.charge_sw = SwitchButton()
        self.charge_sw.setEnabled(False)
        self.charge_sw.setOnText(switch_label1)
        self.charge_sw.setOffText(switch_label1)

        # 放电
        self.disCharge_sw = SwitchButton()
        self.disCharge_sw.setEnabled(False)
        self.disCharge_sw.setOnText(switch_label2)
        self.disCharge_sw.setOffText(switch_label2)
        
        # 蜂鸣器开关
        self.buzzer_sw = SwitchButton()
        self.buzzer_sw.setOnText('蜂鸣器')
        self.buzzer_sw.setOffText('蜂鸣器')

        # 强制休眠
        self.dormancy_sw = PushButton(switch_label3)
        
        # 测试模式
        self.testmode_btn = PushButton('进入测试模式')
        self.testmode_btn.setEnabled(False)

        og = [
            self.buzzer_sw, self.charge_sw, self.disCharge_sw, self.testmode_btn, self.dormancy_sw
        ]
        og_positions = [(i, j) for i in range(1) for j in range(6)]
        for positions, og in zip(og_positions, og):
            # if og != '':
            openStatus_groupBox_grid.addWidget(og, *positions)
        openStatus_groupBox.setLayout(openStatus_groupBox_grid)

        # 电池信息
        battery_groupBox.setLayout(bat_v)
        tab1_layout_left_top_left.addWidget(battery_groupBox)
        tab1_layout_left_top.addLayout(tab1_layout_left_top_left)

        # 温度信息
        tem_h.addWidget(tem_form1_bg)
        tem_h.addWidget(tem_form2_bg)
        tem_h.addLayout(tem_form3)
        temperature_groupBox.setLayout(tem_h)
        tab1_layout_left_top_right.addWidget(temperature_groupBox)
        tab1_layout_left_top.addLayout(tab1_layout_left_top_right)
        tab1_layout_left.addLayout(tab1_layout_left_top)

        # 单体电压
        vol_V.addLayout(vol_V_H1)
        vol_V.addWidget(vol_V_H2_bg)

        voltage_groupBox.setLayout(vol_V)
        tab1_layout_left_mid.addWidget(voltage_groupBox)
        tab1_layout_left.addLayout(tab1_layout_left_mid)

        # 管理员登录
        tab1_layout_right_down = QHBoxLayout()
        login_groupBox = QGroupBox(group_tabel4)
        login_groupBox.setStyleSheet(white_bg)
        login_H = QHBoxLayout()

        pwd_label = QLabel(pwd_label1 + '：')
        pwd_label.setMaximumWidth(80)
        self.pwd_line = QLineEdit()
        self.pwd_line.setEchoMode(QLineEdit.Password)
        self.pwd_btn = QPushButton(pwd_label2)
        self.pwd_btn.setStyleSheet(open_Button)
        login_H.addWidget(pwd_label)
        login_H.addWidget(self.pwd_line)
        login_H.addWidget(self.pwd_btn)

        login_groupBox.setLayout(login_H)
        tab1_layout_right_down.addWidget(login_groupBox)

        port_H.addLayout(port_grid)
        port_groupBox.setLayout(port_H)

        tab1_layout_right_top.addLayout(tab1_layout_right_down)  # 管理员登陆
        tab1_layout_right_top.addWidget(port_groupBox)          # 串口
        tab1_layout_right_top.addWidget(openStatus_groupBox)    # 开关控制
        tab1_layout_right_top.addWidget(sysStatus_groupBox)     # 系统状态
        tab1_layout_right_top.addWidget(otherStatus_groupBox)  # 其他状态

        tab1_layout_right.addLayout(tab1_layout_right_top)

        tab1_layout.addLayout(tab1_layout_left)
        tab1_layout.addLayout(tab1_layout_right)

        self.choice_init()
        self.tab_monitor.setLayout(tab1_layout)

    # 下拉框显示的数据
    def choice_init(self):
        baud_choice = ['9600', '19200', '57600', '115200']
        pack_choice = ['1', '2', '3', '4']
        space_choice = ['3', '2', '1']

        # 显示并选择COM口名称
        self.port_combobox.addItems(Common.load_serial_list())
        self.baud_combobox.addItems(baud_choice)
        self.pack_combobox.addItems(pack_choice)
        self.space_combobox.addItems(space_choice)

    # 实时数据
    def tab_dataUI(self):
        self.tableWidget = QTableWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout_H = QHBoxLayout()

        # self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)  # 3列
        self.tableWidget.setHorizontalHeaderLabels(
            ['Time', 'Direction', 'Send/Receive Data(Hex)'])
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 750)

        # 隐藏水平方向表格头
        self.tableWidget.verticalHeader().setVisible(False)

        self.clearRowbtn = QPushButton(realdata_label1)

        tab2_layout_H.addWidget(self.clearRowbtn)
        tab2_layout.addLayout(tab2_layout_H)
        tab2_layout.addWidget(self.tableWidget)
        self.tab_data.setLayout(tab2_layout)

    # 参数设置
    def tab_setParamsUI(self):
        tab3_layout = QVBoxLayout()
        tab3_layout_H1 = QHBoxLayout()
        self.tab3_form_dic = {}

        # 单体过充设置
        monVolWarn_groupBox = QGroupBox(parset_label1)
        monVolWarn_groupBox.setStyleSheet(white_bg)
        monVolWarn_form = self.tab3_createForm(
            self.tab3_form_dic, f'{parset1_label1}(V)', f'{parset1_label2}(V)', 
                                f'{parset1_label3}(V)', f'{parset1_label4}(mS)',
                                '单体过充告警延时(mS)', '单体过充告警恢复值(V)')
        monVolWarn_groupBox.setLayout(monVolWarn_form)

        # 单体过放设置
        monVolProt_groupBox = QGroupBox(parset_label2)
        monVolProt_groupBox.setStyleSheet(white_bg)
        monVolProt_form = self.tab3_createForm(
            self.tab3_form_dic, f'{parset2_label1}(V)', f'{parset2_label2}(V)', 
                                f'{parset2_label3}(V)', f'{parset2_label4}(mS)',
                                '单体过放告警延时(mS)', '单体过放告警恢复值(V)')
        monVolProt_groupBox.setLayout(monVolProt_form)

        # 总体过充设置
        allVolWarn_groupBox = QGroupBox(parset_label3)
        allVolWarn_groupBox.setStyleSheet(white_bg)
        allVolWarn_form = self.tab3_createForm(
            self.tab3_form_dic, f'{parset3_label1}(V)', f'{parset3_label2}(V)', 
                                f'{parset3_label3}(V)', f'{parset3_label4}(mS)',
                                '总体过充告警延时(mS)', '总体过充告警恢复值(V)')
        allVolWarn_groupBox.setLayout(allVolWarn_form)

        # 总体过放设置
        allVolProt_groupBox = QGroupBox(parset_label4)
        allVolProt_groupBox.setStyleSheet(white_bg)
        allVolProt_form = self.tab3_createForm(
            self.tab3_form_dic, f'{parset4_label1}(V)', f'{parset4_label2}(V)', 
                                f'{parset4_label3}(V)', f'{parset4_label4}(mS)',
                                '总体过放告警延时(mS)', '总体过放告警恢复值(V)')
        allVolProt_groupBox.setLayout(allVolProt_form)

        tab3_layout_H1.addWidget(monVolWarn_groupBox)   # 单体过充设置
        tab3_layout_H1.addWidget(monVolProt_groupBox)   # 单体过放设置
        tab3_layout_H1.addWidget(allVolWarn_groupBox)   # 总体过充设置
        tab3_layout_H1.addWidget(allVolProt_groupBox)   # 总体过放设置

        tab3_layout_H2 = QHBoxLayout()
        # 高温设置
        temWarn_groupBox = QGroupBox(parset_label5)
        temWarn_groupBox.setStyleSheet(white_bg)
        temWarn_form = self.tab3_createForm(self.tab3_form_dic,
                                            f'{parset5_label1}(℃)', f'{parset5_label2}(℃)', f'{parset5_label3}(℃)',
                                            f'{parset5_label4}(℃)', f'{parset5_label5}(℃)', f'{parset5_label6}(℃)',
                                            f'{parset5_label7}(V)', f'{parset5_label8}(mV)', f'{parset5_label9}(V)', 
                                            f'{parset5_label10}(min)'
                                            )
        temWarn_groupBox.setLayout(temWarn_form)

        # 低温设置
        temProt_groupBox = QGroupBox(parset_label6)
        temProt_groupBox.setStyleSheet(white_bg)
        temProt_form = self.tab3_createForm(self.tab3_form_dic,
                                            f'{parset6_label1}(℃)', f'{parset6_label2}(℃)', f'{parset6_label3}(℃)',
                                            f'{parset6_label4}(℃)', f'{parset6_label5}(℃)', f'{parset6_label6}(℃)',
                                            f'{parset6_label7}(V)', f'{parset6_label8}(A)', f'{parset6_label9}(%)'
                                            )
        temProt_groupBox.setLayout(temProt_form)

        # 放电过流设置
        ecProt_groupBox = QGroupBox(parset_label7)
        ecProt_groupBox.setStyleSheet(white_bg)
        ecProt_form = self.tab3_createForm(self.tab3_form_dic,
                                           f'{parset7_label1}(A)', f'{parset7_label2}(A)', 
                                           f'{parset7_label3}(mS)', f'{parset7_label4}(A)', 
                                           f'{parset7_label5}(mS)', '放电过流告警延时(mS)',
                                           '放电过流告警恢复值(V)')
        ecProt_groupBox.setLayout(ecProt_form)

        # 充电过流设置
        ecWarn_groupBox = QGroupBox(parset_label8)
        ecWarn_groupBox.setStyleSheet(white_bg)
        ecWarn_form = self.tab3_createForm(self.tab3_form_dic,
                                           f'{parset8_label1}(A)', f'{parset8_label2}(A)', 
                                           f'{parset8_label3}(mS)', f'{parset8_label4}(A)', 
                                           f'{parset8_label5}(mS)', '充电过流告警延时(mS)',
                                           '充电过流告警恢复值(V)')
        ecWarn_groupBox.setLayout(ecWarn_form)

        tab3_layout_H2.addWidget(temWarn_groupBox)   # 高温设置
        tab3_layout_H2.addWidget(temProt_groupBox)   # 低温设置
        tab3_layout_H2.addWidget(ecProt_groupBox)   # 放电过流设置
        tab3_layout_H2.addWidget(ecWarn_groupBox)   # 充电过流设置

        tab3_layout_H3_bg = QWidget()
        tab3_layout_H3_bg.setMaximumHeight(50)
        tab3_layout_H3_bg.setStyleSheet(white_bg)
        tab3_layout_H3 = QHBoxLayout(tab3_layout_H3_bg)
        self.getTab3Res = QPushButton(parset9_label1)
        self.clsTab3Res = QPushButton(parset9_label2)
        self.writeParam = QPushButton(parset9_label3)
        self.writeParam.setEnabled(False)
        self.resetTab3 = QPushButton(parset9_label4)
        self.resetTab3.setEnabled(False)
        # self.importParam = QPushButton('导入参数(不可用)')
        # self.importParam.setEnabled(False)
        self.deriveParam = QPushButton(parset9_label5)
        self.deriveParam.setEnabled(False)

        tab3_layout_H3.addWidget(self.getTab3Res)   # 读取参数
        tab3_layout_H3.addWidget(self.clsTab3Res)   # 清屏
        tab3_layout_H3.addWidget(self.writeParam)   # 写入参数
        tab3_layout_H3.addWidget(self.resetTab3)   # 恢复默认值
        # tab3_layout_H3.addWidget(self.importParam)   # 导入参数
        tab3_layout_H3.addWidget(self.deriveParam)   # 导出参数

        tab3_layout.addLayout(tab3_layout_H1)
        tab3_layout.addLayout(tab3_layout_H2)
        tab3_layout.addWidget(tab3_layout_H3_bg)
        self.tab_setParams.setLayout(tab3_layout)

    # 创建Form布局
    def tab3_createForm(self, form_dic: dict, *args):
        formName = QFormLayout()
        temp_dic = {}
        for i in args:
            temp_dic[i] = QLineEdit()
            temp_dic[i].setStyleSheet('border: 1px solid #dcd8d8;')
        for k, v in temp_dic.items():
            temp_dic[k].setAlignment(Qt.AlignCenter)

            formName.addRow(k, v)
        form_dic.update(temp_dic)
        return formName

    # 历史数据
    def tab_hisdataUI(self):
        tab4_layout = QVBoxLayout()
        tab4_layout_table = QVBoxLayout()
        tab4_layout_table_btn_H = QHBoxLayout()
        self.hisShow = QPushButton(hisdata_label1)
        self.export_history = QPushButton('导出历史记录')
        self.export_history.setEnabled(False)
        self.clearShow = QPushButton(hisdata_label2)
        self.clearShow.setEnabled(False)
        self.hisTable = TableWidget()

        self.cloumn_name = self.json_modbus[bms_history]
        self.hisTable.setColumnCount(len(self.cloumn_name))
        # self.hisTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 不可编辑
        # 载入表头字段
        self.hisTable.setHorizontalHeaderLabels(
            [k for k, v in self.cloumn_name.items()])
        # 根据字段长度自动适配表头宽度
        for i in range(len(self.cloumn_name.items())):
            self.hisTable.resizeColumnToContents(i)
        self.hisTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # self.hisTable.setColumnWidth(0,150)     # 时间
        # self.hisTable.setColumnWidth(41,150)    # PACK+/-温度(最高)(℃)

        tab4_layout_table_btn_H.addWidget(self.hisShow)
        tab4_layout_table_btn_H.addWidget(self.export_history)
        tab4_layout_table_btn_H.addWidget(self.clearShow)

        tab4_layout_table.addLayout(tab4_layout_table_btn_H)
        tab4_layout_table.addWidget(self.hisTable)
        tab4_layout.addLayout(tab4_layout_table)
        self.tab_hisdata.setLayout(tab4_layout)
