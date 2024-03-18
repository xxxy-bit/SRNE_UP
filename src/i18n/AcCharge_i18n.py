import os, gettext
from PyQt5.QtCore import QSettings

set_dir = os.path.join(os.getcwd(), 'settings', 'settings.ini')
setting = QSettings(set_dir, QSettings.IniFormat)

lang_zh = gettext.translation('AcCharge', localedir=os.path.join(os.getcwd(), 'locales'), languages=[setting.value('language')])
lang_zh.install('AcCharge')
_ = lang_zh.gettext

# 串口相关
open_port_i18n = _('打开串口')
close_port_i18n = _('关闭串口')
erro_port_i18n = _('打开串口失败')
# 开/关监控相关
open_monitor_i18n = _('开启数据监控')
close_monitor_i18n = _('关闭数据监控')
# 写入监控日志相关
write_monitor1_i18n = _('产品类型,产品规格,产品序列号,设备名称,设备地址,硬件版本,软件版本,系统电压,额定充电电流,额定放电电流,原始数据(Hex)')
write_monitor2_i18n = _('充电电流,设备温度,蓄电池电压,蓄电池温度,充电状态,故障/告警信息,原始数据(Hex)')
# 错误提示相关
file_occupy_error = _('文件被占用，请关闭Excel文件后重试.')
file_unknow_error = _('未知错误，请截图并联系相关开发人员.')
# 打开目录相关
open_dir_txt1 = _('导出成功，目录位置为')
open_dir_txt2 = _('是否需要打开该目录?')
# 其他的一些提示
stop_monitor_tips = _('为保准数据准确性，请在实时监控中停止数据监控，需要暂停吗?')
write_data_tips = _('请输入参数')
mdf_data_tips = _('请修改参数.')
writing_data_tips = _('写入中...')
write_param_tips = _('写入数据')
sure_param_tips = _('是否要写入以下参数:')
write_data_ok_tips = _('数据已写入，请重新获取数据.')
port_nostart_tips = _('请先打开串口.')
setting_tips = _('请输入正确的数值.')