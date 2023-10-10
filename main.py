import sys, os
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow
from PyQt5 import QtCore

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)

with open(os.path.join(os.getcwd(), 'ui', 'qss', 'qs.qss'), "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())
MainWindow = MainWindow()
MainWindow.show()

sys.exit(app.exec_())