# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtCore, QtWidgets, QtCore

# 导入 Qt designer 设计的页面
from .hello import Ui_MainWindow as Hello_Ui
from .a_layout import Ui_MainWindow as A_Ui
from .b_layout import Ui_MainWindow as B_Ui

# 主窗口
class HelloWindow(QtWidgets.QMainWindow, Hello_Ui):
    switch_window1 = QtCore.pyqtSignal() # 跳转信号
    switch_window2 = QtCore.pyqtSignal() # 跳转信号
    def __init__(self):
        super(HelloWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.goOperate)
        self.pushButton_2.clicked.connect(self.goLogin)
    def goLogin(self):
        self.switch_window1.emit()
    def goOperate(self):
        self.switch_window2.emit()

# A窗口
class LoginWindow(QtWidgets.QMainWindow, A_Ui):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)

# B窗口
class OperateWindow(QtWidgets.QMainWindow, B_Ui):
    def __init__(self):
        super(OperateWindow, self).__init__()
        self.setupUi(self)
