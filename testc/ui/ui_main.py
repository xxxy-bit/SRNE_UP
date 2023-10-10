from PyQt5 import QtCore, QtGui, QtWidgets

class Menu_Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Menu_Ui, self).__init__()
        self.setupUi(self)

    def setupUi(self, Menu):
        Menu.setObjectName("Menu")
        Menu.resize(500, 300)
        self.centralwidget = QtWidgets.QWidget(Menu)
        self.centralwidget.setObjectName("centralwidget")
        
        
        self.v_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.acc_btn = QtWidgets.QPushButton(self.centralwidget)
        
        
        self.v_layout.addWidget(self.acc_btn)
        
        Menu.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(Menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 462, 22))
        self.menubar.setObjectName("menubar")
        Menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Menu)
        self.statusbar.setObjectName("statusbar")
        Menu.setStatusBar(self.statusbar)