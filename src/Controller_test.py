# -*- coding: utf-8 -*-

from .MainWindow import MainWindow
from .AcCharge import AcLayout
from .Inverter import InvLayout
# from .BMS import Portbms as BmsLayout


class Controller(object):
    def __init__(self):
        pass
    
    # 主菜单
    def show_main_menu(self):
        self.main_window = MainWindow()
        self.main_window.switch_ac_charge.connect(self.show_ac_layout)
        self.main_window.switch_inverter.connect(self.show_inv_layout)
        # self.main_window.switch_bms.connect(self.show_bms_layout)
        self.main_window.show()
    
    # 跳转 AC充电器
    def show_ac_layout(self):
        self.ac_layout = AcLayout()
        self.main_window.close()
        self.ac_layout.show()
        
    # 跳转 逆变器
    def show_inv_layout(self):
        self.inv_layout = InvLayout()
        self.main_window.close()
        self.inv_layout.show()
    
    # 跳转 bms
    # def show_bms_layout(self):
    #     self.bms_layout = BmsLayout()
    #     self.main_window.close()
    #     self.bms_layout.show()