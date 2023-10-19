# -*- coding: utf-8 -*-

import os, locale, functools
from PyQt5 import QtCore, QtWidgets, QtCore
from PyQt5.QtCore import QSettings
from ui.main_meun import Ui_MainWindow as main_menu
from .AcCharge import AcLayout
from .Inverter import InvLayout
from .QssStyle import *



class MainWindow(QtWidgets.QMainWindow, main_menu):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.trans = QtCore.QTranslator()  # 实例翻译者
        
        # 设置项的保存路径
        set_dir = os.path.join(os.getcwd(), 'settings', 'settings.ini')
        self.setting = QSettings(set_dir, QSettings.IniFormat)

        # 跟随系统语言切换对应的语言包
        lang = locale.getdefaultlocale()[0]
        self.change_language(lang)
        
        self.lang_en.triggered.connect(functools.partial(self.change_language, 'en_US'))
        self.lang_zh.triggered.connect(functools.partial(self.change_language, 'zh_CN'))
        
        # 隐藏 充电器 和 逆变器 的按钮，仅提供给bms使用
        # self.acchargeButton.hide()
        # self.InverterButton.hide()
        
        self.acchargeButton.clicked.connect(self.goAcCharge) # 跳转AC/DC充电器
        self.acchargeButton.enterEvent = self.ac_enEvent
        self.acchargeButton.leaveEvent = self.ac_leEvent
        
        self.InverterButton.clicked.connect(self.goInverter) # 跳转逆变器
        self.InverterButton.enterEvent = self.inv_enEvent
        self.InverterButton.leaveEvent = self.inv_leEvent
        
        self.bmsButton.clicked.connect(self.goBms) # 跳转BMS
        self.bmsButton.enterEvent = self.bms_enEvent
        self.bmsButton.leaveEvent = self.bms_leEvent
    
    def ac_enEvent(self, event):
        self.ac_bg.setStyleSheet(main_ac_bg_ent_event)
        self.ac_text.setStyleSheet(main_ac_txt_ent_event)
            
    def ac_leEvent(self, event):
        self.ac_bg.setStyleSheet(main_ac_bg_lev_event)
        self.ac_text.setStyleSheet(main_ac_txt_lev_event)
            
    def bms_enEvent(self, event):
        self.bms_bg.setStyleSheet(main_ac_bg_ent_event)
        self.bms_text.setStyleSheet(main_ac_txt_ent_event)
            
    def bms_leEvent(self, event):
        self.bms_bg.setStyleSheet(main_ac_bg_lev_event)
        self.bms_text.setStyleSheet(main_ac_txt_lev_event)

    def inv_enEvent(self, event):
        self.inverter_bg.setStyleSheet(main_ac_bg_ent_event)
        self.inverter_text.setStyleSheet(main_ac_txt_ent_event)
            
    def inv_leEvent(self, event):
        self.inverter_bg.setStyleSheet(main_ac_bg_lev_event)
        self.inverter_text.setStyleSheet(main_ac_txt_lev_event)
        
    def goAcCharge(self):
        self.ac_layout = AcLayout()
        self.close()
        self.ac_layout.show()

    def goInverter(self):
        self.inv_layout = InvLayout()
        self.close()
        self.inv_layout.show()

    def goBms(self):
        from .BMS.Portbms import Portbms
        self.bms_layout = Portbms()
        self.close()
        self.bms_layout.show()

    # 切换语言
    def change_language(self, langauge):
        """
        langauge: en_US , zh_CN
        """
        if langauge != 'zh_CN':
            langauge = 'en_US'
        self.setting.setValue("language", langauge)
        self.setting.sync()
            
        qm = os.getcwd() + f'\\ui\\{langauge}.qm'
        self.trans.load(qm)   # 读取qm语言包
        _app = QtWidgets.QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)