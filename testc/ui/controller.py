from .window import HelloWindow
from .window import OperateWindow
from .window import LoginWindow


# 利用一个控制器来控制页面的跳转
class Controller:
    def __init__(self):
        pass
    # 跳转到 hello 窗口
    def show_hello(self):
        self.hello = HelloWindow()
        self.hello.switch_window1.connect(self.show_login)
        self.hello.switch_window2.connect(self.show_operate)
        self.hello.show()
    # 跳转到 login 窗口, 注意关闭原页面
    def show_login(self):
        self.login = LoginWindow()
        self.hello.close()
        self.login.show()
    # 跳转到 operate 窗口, 注意关闭原页面
    def show_operate(self):
        self.operate = OperateWindow()
        self.hello.close()
        self.operate.show()
