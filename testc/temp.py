import binascii


# a = '6df15733785565e565b080fd6e9079d1628067099650516c53f8'
# b = 'c4e3bac3'
# bs = binascii.a2b_hex(b)
# print(bs)
# print(bs.decode('gb2312'))

import os

# 打开目录
# directory = 'E:/xy/xy/APP文档'
# os.startfile(directory)

# 获取系统语言
# import locale
# loc = locale.getlocale()
# print(loc)
# print(locale.getdefaultlocale())

import gettext
from PyQt5.QtCore import QSettings

set_dir = os.getcwd() + "\\settings\\settings.ini"
setting = QSettings(set_dir, QSettings.IniFormat)

lang_zh = gettext.translation('temp', localedir=f'{os.getcwd()}\\testc\\loc', languages=['zh_CN'])
lang_zh.install('temp')
_ = lang_zh.gettext

a = {
    '1': _('one'),
    '2': _('two'),
    '3': _('three'),
    '4': _('four'),
    '5': _('fire'),
    '6': _('six'),
    '7': _('seven'),
    '8': _('eight'),
    '9': _('nice'),
    '10': _('ten'),
}

print(a)
print(*[str(i) for i in range(1, 11)])
print(*[1,2,3])

