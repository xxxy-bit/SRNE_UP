import sys
from Ui_Form import Ui_Form
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication, QWidget


class Demo(QWidget, Ui_Form):
    def __init__(self):
        super(Demo, self).__init__()
        self.setupUi(self)
        self.trans = QTranslator(self)                              # 1
        self.comboBox.currentTextChanged.connect(self.change_func)  # 2

    def change_func(self):                                          # 3
        if self.comboBox.currentText() == '中文':
            self.trans.load('zh.qm')
            _app = QApplication.instance()
            _app.installTranslator(self.trans)
            self.retranslateUi(self)
        elif self.comboBox.currentText() == 'français':
            self.trans.load('fr')
            _app = QApplication.instance()
            _app.installTranslator(self.trans)
            self.retranslateUi(self)
        else:
            _app = QApplication.instance()
            _app.removeTranslator(self.trans)
            self.retranslateUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())