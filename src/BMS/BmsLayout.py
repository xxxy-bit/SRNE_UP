#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial.tools.list_ports, json, os, gettext
from PyQt5.QtWidgets import QProgressBar, QTableWidget, QLineEdit, QTabWidget, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton, QLabel, QGridLayout, QTextBrowser, QComboBox, QFormLayout
from PyQt5.QtCore import Qt, QSettings
from .QssStyle import *
from src.OrderList import *


class BmsLayout(QWidget):

    def __init__(self):
        super().__init__()
        
    def initUI(self):
        
        with open(os.path.join(os.getcwd(), 'settings', 'MODBUS.json'), 'r', encoding='utf-8') as f:
            self.json_modbus = json.load(f)
            
        with open(os.path.join(os.getcwd(), 'settings', 'RS485.json'), 'r', encoding='utf-8') as f:
            self.json_rs485 = json.load(f)
        
        # 加载中英文
        self.bms_i18n()
        
        self.setWindowTitle('Portbms v1.2.1')
        self.resize(1000, 765)   # 可拉伸
        # self.setFixedSize(1800, 950)   # 固定界面大小，不可拉伸
        
        # 外层
        self.V_layout = QVBoxLayout()
        self.V_layout.setContentsMargins(0, 0, 0, 0)

        self.tabWidget = QTabWidget()
        self.tab_monitor = QWidget()
        self.pal_monitor =  QWidget()
        self.tab_data = QWidget()
        self.tab_setParams = QWidget()
        self.sys_seting = QWidget()
        self.tab_hisdata = QWidget()
        
        self.tabWidget.addTab(self.tab_monitor,self.tab_tabel1)
        self.tabWidget.addTab(self.pal_monitor,self.tab_tabel2)
        self.tabWidget.addTab(self.tab_setParams,self.tab_tabel3)
        self.tabWidget.addTab(self.sys_seting,self.tab_tabel4)
        self.tabWidget.addTab(self.tab_hisdata,self.tab_tabel5)
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
        
    # bms i18n 中英切换
    def bms_i18n(self):
        set_dir = os.path.join(os.getcwd(), 'settings', 'settings.ini')
        setting = QSettings(set_dir, QSettings.IniFormat)
        
        lang_zh = gettext.translation('Bms', localedir=os.path.join(os.getcwd(), 'locales'), languages=[setting.value('language')])
        lang_zh.install('Bms')
        _ = lang_zh.gettext
        
        # 选项卡
        self.tab_tabel1 = _('实时监控')
        self.tab_tabel2 = _('并机监控')
        self.tab_tabel3 = _('参数设置')
        self.tab_tabel4 = _('系统设置')
        self.tab_tabel5 = _('历史数据')
        self.tab_tabel6 = _('实时数据')
        
        # 实时监控页
        # 组名称
        self.group_tabel1 = _('电池信息')
        self.group_tabel2 = _('温度信息')
        self.group_tabel3 = _('单体电压')
        self.group_tabel4 = _('管理员登录')
        self.group_tabel55 = _('串口信息')
        self.group_tabel5 = _('串口')
        self.group_tabel6 = _('开关控制')
        self.group_tabel7 = _('系统状态')
        self.group_tabel8 = _('故障状态')
        self.group_tabel9 = _('告警状态')
        self.group_tabel10 = _('保护状态')
        
        # 电池信息
        self.battery_label1 = _('Pack电池电压')
        self.battery_label2 = _('Pack电池电流')
        self.battery_label3 = _('剩余容量')
        self.battery_label4 = _('充满容量')
        self.battery_label5 = _('循环次数')
        
        # 温度信息
        self.temp_label19 = _('环境温度')
        self.temp_label20 = _('Pack正极端子温度')
        self.temp_label21 = _('Pack负极端子温度')
        self.temp_label22 = _('Pack端子温度3')
        self.temp_label23 = _('Pack端子温度4')
        self.temp_label24 = _('Mos管1温度')
        self.temp_label25 = _('Mos管2温度')
        
        # 单体电压
        self.vol_label17 = _('cell最大压差')
        self.vol_label18 = _('cell最大电压')
        self.vol_label19 = _('cell最小电压')
        
        # 管理员登录
        self.pwd_label1 = _('密码')
        self.pwd_label2 = _('确定')
    
        # 串口
        self.com_label2 = _('波特率')
        self.com_label3 = _('Pack数量')
        self.com_label4 = _('地址')
        self.com_label5 = _('间隔（秒）')
        self.com_label6 = _('打开串口')
        self.com_label8 = _('开始监控')
        
        # 开关控制
        self.switch_label1 = _('充电')
        self.switch_label2 = _('放电')
        self.switch_label3 = _('强制休眠')
        self.switch_label4 = _('打开')
    
        # 系统状态
        self.sys_label1 = _('有效充电电流')
        self.sys_label2 = _('有效放电电流')
        self.sys_label3 = _('充电MOS管开启')
        self.sys_label4 = _('放电MOS管开启')
        self.sys_label5 = _('充电器接入')
        self.sys_label6 = _('满充')
        
        # 并机监控页
        # 组名称
        self.pal_label1 = _('并联连接')
        self.pal_label2 = _('报警状态')
        self.pal_label3 = _('并联数据')
        self.pal_label4 = _('电芯数据')

        # 并联设置
        self.palset_label1 = _('Pack 数量')
        self.palset_label2 = _('获取数据')
        
        # 报警状态
        self.error_label1 = _('充电状态')
        self.error_label2 = _('放电状态')
        self.error_label3 = _('总高压报警')
        self.error_label4 = _('总低压报警')
        
        # 并联数据
        self.paldata_label1 = _('平均电压')
        self.paldata_label2 = _('平均SOC')
        self.paldata_label3 = _('总电流')
        
        # 电芯数据
        self.celldata_label1 = _('最高电芯电压')
        self.celldata_label2 = _('最高电芯电压位置')
        self.celldata_label3 = _('最低电芯电压')
        self.celldata_label4 = _('最低电芯电压位置')
        self.celldata_label5 = _('最高电芯温度')
        self.celldata_label6 = _('最高电芯温度位置')
        self.celldata_label7 = _('最低电芯温度')
        self.celldata_label8 = _('最低电芯温度位置')
        
        # 并机数据
        self.palnum_label1 = _('电压')
        self.palnum_label2 = _('温度')
        self.palnum_label3 = _('PACK电流')
        self.palnum_label7 = _('充放电循环次数')
        self.palnum_label8 = _('PACK设计容量')
        self.palnum_label9 = _('告警')
        self.palnum_label10 = _('PACK充电电流告警')
        self.palnum_label11 = _('PACK总电压告警')
        self.palnum_label12 = _('PACK放电电流告警')
        self.palnum_label14 = _('指示状态')
        self.palnum_label15 = _('控制状态')
        self.palnum_label16 = _('均衡状态')
        
        # 参数设置页
        # 组名称
        self.parset_label1 = _('单体过充设置')
        self.parset_label2 = _('单体过放设置')
        self.parset_label3 = _('总体过充设置')
        self.parset_label4 = _('总体过放设置')
        self.parset_label5 = _('高温设置')
        self.parset_label6 = _('低温设置')
        self.parset_label7 = _('放电过流设置')
        self.parset_label8 = _('充电过流设置')
        
        # 单体过充设置
        self.parset1_label1 = _('单体过充告警')
        self.parset1_label2 = _('单体过充保护')
        self.parset1_label3 = _('单体过充保护恢复')
        self.parset1_label4 = _('单体过充保护延时')
        
        # 单体过放设置
        self.parset2_label1 = _('单体过放告警')
        self.parset2_label2 = _('单体过放保护')
        self.parset2_label3 = _('单体过放保护恢复')
        self.parset2_label4 = _('单体过放保护延时')
        
        # 总体过充设置
        self.parset3_label1 = _('总体过充告警')
        self.parset3_label2 = _('总体过充保护')
        self.parset3_label3 = _('总体过充保护恢复')
        self.parset3_label4 = _('总体过充保护延时')
        
        # 总体过放设置
        self.parset4_label1 = _('总体过放告警')
        self.parset4_label2 = _('总体过放保护')
        self.parset4_label3 = _('总体过放保护恢复')
        self.parset4_label4 = _('总体过放保护延时')
    
        # 高温设置
        self.parset5_label1 = _('充电高温告警')
        self.parset5_label2 = _('充电高温保护')
        self.parset5_label3 = _('充电高温保护恢复')
        self.parset5_label4 = _('放电高温告警')
        self.parset5_label5 = _('放电高温保护')
        self.parset5_label6 = _('放电高温保护恢复')
        self.parset5_label7 = _('均衡开启电压')
        self.parset5_label8 = _('均衡开启压差')
        self.parset5_label9 = _('单体休眠电压')
        self.parset5_label10 = _('单体休眠延时')
    
        # 低温设置
        self.parset6_label1 = _('充电低温告警')
        self.parset6_label2 = _('充电低温保护')
        self.parset6_label3 = _('充电低温保护恢复')
        self.parset6_label4 = _('放电低温告警')
        self.parset6_label5 = _('放电低温保护')
        self.parset6_label6 = _('放电低温保护恢复')
        self.parset6_label7 = _('电池包截止电压')
        self.parset6_label8 = _('电池包截止电流')
        self.parset6_label9 = _('低电量告警')
    
        # 放电过流设置
        self.parset7_label1 = _('放电过流告警')
        self.parset7_label2 = _('放电过流保护1')
        self.parset7_label3 = _('放电过流保护延时1')
        self.parset7_label4 = _('放电过流保护2')
        self.parset7_label5 = _('放电过流保护延时2')
        self.parset7_label6 = _('短路保护延时')
    
        # 充电过流设置
        self.parset8_label1 = _('充电过流告警')
        self.parset8_label2 = _('充电过流保护1')
        self.parset8_label3 = _('充电过流保护延时1')
        self.parset8_label4 = _('充电过流保护2')
        self.parset8_label5 = _('充电过流保护延时2')
        
        # 按钮
        self.parset9_label1 = _('读取参数')
        self.parset9_label2 = _('清屏')
        self.parset9_label3 = _('写入参数')
        self.parset9_label4 = _('恢复默认值')
        self.parset9_label5 = _('导出参数')
        
        # 系统设置页
        self.sysset_label1 = _('电量')
        self.sysset_label2 = _('设计容量')
        self.sysset_label4 = _('总容量')
        self.sysset_label5 = _('读取')
        self.sysset_label6 = _('设置')
        
        # 历史数据页
        self.hisdata_label1 = _('获取最近历史数据(1~100)')
        self.hisdata_label2 = _('擦除历史数据')
        
        # 实时数据页
        self.realdata_label1 = _('清空内容')
        
        # 底边栏
        self.ver_label1 = _('版本')
    
    # 并机监控
    def pal_monitorUI(self):
        # 最外层
        pal_layout = QVBoxLayout()
        
        # 上方
        pal_layout_top = QHBoxLayout()
        
        pal_sys_groupBox = QGroupBox(self.pal_label1)
        pal_sys_groupBox_grid = QGridLayout()
        
        self.pack_total = QComboBox()
        self.pack_total.addItems([str(i) for i in range(1, 16)])
        self.pal_start = QPushButton(self.palset_label2)
        
        ed4 = [
            QLabel(self.palset_label1 + '：'), self.pack_total,
            '', self.pal_start
        ]
        positions4 = [(i, j) for i in range(2) for j in range(2)]
        for positions4, ed4 in zip(positions4, ed4):
            if ed4 != '':
                pal_sys_groupBox_grid.addWidget(ed4, *positions4)
        
        pal_sys_groupBox.setLayout(pal_sys_groupBox_grid)
        pal_layout_top.addWidget(pal_sys_groupBox)
        
        status_groupBox = QGroupBox(self.pal_label2)
        status_groupBox_grid = QGridLayout()
        
        self.pal_char_status = QLabel('●' + self.error_label1)
        self.pal_dischar_status = QLabel('●' + self.error_label2)
        self.pal_higvol_status = QLabel('●' + self.error_label3)
        self.pal_lowvol_status = QLabel('●' + self.error_label4)
        
        ed3 = [
            self.pal_char_status,
            self.pal_dischar_status,
            self.pal_higvol_status,
            self.pal_lowvol_status
        ]
        positions3 = [(i, j) for i in range(4) for j in range(1)]
        for positions3, ed3 in zip(positions3, ed3):
            status_groupBox_grid.addWidget(ed3, *positions3)
        
        status_groupBox.setLayout(status_groupBox_grid)
        pal_layout_top.addWidget(status_groupBox)
        
        data_groupBox = QGroupBox(self.pal_label3)
        data_groupBox_grid = QGridLayout()
        self.avg_voltage = QLineEdit()
        self.avg_soc = QLineEdit()
        self.total_elc = QLineEdit()
        self.sur_cap = QLineEdit()
        self.full_cap = QLineEdit()
        self.soh = QLineEdit()
        self.loop_num = QLineEdit()
        
        ed = [
            QLabel(self.paldata_label1 + '(V)：'), self.avg_voltage ,QLabel(self.battery_label3 + '(AH)：'), self.sur_cap,
            QLabel(self.paldata_label2 + '(%)：'), self.avg_soc ,QLabel(self.battery_label4 + '(AH)：'), self.full_cap,
            QLabel(self.paldata_label3 + '(V)：'), self.total_elc ,QLabel('SOH(AH)：'), self.soh,
            '','',QLabel(self.battery_label1 + '：'), self.loop_num
        ]
        positions = [(i, j) for i in range(4) for j in range(4)]
        for positions, ed in zip(positions, ed):
            if ed != '':
                data_groupBox_grid.addWidget(ed, *positions)

        data_groupBox.setLayout(data_groupBox_grid)
        pal_layout_top.addWidget(data_groupBox)
        
        celldata_groupBox = QGroupBox(self.pal_label4)
        celldata_groupBox_grid = QGridLayout()
        self.cell_max = QLineEdit()
        self.cell_max_posi = QLineEdit()
        self.cell_min = QLineEdit()
        self.cell_min_posi = QLineEdit()
        
        self.cell_max_tmp = QLineEdit()
        self.cell_max_tmp_posi = QLineEdit()
        self.cell_min_tmp = QLineEdit()
        self.cell_min_tmp_posi = QLineEdit()
        
        ed2 = [
            QLabel(self.celldata_label1 + '(mV)：'), self.cell_max ,QLabel(self.celldata_label5 + '(%)：'), self.cell_max_tmp,
            QLabel(self.celldata_label2 + '：'), self.cell_max_posi ,QLabel(self.celldata_label6 + '：'), self.cell_max_tmp_posi,
            QLabel(self.celldata_label3 + '(mV)：'), self.cell_min ,QLabel(self.celldata_label7 + '(%)：'), self.cell_min_tmp,
            QLabel(self.celldata_label4 + '：'), self.cell_min_posi,QLabel(self.celldata_label8 + '：'), self.cell_min_tmp_posi
        ]
        positions2 = [(i, j) for i in range(4) for j in range(4)]
        for positions2, ed2 in zip(positions2, ed2):
            celldata_groupBox_grid.addWidget(ed2, *positions2)
        celldata_groupBox.setLayout(celldata_groupBox_grid)
        pal_layout_top.addWidget(celldata_groupBox)
        
        # 下方
        pal_layout_bottom = QHBoxLayout()
        self.palTable = QTableWidget()
        # self.palTable.setColumnCount(4)
        # self.palTable.setHorizontalHeaderLabels(['11','12','13','14'])
        self.col_labels = [
            'Cell' + self.palnum_label1 + '_1','Cell' + self.palnum_label1 + '_2','Cell' + self.palnum_label1 + '_3','Cell' + self.palnum_label1 + '_4',
            'Cell' + self.palnum_label1 + '_5','Cell' + self.palnum_label1 + '_6','Cell' + self.palnum_label1 + '_7','Cell' + self.palnum_label1 + '_8',
            'Cell' + self.palnum_label1 + '_9','Cell' + self.palnum_label1 + '_10','Cell' + self.palnum_label1 + '_11','Cell' + self.palnum_label1 + '_12',
            'Cell' + self.palnum_label1 + '_13','Cell' + self.palnum_label1 + '_14','Cell' + self.palnum_label1 + '_15','Cell' + self.palnum_label1 + '_16',
            self.palnum_label2 + '_1',self.palnum_label2 + '_2',self.palnum_label2 + '_3',self.palnum_label2 + '_4',self.palnum_label2 + '_5',
            self.palnum_label2 + '_6',self.palnum_label2 + '_7',self.palnum_label2 + '_8',self.palnum_label2 + '_9',
            self.palnum_label3,'PACK' + self.paldata_label3,'PACK' + self.battery_label3,'PACK' + self.battery_label4,
            self.palnum_label7, self.palnum_label8,'PACK SOC',
            'Cell' + self.palnum_label9 + '_1','Cell' + self.palnum_label9 + '_2','Cell' + self.palnum_label9 + '_3','Cell' + self.palnum_label9 + '_4',
            'Cell' + self.palnum_label9 + '_5','Cell' + self.palnum_label9 + '_6','Cell' + self.palnum_label9 + '_7','Cell' + self.palnum_label9 + '_8',
            'Cell' + self.palnum_label9 + '_9','Cell' + self.palnum_label9 + '_1','Cell' + self.palnum_label9 + '_11','Cell' + self.palnum_label9 + '_12',
            'Cell' + self.palnum_label9 + '_13','Cell' + self.palnum_label9 + '_14','Cell' + self.palnum_label9 + '_15','Cell' + self.palnum_label9 + '_16',
            self.palnum_label2 + self.palnum_label9 +  '_1',self.palnum_label2 + self.palnum_label9 + '_2',self.palnum_label2 + self.palnum_label9 + '_3',self.palnum_label2 + self.palnum_label9 + '_4',self.palnum_label2 + self.palnum_label9 + '_5',
            self.palnum_label2 + self.palnum_label9 + '_6' ,self.palnum_label2 + self.palnum_label9 + '_7',self.palnum_label2 + self.palnum_label9 + '_8',self.palnum_label2 + self.palnum_label9 + '_9',
            self.palnum_label10,self.palnum_label11,self.palnum_label12,f'{self.group_tabel10}_1',
            f'{self.group_tabel10}_2',self.palnum_label14,self.palnum_label15,self.group_tabel8,
            self.palnum_label16 + '_1',self.palnum_label16 + '_2',f'{self.group_tabel9}_1',f'{self.group_tabel9}_2',
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

        # 左边
        sys_layout_left = QVBoxLayout()
        
        elect_groupBox = QGroupBox(self.sysset_label1)
        elect_groupBox.setMaximumHeight(500)
        elect_groupBox.setMaximumWidth(500)
        elect_groupBox_grid = QGridLayout()

        self.designCap = QLineEdit()
        self.remainCap = QLineEdit()
        self.fullCap = QLineEdit()
        self.readCap = QPushButton(self.sysset_label5)
        self.writeCap = QPushButton(self.sysset_label6)
        self.writeCap.setEnabled(False)
        
        ed = [
            QLabel(f'{self.sysset_label2}(AH)：'), self.designCap,
            QLabel(self.battery_label3 + '(AH)：'), self.remainCap,
            QLabel(f'{self.sysset_label4}(AH)：'), self.fullCap,
            self.readCap, self.writeCap
        ]
        positions = [(i, j) for i in range(4) for j in range(2)]
        for positions, ed in zip(positions, ed):
            elect_groupBox_grid.addWidget(ed, *positions)
        
        elect_groupBox.setLayout(elect_groupBox_grid)
        sys_layout_left.addWidget(elect_groupBox)

        # 右边
        sys_layout_right = QVBoxLayout()

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
        self.version = QLabel(f'{self.ver_label1}:')
        # self.version.setAlignment(Qt.AlignLeft)
        self.bms_sn = QLabel('BMS S/N:')
        self.pack_sn = QLabel('PACK S/N:')
        self.connStatus = QProgressBar()
        self.connStatus.setStyleSheet(RED_ProgressBar)
        self.connStatus.setAlignment(Qt.AlignCenter)
        self.connStatus.setMaximumWidth(500)
        self.nowTime = QLabel()
        # self.nowTime.setAlignment(Qt.AlignCenter)

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
        tab1_layout_left_top = QHBoxLayout()

        # 左边-上-左：电池信息
        tab1_layout_left_top_left = QVBoxLayout()
        battery_groupBox = QGroupBox(self.group_tabel1)

        # 电池信息：竖布局
        bat_v = QVBoxLayout()
        battery_form = QFormLayout()
        self.bat_wd = {
            self.battery_label1:QLineEdit(),
            self.battery_label2:QLineEdit(),
            'SOC':QLineEdit(),
            'SOH':QLineEdit(),
            self.battery_label3:QLineEdit(),
            self.battery_label4:QLineEdit(),
            self.battery_label5:QLineEdit()
        }
        for k,v in self.bat_wd.items():
            self.bat_wd[k].setReadOnly(True)
            # 指定小部件最小宽度
            self.bat_wd[k].setMinimumWidth(90)
            self.bat_wd[k].setAlignment(Qt.AlignCenter)
            battery_form.addRow(k, v)

        # 左边-上-右：温度信息
        tab1_layout_left_top_right = QVBoxLayout()
        temperature_groupBox = QGroupBox(self.group_tabel2)
        tem_h = QHBoxLayout()
        tem_form1 = QFormLayout()
        tem_form2 = QFormLayout()
        tem_form3 = QFormLayout()

        # 创建 cell温度 1~16 的对象
        self.cell_temp_8 = {}
        self.cell_temp_16 = {}
        
        for i in range(8):
            self.cell_temp_8[f'cell_{i+1}(℃)'] = QLineEdit()
        for k,v in self.cell_temp_8.items():
            self.cell_temp_8[k].setReadOnly(True)
            self.cell_temp_8[k].setAlignment(Qt.AlignCenter)
            tem_form1.addRow(k, v)

        for i in range(8, 16):
            self.cell_temp_16[f'cell_{i+1}(℃)'] = QLineEdit()
        for k,v in self.cell_temp_16.items():
            self.cell_temp_16[k].setReadOnly(True)
            self.cell_temp_16[k].setAlignment(Qt.AlignCenter)
            tem_form2.addRow(k, v)
        
        self.tem_other = {
            self.temp_label19 + '(℃)': QLineEdit(),
            self.temp_label20 + '(℃)': QLineEdit(),
            self.temp_label21 + '(℃)': QLineEdit(),
            self.temp_label22 + '(℃)': QLineEdit(),
            self.temp_label23 + '(℃)': QLineEdit(),
            self.temp_label24 + '(℃)': QLineEdit(),
            self.temp_label25 + '(℃)': QLineEdit()
        }
        for k,v in self.tem_other.items():
            self.tem_other[k].setReadOnly(True)
            self.tem_other[k].setAlignment(Qt.AlignCenter)
            tem_form3.addRow(k, v)

        # 左边-下
        tab1_layout_left_mid = QHBoxLayout()
        voltage_groupBox = QGroupBox(self.group_tabel3)
        vol_H = QHBoxLayout()
        vol_form1 = QFormLayout()
        vol_form2 = QFormLayout()
        vol_form3 = QFormLayout()

        self.cell_vol_8 = {}
        self.cell_vol_16 = {}
        
        for i in range(8):
            self.cell_vol_8[f'cell_{i+1}(V)'] = QLineEdit()
        for k,v in self.cell_vol_8.items():
            self.cell_vol_8[k].setReadOnly(True)
            self.cell_vol_8[k].setAlignment(Qt.AlignCenter)
            vol_form1.addRow(k, v)

        for i in range(8, 16):
            self.cell_vol_16[f'cell_{i+1}(V)'] = QLineEdit()
        for k,v in self.cell_vol_16.items():
            self.cell_vol_16[k].setReadOnly(True)
            self.cell_vol_16[k].setAlignment(Qt.AlignCenter)
            vol_form2.addRow(k, v)

        self.vol_other = {
            self.vol_label17 + '(V)': QLineEdit(),
            self.vol_label18 + '(V)': QLineEdit(),
            self.vol_label19 + '(V)': QLineEdit()
        }
        for k,v in self.vol_other.items():
            self.vol_other[k].setReadOnly(True)
            self.vol_other[k].setAlignment(Qt.AlignCenter)
            vol_form3.addRow(k, v)

        # # 右边
        tab1_layout_right = QVBoxLayout()

        # 右边-上
        tab1_layout_right_top = QVBoxLayout()
        port_groupBox = QGroupBox(self.group_tabel55)
        port_H = QHBoxLayout()
        port_grid = QGridLayout()

        self.port_combobox = QComboBox()
        self.baud_combobox = QComboBox()
        self.pack_combobox = QComboBox()
        self.pack_combobox.setEnabled(False)
        self.pack_num_line = QLineEdit()
        self.pack_num_line.setEnabled(False)
        self.address_line = QLineEdit()
        self.address_line.setEnabled(False)
        self.space_combobox = QComboBox()
        self.open_port_btn = QPushButton(self.com_label6)
        self.open_port_btn.setStyleSheet(color_close)
        self.getP01_data_btn = QPushButton(self.com_label8)
        self.getP01_data_btn.setStyleSheet(color_close)
        wd = [
            QLabel(self.group_tabel5 + ':'), self.port_combobox, QLabel(self.com_label2 + ':'), self.baud_combobox, self.open_port_btn,
            QLabel('Pack:'), self.pack_combobox, QLabel(self.com_label3 + ':'), self.pack_num_line, self.getP01_data_btn,
            QLabel(self.com_label4 + ':'), self.address_line, QLabel(self.com_label5 + ':'), self.space_combobox, ''
        ]
        positions = [(i,j) for i in range(3) for j in range(5)]
        for positions, wd in zip(positions, wd):
            if wd == '':
                continue
            port_grid.addWidget(wd, *positions)

        sysStatus_groupBox = QGroupBox(self.group_tabel7)
        sysStatus_groupBox_grid = QGridLayout()
        self.charg_status = QLabel('●' + self.sys_label1)
        self.disCharg_status = QLabel('●' + self.sys_label2)
        self.chargMos_status = QLabel('●' + self.sys_label3)
        self.disChargMos_status = QLabel('●' + self.sys_label4)
        self.batCharg_status = QLabel('●' + self.sys_label5)
        self.full_status = QLabel('●' + self.sys_label6)
        sg = [
            self.charg_status, self.chargMos_status, self.batCharg_status,
            self.disCharg_status, self.disChargMos_status, self.full_status
        ]
        sys_positions = [(i,j) for i in range(2) for j in range(3)]
        for positions, sg in zip(sys_positions, sg):
            sysStatus_groupBox_grid.addWidget(sg, *positions)
        sysStatus_groupBox.setLayout(sysStatus_groupBox_grid)

        warnStatus_groupBox = QGroupBox(self.group_tabel8)
        warnStatus_groupBox_hbox = QHBoxLayout()
        self.warn_status_txt = QTextBrowser()
        self.warn_status_txt.setStyleSheet('color:red')
        warnStatus_groupBox_hbox.addWidget(self.warn_status_txt)
        warnStatus_groupBox.setLayout(warnStatus_groupBox_hbox)

        protectStatus_groupBox = QGroupBox(self.group_tabel10)
        protectStatus_groupBox_hbox = QHBoxLayout()
        self.protect_status_txt = QTextBrowser()
        self.protect_status_txt.setStyleSheet('color:red')
        protectStatus_groupBox_hbox.addWidget(self.protect_status_txt)
        protectStatus_groupBox.setLayout(protectStatus_groupBox_hbox)

        errorStatus_groupBox = QGroupBox(self.group_tabel9)
        errorStatus_groupBox_hbox = QHBoxLayout()
        self.error_status_txt = QTextBrowser()
        self.error_status_txt.setStyleSheet('color:red')
        errorStatus_groupBox_hbox.addWidget(self.error_status_txt)
        errorStatus_groupBox.setLayout(errorStatus_groupBox_hbox)

        openStatus_groupBox = QGroupBox(self.group_tabel6)
        openStatus_groupBox_grid = QGridLayout()
        charge_lab = QLabel(self.switch_label1)
        charge_lab.setMaximumWidth(50)
        # charge_lab.setAlignment(Qt.AlignCenter)
        self.charge_btn = QPushButton(self.switch_label4)
        self.charge_btn.setEnabled(False)
        discharge_lab = QLabel(self.switch_label2)
        discharge_lab.setMaximumWidth(50)
        self.disCharge_btn = QPushButton(self.switch_label4)
        self.disCharge_btn.setEnabled(False)
        sleep_lab = QLabel(self.switch_label3)
        sleep_lab.setMaximumWidth(100)
        self.dormancy_btn = QPushButton(self.switch_label4)
        self.dormancy_btn.setStyleSheet(color_close)
        self.dormancy_btn.setEnabled(False)
        og = [
            charge_lab, self.charge_btn, discharge_lab, self.disCharge_btn, sleep_lab, self.dormancy_btn
        ]
        og_positions = [(i,j) for i in range(1) for j in range(6)]
        for positions, og in zip(og_positions, og):
            # if og != '':
            openStatus_groupBox_grid.addWidget(og, *positions)
        openStatus_groupBox.setLayout(openStatus_groupBox_grid)
        
        # 电池信息
        bat_v.addLayout(battery_form)
        battery_groupBox.setLayout(bat_v)
        tab1_layout_left_top_left.addWidget(battery_groupBox)
        tab1_layout_left_top.addLayout(tab1_layout_left_top_left)

        # 温度信息
        tem_h.addLayout(tem_form1)
        tem_h.addLayout(tem_form2)
        tem_h.addLayout(tem_form3)
        temperature_groupBox.setLayout(tem_h)
        tab1_layout_left_top_right.addWidget(temperature_groupBox)
        tab1_layout_left_top.addLayout(tab1_layout_left_top_right)
        tab1_layout_left.addLayout(tab1_layout_left_top)

        # 单体电压
        # vol_H.addStretch(2)
        vol_H.addLayout(vol_form1)
        vol_H.addLayout(vol_form2)
        vol_H.addLayout(vol_form3)
        # vol_H.addStretch(2)
        voltage_groupBox.setLayout(vol_H)
        tab1_layout_left_mid.addWidget(voltage_groupBox)
        tab1_layout_left.addLayout(tab1_layout_left_mid)
        
        # 登录验证
        tab1_layout_right_down = QHBoxLayout()
        login_groupBox = QGroupBox(self.group_tabel4)
        login_H = QHBoxLayout()
        
        pwd_label = QLabel(self.pwd_label1 + '：')
        pwd_label.setMaximumWidth(80)
        self.pwd_line = QLineEdit()
        self.pwd_line.setEchoMode(QLineEdit.Password)
        self.pwd_btn = QPushButton(self.pwd_label2)
        login_H.addWidget(pwd_label)
        login_H.addWidget(self.pwd_line)
        login_H.addWidget(self.pwd_btn)
        
        login_groupBox.setLayout(login_H)
        tab1_layout_right_down.addWidget(login_groupBox)

        port_H.addLayout(port_grid)
        port_groupBox.setLayout(port_H)
        
        tab1_layout_right_top.addLayout(tab1_layout_right_down) # 管理员登陆
        tab1_layout_right_top.addWidget(port_groupBox)          # 串口
        tab1_layout_right_top.addWidget(openStatus_groupBox)    # 开关控制
        tab1_layout_right_top.addWidget(sysStatus_groupBox)     # 系统状态
        tab1_layout_right_top.addWidget(warnStatus_groupBox)    # 故障状态
        tab1_layout_right_top.addWidget(errorStatus_groupBox)   # 告警状态
        tab1_layout_right_top.addWidget(protectStatus_groupBox) # 保护状态
        tab1_layout_right.addLayout(tab1_layout_right_top)

        tab1_layout.addLayout(tab1_layout_left)
        tab1_layout.addLayout(tab1_layout_right)

        self.choice_init()
        self.tab_monitor.setLayout(tab1_layout)

    # 下拉框显示的数据
    def choice_init(self):
        # 显示并选择COM口名称
        port_list = list(serial.tools.list_ports.comports())
        port_choice = [num.device for num in port_list]

        baud_choice = ['9600', '19200', '57600', '115200']
        pack_choice = ['1', '2', '3', '4']
        space_choice = ['3', '2', '1']

        self.port_combobox.addItems(port_choice)
        self.baud_combobox.addItems(baud_choice)
        self.pack_combobox.addItems(pack_choice)
        self.space_combobox.addItems(space_choice)

    # 实时数据
    def tab_dataUI(self):
        self.tableWidget = 	QTableWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout_H = QHBoxLayout()

        # self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)  # 3列
        self.tableWidget.setHorizontalHeaderLabels(['Time', 'Direction','Send/Receive Data(Hex)'])
        self.tableWidget.setColumnWidth(0,150)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,750)

        # 隐藏水平方向表格头
        self.tableWidget.verticalHeader().setVisible(False)

        self.clearRowbtn = QPushButton(self.realdata_label1)

        tab2_layout_H.addWidget(self.clearRowbtn)
        tab2_layout.addLayout(tab2_layout_H)
        tab2_layout.addWidget(self.tableWidget)
        self.tab_data.setLayout(tab2_layout)

    # 参数设置
    def tab_setParamsUI(self):
        tab3_layout = QVBoxLayout()
        tab3_layout_H1 = QHBoxLayout()
        self.tab3_form_dic = {}

        monVolWarn_groupBox = QGroupBox(self.parset_label1)
        monVolWarn_form = self.tab3_createForm(self.tab3_form_dic, f'{self.parset1_label1}(V)', f'{self.parset1_label2}(V)', f'{self.parset1_label3}(V)', f'{self.parset1_label4}(S)')
        monVolWarn_groupBox.setLayout(monVolWarn_form)

        monVolProt_groupBox = QGroupBox(self.parset_label2)
        monVolProt_form = self.tab3_createForm(self.tab3_form_dic, f'{self.parset2_label1}(V)', f'{self.parset2_label2}(V)', f'{self.parset2_label3}(V)', f'{self.parset2_label4}(S)')
        monVolProt_groupBox.setLayout(monVolProt_form)

        allVolWarn_groupBox = QGroupBox(self.parset_label3)
        allVolWarn_form = self.tab3_createForm(self.tab3_form_dic, f'{self.parset3_label1}(V)', f'{self.parset3_label2}(V)', f'{self.parset3_label3}(V)', f'{self.parset3_label4}(S)')
        allVolWarn_groupBox.setLayout(allVolWarn_form)

        allVolProt_groupBox = QGroupBox(self.parset_label4)
        allVolProt_form = self.tab3_createForm(self.tab3_form_dic, f'{self.parset4_label1}(V)', f'{self.parset4_label2}(V)', f'{self.parset4_label3}(V)', f'{self.parset4_label4}(S)')
        allVolProt_groupBox.setLayout(allVolProt_form)

        tab3_layout_H1.addWidget(monVolWarn_groupBox)   # 单体过充设置
        tab3_layout_H1.addWidget(monVolProt_groupBox)   # 单体过放设置
        tab3_layout_H1.addWidget(allVolWarn_groupBox)   # 总体过充设置
        tab3_layout_H1.addWidget(allVolProt_groupBox)   # 总体过放设置
        
        tab3_layout_H2 = QHBoxLayout()
        temWarn_groupBox = QGroupBox(self.parset_label5)
        temWarn_form = self.tab3_createForm(self.tab3_form_dic,
            f'{self.parset5_label1}(℃)', f'{self.parset5_label2}(℃)', f'{self.parset5_label3}(℃)', 
            f'{self.parset5_label4}(℃)', f'{self.parset5_label5}(℃)', f'{self.parset5_label6}(℃)',
            f'{self.parset5_label7}(V)', f'{self.parset5_label8}(mV)', f'{self.parset5_label9}(V)', f'{self.parset5_label10}(min)'
        )
        temWarn_groupBox.setLayout(temWarn_form)

        temProt_groupBox = QGroupBox(self.parset_label6)
        temProt_form = self.tab3_createForm(self.tab3_form_dic,
            f'{self.parset6_label1}(℃)', f'{self.parset6_label2}(℃)', f'{self.parset6_label3}(℃)',
            f'{self.parset6_label4}(℃)', f'{self.parset6_label5}(℃)', f'{self.parset6_label6}(℃)',
            f'{self.parset6_label7}(V)', f'{self.parset6_label8}(A)', f'{self.parset6_label9}(%)'
        )
        temProt_groupBox.setLayout(temProt_form)

        ecProt_groupBox = QGroupBox(self.parset_label7)
        ecProt_form = self.tab3_createForm(self.tab3_form_dic, 
            f'{self.parset7_label1}(A)', f'{self.parset7_label2}(A)', f'{self.parset7_label3}(S)', 
            f'{self.parset7_label4}(A)', f'{self.parset7_label5}(S)', f'{self.parset7_label6}(uS)')
        ecProt_groupBox.setLayout(ecProt_form)

        ecWarn_groupBox = QGroupBox(self.parset_label8)
        ecWarn_form = self.tab3_createForm(self.tab3_form_dic, 
            f'{self.parset8_label1}(A)', f'{self.parset8_label2}(A)', f'{self.parset8_label3}(S)', 
            f'{self.parset8_label4}(A)', f'{self.parset8_label5}(S)')
        ecWarn_groupBox.setLayout(ecWarn_form)

        tab3_layout_H2.addWidget(temWarn_groupBox)   # 高温设置
        tab3_layout_H2.addWidget(temProt_groupBox)   # 低温设置
        tab3_layout_H2.addWidget(ecProt_groupBox)   # 放电过流设置
        tab3_layout_H2.addWidget(ecWarn_groupBox)   # 充电过流设置

        tab3_layout_H3 = QHBoxLayout()
        self.getTab3Res = QPushButton(self.parset9_label1)
        self.clsTab3Res = QPushButton(self.parset9_label2)
        self.writeParam = QPushButton(self.parset9_label3)
        self.writeParam.setEnabled(False)
        self.resetTab3 = QPushButton(self.parset9_label4)
        self.resetTab3.setEnabled(False)
        # self.importParam = QPushButton('导入参数(不可用)')
        # self.importParam.setEnabled(False)
        self.deriveParam = QPushButton(self.parset9_label5)
        self.deriveParam.setEnabled(False)

        tab3_layout_H3.addWidget(self.getTab3Res)   # 读取参数
        tab3_layout_H3.addWidget(self.clsTab3Res)   # 清屏
        tab3_layout_H3.addWidget(self.writeParam)   # 写入参数
        tab3_layout_H3.addWidget(self.resetTab3)   # 恢复默认值
        # tab3_layout_H3.addWidget(self.importParam)   # 导入参数
        tab3_layout_H3.addWidget(self.deriveParam)   # 导出参数

        tab3_layout.addLayout(tab3_layout_H1)
        tab3_layout.addLayout(tab3_layout_H2)
        tab3_layout.addLayout(tab3_layout_H3)
        self.tab_setParams.setLayout(tab3_layout)
        
    # 创建Form布局
    def tab3_createForm(self, form_dic:dict, *args):
        formName = QFormLayout()
        temp_dic = {}
        for i in args:
            temp_dic[i] = QLineEdit()
        for k,v in temp_dic.items():
            temp_dic[k].setAlignment(Qt.AlignCenter)
            formName.addRow(k, v)
        form_dic.update(temp_dic)
        return formName

    # 历史数据
    def tab_hisdataUI(self):
        tab4_layout = QVBoxLayout()
        tab4_layout_table = QVBoxLayout()
        tab4_layout_table_btn_H = QHBoxLayout()
        self.hisShow = QPushButton(self.hisdata_label1)
        self.clearShow = QPushButton(self.hisdata_label2)
        self.hisTable = QTableWidget()
        
        cloumn_name = self.json_modbus['0103f0010036a71c']
        self.hisTable.setColumnCount(len(cloumn_name))
        # self.hisTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 不可编辑
        # self.hisTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 表头自适应
        self.hisTable.setHorizontalHeaderLabels([k for k,v in cloumn_name.items()])
        self.hisTable.setColumnWidth(0,150)     # 时间
        self.hisTable.setColumnWidth(41,150)    # PACK+/-温度(最高)(℃)
        
        tab4_layout_table_btn_H.addWidget(self.hisShow)
        tab4_layout_table_btn_H.addWidget(self.clearShow)
        
        tab4_layout_table.addLayout(tab4_layout_table_btn_H)
        tab4_layout_table.addWidget(self.hisTable)
        tab4_layout.addLayout(tab4_layout_table)
        self.tab_hisdata.setLayout(tab4_layout)


