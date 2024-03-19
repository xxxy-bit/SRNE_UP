import os, gettext
from PyQt5.QtCore import QSettings

set_dir = os.path.join(os.getcwd(), 'settings', 'settings.ini')
setting = QSettings(set_dir, QSettings.IniFormat)

lang_zh = gettext.translation('DcCharge', localedir=os.path.join(os.getcwd(), 'locales'), languages=[setting.value('language')])
lang_zh.install('DcCharge')
_ = lang_zh.gettext


# BatTypeSet
BatTypeSet_1 = _('自定义')
BatTypeSet_2 = _('开口(FLD)')
BatTypeSet_3 = _('密封(SLD)')
BatTypeSet_4 = _('胶体(GEL)')
BatTypeSet_5 = _('锂电池(LI)')

# ChgMode
ChgMode_1 = _('充电模式')
ChgMode_2 = _('电源模式')

# GeneratorType
GeneratorType_1 = _('传统发电机')
GeneratorType_2 = _('智能发电机')
GeneratorType_3 = _('自定义发电机')

# Button
Button_1 = _('打开串口')
Button_2 = _('关闭串口')
Button_3 = _('开启监控')
Button_4 = _('关闭监控')

# tips
tips_1 = _('读取完成')
tips_2 = _('请先修改参数')
tips_3 = _('串口打开失败')

# csv
csv_1 = _('系统电压,额定充电电流,产品类型,产品规格,软件版本,硬件版本,产品序列号,设备地址,CAN程序版本,设备名字,原始数据(Hex)')
csv_2 = _('蓄电池电压,充电电流,设备温度,蓄电池温度,输入电压,充电功率,输出端开机以来最低电压,输出端开机以来最高电压,开机以来充电最大电流,当天充电安时数,当天发电量,总运行天数,蓄电池总充满次数,蓄电池总充电安时数,累计发电量,充电状态,控制器/告警信息1,原始数据(Hex)')
