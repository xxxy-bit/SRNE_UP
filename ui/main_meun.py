# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\svn\SrneUpperComputer\ui\main_meun.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 689)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/硕日logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QtCore.QSize(111, 32))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(0, 0, 1000, 689))
        self.listView.setStyleSheet("background-image:url(:/背景.png)")
        self.listView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView.setObjectName("listView")
        self.listView_2 = QtWidgets.QListView(self.centralwidget)
        self.listView_2.setGeometry(QtCore.QRect(55, 134, 891, 436))
        self.listView_2.setStyleSheet("background-image:url(:/选择连接设备框.png)")
        self.listView_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView_2.setObjectName("listView_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(390, 111, 231, 61))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet("background: transparent;\n"
"font-size: 32px;\n"
"font-family: \"微软雅黑\";\n"
"color:#F37C00;")
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(64, 180, 871, 380))
        self.scrollArea.setStyleSheet("background: transparent;")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 854, 650))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 650))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.ac_bg = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.ac_bg.setGeometry(QtCore.QRect(72, 60, 200, 244))
        self.ac_bg.setStyleSheet("background-color:#FEFEFE;\n"
"border: 1px solid #E8E8E8;\n"
"border-top-left-radius:10px;\n"
"border-top-right-radius:10px;\n"
"border-bottom-left-radius:10px;\n"
"border-bottom-right-radius:10px;")
        self.ac_bg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ac_bg.setViewMode(QtWidgets.QListView.ListMode)
        self.ac_bg.setObjectName("ac_bg")
        self.ac_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ac_text.setGeometry(QtCore.QRect(108, 240, 141, 31))
        self.ac_text.setStyleSheet("color:#8A4600;\n"
"font-size:16pt;\n"
"text-align: center;\n"
"font-family: \"微软雅黑\";")
        self.ac_text.setObjectName("ac_text")
        self.listView_6 = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.listView_6.setGeometry(QtCore.QRect(144, 100, 55, 113))
        self.listView_6.setStyleSheet("background-image:url(:/AC-DC充电器.png)")
        self.listView_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView_6.setObjectName("listView_6")
        self.bms_bg = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.bms_bg.setGeometry(QtCore.QRect(72, 350, 200, 244))
        self.bms_bg.setStyleSheet("background-color: #FEFEFE;\n"
"border: 1px solid #E8E8E8;\n"
"border-top-left-radius:10px;\n"
"border-top-right-radius:10px;\n"
"border-bottom-left-radius:10px;\n"
"border-bottom-right-radius:10px;")
        self.bms_bg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bms_bg.setObjectName("bms_bg")
        self.bms_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.bms_text.setGeometry(QtCore.QRect(147, 530, 51, 21))
        self.bms_text.setStyleSheet("color:#8A4600;\n"
"font-size:16pt;\n"
"text-align: center;\n"
"font-family: \"微软雅黑\";")
        self.bms_text.setObjectName("bms_text")
        self.listView_7 = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.listView_7.setGeometry(QtCore.QRect(135, 390, 70, 113))
        self.listView_7.setStyleSheet("background-image:url(:/BMS.png)")
        self.listView_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView_7.setObjectName("listView_7")
        self.inverter_bg = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.inverter_bg.setGeometry(QtCore.QRect(600, 60, 200, 244))
        self.inverter_bg.setStyleSheet("background-color: #FEFEFE;\n"
"border: 1px solid #E8E8E8;\n"
"border-top-left-radius:10px;\n"
"border-top-right-radius:10px;\n"
"border-bottom-left-radius:10px;\n"
"border-bottom-right-radius:10px;")
        self.inverter_bg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.inverter_bg.setObjectName("inverter_bg")
        self.inverter_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.inverter_text.setGeometry(QtCore.QRect(629, 244, 151, 21))
        self.inverter_text.setStyleSheet("color:#8A4600;\n"
"font-size:16pt;\n"
"text-align: center;\n"
"font-family: \"微软雅黑\";")
        self.inverter_text.setObjectName("inverter_text")
        self.listView_8 = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.listView_8.setGeometry(QtCore.QRect(668, 92, 64, 126))
        self.listView_8.setStyleSheet("background-image:url(:/工频离网逆变器.png)")
        self.listView_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView_8.setObjectName("listView_8")
        self.dc_bg = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.dc_bg.setGeometry(QtCore.QRect(336, 60, 200, 244))
        self.dc_bg.setStyleSheet("background-color:#FEFEFE;\n"
"border: 1px solid #E8E8E8;\n"
"border-top-left-radius:10px;\n"
"border-top-right-radius:10px;\n"
"border-bottom-left-radius:10px;\n"
"border-bottom-right-radius:10px;")
        self.dc_bg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dc_bg.setViewMode(QtWidgets.QListView.ListMode)
        self.dc_bg.setObjectName("dc_bg")
        self.dc_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.dc_text.setGeometry(QtCore.QRect(370, 240, 141, 31))
        self.dc_text.setStyleSheet("color:#8A4600;\n"
"font-size:16pt;\n"
"text-align: center;\n"
"font-family: \"微软雅黑\";")
        self.dc_text.setObjectName("dc_text")
        self.listView_9 = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.listView_9.setGeometry(QtCore.QRect(379, 115, 120, 83))
        self.listView_9.setStyleSheet("background-image:url(:/DC-DC充电器.png)")
        self.listView_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView_9.setObjectName("listView_9")
        self.acchargerBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.acchargerBtn.setGeometry(QtCore.QRect(70, 60, 200, 250))
        self.acchargerBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.acchargerBtn.setStyleSheet("background: transparent;")
        self.acchargerBtn.setText("")
        self.acchargerBtn.setObjectName("acchargerBtn")
        self.bmsBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.bmsBtn.setGeometry(QtCore.QRect(70, 340, 200, 251))
        self.bmsBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.bmsBtn.setStyleSheet("background: transparent;")
        self.bmsBtn.setText("")
        self.bmsBtn.setObjectName("bmsBtn")
        self.InverterBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.InverterBtn.setGeometry(QtCore.QRect(600, 50, 200, 251))
        self.InverterBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.InverterBtn.setStyleSheet("background: transparent;")
        self.InverterBtn.setText("")
        self.InverterBtn.setObjectName("InverterBtn")
        self.dcchargerBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.dcchargerBtn.setGeometry(QtCore.QRect(336, 62, 201, 241))
        self.dcchargerBtn.setStyleSheet("background: transparent;")
        self.dcchargerBtn.setText("")
        self.dcchargerBtn.setObjectName("dcchargerBtn")
        self.inverter_bg.raise_()
        self.inverter_text.raise_()
        self.ac_bg.raise_()
        self.ac_text.raise_()
        self.listView_6.raise_()
        self.bms_bg.raise_()
        self.listView_8.raise_()
        self.dc_bg.raise_()
        self.dc_text.raise_()
        self.listView_9.raise_()
        self.bms_text.raise_()
        self.listView_7.raise_()
        self.bmsBtn.raise_()
        self.acchargerBtn.raise_()
        self.dcchargerBtn.raise_()
        self.InverterBtn.raise_()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setGeometry(QtCore.QRect(-1603, 303, 109, 82))
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.lang_zh = QtWidgets.QAction(MainWindow)
        self.lang_zh.setObjectName("lang_zh")
        self.lang_en = QtWidgets.QAction(MainWindow)
        self.lang_en.setObjectName("lang_en")
        self.menu.addAction(self.lang_zh)
        self.menu.addAction(self.lang_en)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SRNE v0.1.3.3"))
        self.label.setText(_translate("MainWindow", "选择连接的设备"))
        self.ac_text.setText(_translate("MainWindow", "AC-DC 充电器"))
        self.bms_text.setText(_translate("MainWindow", "BMS"))
        self.inverter_text.setText(_translate("MainWindow", "工频离网逆变器"))
        self.dc_text.setText(_translate("MainWindow", "DC-DC 充电器"))
        self.menu.setTitle(_translate("MainWindow", "语言"))
        self.lang_zh.setText(_translate("MainWindow", "中文"))
        self.lang_en.setText(_translate("MainWindow", "English"))
from resources.images import ui
