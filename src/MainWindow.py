# -*- coding: utf-8 -*-

import os, locale, functools
from PyQt5 import QtCore, QtWidgets, QtCore
from PyQt5.QtCore import QSettings
from ui.main_meun import Ui_MainWindow as main_menu
from .update.update import download_update_from_url
from .QssStyle import *


class MainWindow(QtWidgets.QMainWindow, main_menu):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        # self.setWindowTitle('11111')
        
        print(f'当前版本：{self.windowTitle()}')
        
        self.trans = QtCore.QTranslator()  # 实例翻译者
        
        # 设置项的保存路径
        set_dir = os.path.join(os.getcwd(), 'settings', 'settings.ini')
        self.setting = QSettings(set_dir, QSettings.IniFormat)

        # 跟随系统语言切换对应的语言包
        lang = locale.getdefaultlocale()[0]
        self.change_language(lang)
        
        self.lang_en.triggered.connect(functools.partial(self.change_language, 'en_US'))
        self.lang_zh.triggered.connect(functools.partial(self.change_language, 'zh_CN'))
        
        self.acchargerBtn.clicked.connect(self.goAcCharger) # 跳转AC充电器
        self.acchargerBtn.enterEvent = self.ac_enEvent
        self.acchargerBtn.leaveEvent = self.ac_leEvent
        
        self.dcchargerBtn.clicked.connect(self.goDcCharger) # 跳转DC充电器
        self.dcchargerBtn.enterEvent = self.dc_enEvent
        self.dcchargerBtn.leaveEvent = self.dc_leEvent
        
        self.InverterBtn.clicked.connect(self.goInverter) # 跳转逆变器
        self.InverterBtn.enterEvent = self.inv_enEvent
        self.InverterBtn.leaveEvent = self.inv_leEvent
        
        self.bmsBtn.clicked.connect(self.goBms) # 跳转BMS
        self.bmsBtn.enterEvent = self.bms_enEvent
        self.bmsBtn.leaveEvent = self.bms_leEvent
        
        # self.update_version()
    
    def ac_enEvent(self, event):
        self.ac_bg.setStyleSheet(main_ac_bg_ent_event)
        self.ac_text.setStyleSheet(main_ac_txt_ent_event)
            
    def ac_leEvent(self, event):
        self.ac_bg.setStyleSheet(main_ac_bg_lev_event)
        self.ac_text.setStyleSheet(main_ac_txt_lev_event)
            
    def dc_enEvent(self, event):
        self.dc_bg.setStyleSheet(main_ac_bg_ent_event)
        self.dc_text.setStyleSheet(main_ac_txt_ent_event)
            
    def dc_leEvent(self, event):
        self.dc_bg.setStyleSheet(main_ac_bg_lev_event)
        self.dc_text.setStyleSheet(main_ac_txt_lev_event)
        
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
        
    def goAcCharger(self):
        from .AcCharge import AcLayout
        self.ac_layout = AcLayout()
        self.close()
        self.ac_layout.show()

    def goDcCharger(self):
        from .DcCharger import DCLayout
        self.dc_layout = DCLayout()
        self.close()
        self.dc_layout.show()

    def goInverter(self):
        from .Inverter_pf_off import Invt_pf_off_layout
        self.inv_layout = Invt_pf_off_layout()
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

    # 版本更新
    def update_version(self):
        
        set_dir = os.path.join(os.getcwd(), 'settings', 'dynamic.ini')
        setting = QSettings(set_dir, QSettings.IniFormat)
        
        temp_file = os.path.join(os.getcwd(), 'update', 'update.zip')
        
        download_update_from_url(setting.value('url'), temp_file)
        
        print(setting.value('version'))
        print(setting.value('url'))
        