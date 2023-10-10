import sys
import os
from lang import Ui_MainWindow
from PyQt5 import QtCore
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from qt_material import apply_stylesheet


class Demo(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        self.setupUi(self)
        self.t = QTranslator(self)
        self.comboBox.currentTextChanged.connect(self.change_func)  # 2

    def change_func(self):
        dir = os.path.dirname(os.path.abspath(__file__))

        if self.comboBox.currentText() == "English":
            print(self.t.load(dir + "\\lang_en.qm"))
        else:
            print(self.t.load(dir + "\\lang_zh.qm"))

        app.installTranslator(self.t)
        self.retranslateUi(self)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    demo = Demo()

    apply_stylesheet(app, theme="default.xml")

    demo.show()
    sys.exit(app.exec_())