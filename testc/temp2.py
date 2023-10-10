import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtGui import QFont

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 初始化应用程序界面
        QToolTip.setFont(QFont('SansSerif', 10))  # 设置全局的字体样式和大小

        button = QPushButton('Hover me', self)
        button.setToolTip('This is a tooltip')  # 设置提示文本

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltip Example')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
