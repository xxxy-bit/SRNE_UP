import os, gettext
from PyQt5.QtCore import QSettings

set_dir = os.path.join(os.getcwd(), 'settings', 'settings.ini')
setting = QSettings(set_dir, QSettings.IniFormat)

lang_zh = gettext.translation('Bms', localedir=os.path.join(os.getcwd(), 'locales'), languages=[setting.value('language')])
lang_zh.install('Bms')
_ = lang_zh.gettext

# 选项卡
tab_tabel1 = _('实时监控')
tab_tabel2 = _('并机监控')
tab_tabel3 = _('参数设置')
tab_tabel4 = _('系统设置')
tab_tabel5 = _('历史数据')
tab_tabel6 = _('实时数据')

# 实时监控页
# 组名称
group_tabel1 = _('电池信息')
group_tabel2 = _('温度信息')
group_tabel3 = _('单体电压')
group_tabel4 = _('管理员登录')
group_tabel55 = _('串口信息')
group_tabel5 = _('串口')
group_tabel6 = _('开关控制')
group_tabel7 = _('系统状态')
group_tabel8 = _('故障状态')
group_tabel9 = _('告警状态')
group_tabel10 = _('保护状态')
group_tabel11 = _('其他状态')

# 电池信息
battery_label1 = _('Pack电池电压')
battery_label2 = _('Pack电池电流')
battery_label3 = _('剩余容量')
battery_label4 = _('充满容量')
battery_label5 = _('循环次数')

# 温度信息
temp_label19 = _('环境温度')
temp_label20 = _('Pack正极端子温度')
temp_label21 = _('Pack负极端子温度')
temp_label22 = _('Pack端子温度3')
temp_label23 = _('Pack端子温度4')
temp_label24 = _('Mos管1温度')
temp_label25 = _('Mos管2温度')

# 单体电压
vol_label17 = _('cell最大压差')
vol_label18 = _('cell最大电压')
vol_label19 = _('cell最小电压')

# 管理员登录
pwd_label1 = _('密码')
pwd_label2 = _('确定')

# 串口
com_label2 = _('波特率')
com_label3 = _('Pack数量')
com_label4 = _('地址')
com_label5 = _('间隔（秒）')
com_label6 = _('打开串口')
com_label8 = _('开始监控')
com_label9 = _('刷新串口')

# 开关控制
switch_label1 = _('充电')
switch_label2 = _('放电')
switch_label3 = _('强制休眠')
switch_label4 = _('打开')
switch_label5 = _('蜂鸣器')
switch_label6 = _('进入测试模式')
switch_label7 = _('退出测试模式')

# 系统状态
sys_label1 = _('充电状态')
sys_label2 = _('放电状态')
sys_label3 = _('充电MOS管开启')
sys_label4 = _('放电MOS管开启')
sys_label5 = _('充电器接入')
sys_label6 = _('满充')
sys_label7 = _('加热')
sys_label8 = _('二次保护触发')

# 并机监控页
# 组名称
pal_label1 = _('并联连接')
pal_label2 = _('报警状态')
pal_label3 = _('并联数据')
pal_label4 = _('电芯数据')

# 并联设置
palset_label1 = _('Pack 数量')
palset_label2 = _('获取数据')
palset_label3 = _('取消')

# 报警状态
error_label1 = _('充电状态')
error_label2 = _('放电状态')
error_label3 = _('总高压报警')
error_label4 = _('总低压报警')

# 并联数据
paldata_label1 = _('平均电压')
paldata_label2 = _('平均SOC')
paldata_label3 = _('总电流')    # 总电压
paldata_label4 = _('总电压')    # 总电压

# 电芯数据
celldata_label1 = _('最高电芯电压')
celldata_label2 = _('最高电芯电压位置')
celldata_label3 = _('最低电芯电压')
celldata_label4 = _('最低电芯电压位置')
celldata_label5 = _('最高电芯温度')
celldata_label6 = _('最高电芯温度位置')
celldata_label7 = _('最低电芯温度')
celldata_label8 = _('最低电芯温度位置')

# 并机数据
palnum_label1 = _('电压')
palnum_label2 = _('温度')
palnum_label3 = _('PACK 电流')
palnum_label7 = _('充放电循环次数')
palnum_label8 = _('PACK设计容量')
palnum_label9 = _('告警')
palnum_label10 = _('PACK充电电流告警')
palnum_label11 = _('PACK总电压告警')
palnum_label12 = _('PACK放电电流告警')
palnum_label14 = _('指示状态')
palnum_label15 = _('控制状态')
palnum_label16 = _('均衡状态')

# 参数设置页
# 组名称
parset_label1 = _('单体过充设置')
parset_label2 = _('单体过放设置')
parset_label3 = _('总体过充设置')
parset_label4 = _('总体过放设置')
parset_label5 = _('高温设置')
parset_label6 = _('低温设置')
parset_label7 = _('放电过流设置')
parset_label8 = _('充电过流设置')

# 单体过充设置
parset1_label1 = _('单体过充告警')
parset1_label2 = _('单体过充保护')
parset1_label3 = _('单体过充保护恢复')
parset1_label4 = _('单体过充保护延时')
parset1_label5 = _('单体过充告警延时')
parset1_label6 = _('单体过充告警恢复值')

# 单体过放设置
parset2_label1 = _('单体过放告警')
parset2_label2 = _('单体过放保护')
parset2_label3 = _('单体过放保护恢复')
parset2_label4 = _('单体过放保护延时')
parset2_label5 = _('单体过放告警延时')
parset2_label6 = _('单体过放告警恢复值')

# 总体过充设置
parset3_label1 = _('总体过充告警')
parset3_label2 = _('总体过充保护')
parset3_label3 = _('总体过充保护恢复')
parset3_label4 = _('总体过充保护延时')
parset3_label5 = _('总体过充告警延时')
parset3_label6 = _('总体过充告警恢复值')

# 总体过放设置
parset4_label1 = _('总体过放告警')
parset4_label2 = _('总体过放保护')
parset4_label3 = _('总体过放保护恢复')
parset4_label4 = _('总体过放保护延时')
parset4_label5 = _('总体过放告警延时')
parset4_label6 = _('总体过放告警恢复值')

# 高温设置
parset5_label1 = _('充电高温告警')
parset5_label2 = _('充电高温保护')
parset5_label3 = _('充电高温保护恢复')
parset5_label4 = _('放电高温告警')
parset5_label5 = _('放电高温保护')
parset5_label6 = _('放电高温保护恢复')
parset5_label7 = _('均衡开启电压')
parset5_label8 = _('均衡开启压差')
parset5_label9 = _('单体休眠电压')
parset5_label10 = _('单体低压休眠延时')

# 低温设置
parset6_label1 = _('充电低温告警')
parset6_label2 = _('充电低温保护')
parset6_label3 = _('充电低温保护恢复')
parset6_label4 = _('放电低温告警')
parset6_label5 = _('放电低温保护')
parset6_label6 = _('放电低温保护恢复')
parset6_label7 = _('电池充满电压')
parset6_label8 = _('电池满充电流')
parset6_label9 = _('低电量告警')

# 放电过流设置
parset7_label1 = _('放电过流告警')
parset7_label2 = _('放电过流保护1')
parset7_label3 = _('放电过流保护延时1')
parset7_label4 = _('放电过流保护2')
parset7_label5 = _('放电过流保护延时2')
parset7_label6 = _('短路保护延时')
parset7_label7 = _('放电过流告警延时')
parset7_label8 = _('放电过流告警恢复值')

# 充电过流设置
parset8_label1 = _('充电过流告警')
parset8_label2 = _('充电过流保护1')
parset8_label3 = _('充电过流保护延时1')
parset8_label4 = _('充电过流保护2')
parset8_label5 = _('充电过流保护延时2')
parset8_label6 = _('充电过流告警延时')
parset8_label7 = _('充电过流告警恢复值')

# 按钮
parset9_label1 = _('读取参数')
parset9_label2 = _('清屏')
parset9_label3 = _('写入参数')
parset9_label4 = _('恢复默认值')
parset9_label5 = _('导出参数')

# 系统设置页
sysset_label1 = _('电量')
sysset_label2 = _('设计容量')
sysset_label4 = _('总容量')
sysset_label5 = _('读取')
sysset_label6 = _('设置')

# 数据校准
datacal_label1 = _('数据校准')
datacal_label2 = _('校准')
datacal_label3 = _('校准完毕')

# 系统时间
systime_label1 = _('系统时间')
systime_label2 = _('同步时间')
systime_label3 = _('写入')

# 历史数据页
hisdata_label1 = _('获取最近历史数据(1~100)')
hisdata_label2 = _('擦除历史数据')
hisdata_label3 = _('导出历史记录')
hisdata_label4 = _('继续')
hisdata_label5 = _('暂停')

# 实时数据页
realdata_label1 = _('清空内容')

# 底边栏
ver_label1 = _('版本')

# 逻辑部分文本
bms_logic_label2 = _('关闭串口')
bms_logic_label4 = _('停止监控')
bms_logic_label6 = _('关闭')
bms_logic_label7 = _('串口未打开')
bms_logic_label8 = _('正在获取100条历史数据，请稍等...')
bms_logic_label9 = _('为保证数据准确性，需要先停止实时监控中的数据监控，是否停止？')
bms_logic_label11 = _('请输入正确的数据')

bms_logic_label12 = _('超出数据接收范围')
bms_logic_label13 = _('请先修改数据')
bms_logic_label15 = _('通信正常')
bms_logic_label16 = _('通信中断')
bms_logic_label18 = _('登录成功')
bms_logic_label19 = _('密码错误')
bms_logic_label20 = _('串口打开失败')
bms_logic_label21 = _('数据不能大于4')
bms_logic_label22 = _('数据不能大于60')
bms_logic_label24 = _('是否确定写入以下参数')
bms_logic_label26 = _('保存成功，文件位置在')
bms_logic_label27 = _('历史数据为0')
bms_logic_label28 = _('cell低压或pack低压超过30分钟，已停止监控')
bms_logic_label29 = _('返回的校验码不正确')
bms_logic_label30 = _('正在获取历史数据，请暂停或等待完成.')
bms_logic_label31 = _('文件被占用，请关闭Excel文件后重试.')
bms_logic_label32 = _('未知错误，请联系相关开发人员.')
bms_logic_label33 = _('导出成功，文件位置为：')
bms_logic_label34 = _('是否需要打开该文件?')
bms_logic_label35 = _('写入完毕，请重新读取数据.')
bms_logic_label36 = _('请输入整数')
bms_logic_label37 = _('串口异常')

# 解析数据
bms_parse_label1 = _('超压')
bms_parse_label2 = _('低压')
bms_parse_label3 = _('充电反接')
bms_parse_label4 = _('放电短路')
bms_parse_label5 = _('充电短路')
bms_parse_label6 = _('充电超压保护')
bms_parse_label7 = _('MOS高温保护')
bms_parse_label8 = _('环境高温保护')
bms_parse_label9 = _('环境低温保护')
bms_parse_label10 = _('端子高温保护')
bms_parse_label11 = _('充电过流1')
bms_parse_label12 = _('放电过流1')
bms_parse_label13 = _('充电过流2')
bms_parse_label14 = _('放电过流2')
bms_parse_label15 = _('充电MOS管故障')
bms_parse_label16 = _('放电MOS管故障')
bms_parse_label17 = _('温度传感器故障')
bms_parse_label18 = _('cell失效')
bms_parse_label19 = _('采样故障')
bms_parse_label20 = _('电量计故障')
bms_parse_label21 = _('逆变器通讯故障')
bms_parse_label22 = _('E2ROM通讯故障')
bms_parse_label23 = _('cell超压')
bms_parse_label24 = _('cell低压')
bms_parse_label25 = _('pack超压')
bms_parse_label26 = _('pack低压')
bms_parse_label27 = _('SOC过低')
bms_parse_label28 = _('充电高温')
bms_parse_label29 = _('放电高温')
bms_parse_label30 = _('充电低温')
bms_parse_label31 = _('放电低温')
bms_parse_label32 = _('环境高温')
bms_parse_label33 = _('环境低温')
bms_parse_label34 = _('MOS高温')
bms_parse_label35 = _('端子高温')
bms_parse_label36 = _('充电过流')
bms_parse_label37 = _('放电过流')

# 历史数据
bms_history_label1 = _('时间')
bms_history_label2 = _('总压')
bms_history_label3 = _('电流')
bms_history_label4 = _('状态位')
bms_history_label5 = _('保护位')
bms_history_label6 = _('警告位')
bms_history_label7 = _('故障位')
bms_history_label8 = _('压差')
bms_history_label9 = _('最高cell电压')
bms_history_label10 = _('最低cell电压')
bms_history_label11 = _('最高压对应cell')
bms_history_label12 = _('最低压对应cell')
bms_history_label13 = _('最高温度对应cell')
bms_history_label14 = _('最低温度对应cell')
bms_history_label15 = _('PACK+/-温度(最高)')

bms_history_label18 = _('预充')
bms_history_label19 = _('限流充电')
bms_history_label20 = _('充电器反接')
bms_history_label21 = _('预充MOS管开启')
bms_history_label22 = _('激活MOS管开启')
bms_history_label23 = _('限流充电MOS管开启')
bms_history_label24 = _('风扇开启')
bms_history_label25 = _('加热开启')
bms_history_label26 = _('干接点1(故障信号)开启')
bms_history_label27 = _('干接点2(电池过放)开启')
bms_history_label28 = _('干接点3(灭火装置)开启')
bms_history_label29 = _('干接点4(二次保护触发)开启')

bms_history_label30 = _('BMS 开机动作')
bms_history_label31 = _('BMS 关机动作')
bms_history_label32 = _('时间校准动作')

# 并联数据逻辑
bms_pal_logic_label1 = _('正常')
bms_pal_logic_label2 = _('欠压')
bms_pal_logic_label3 = _('电流过高')
bms_pal_logic_label4 = _('温度过低')
bms_pal_logic_label5 = _('温度过高')

# rs485配置文件
bms_rs485_label1 = _('单体过压保护')
bms_rs485_label2 = _('总压过压保护')
bms_rs485_label3 = _('总压过放保护')
bms_rs485_label4 = _('充电过流保护')
bms_rs485_label5 = _('放电过流保护')
bms_rs485_label6 = _('短路')
bms_rs485_label7 = _('Fully充满')
bms_rs485_label8 = _('限流')
bms_rs485_label9 = _('Pack供电')
bms_rs485_label10 = _('加热膜')
bms_rs485_label11 = _('蜂鸣器告警')
bms_rs485_label12 = _('充电限流')
bms_rs485_label13 = _('充电MOS故障')
bms_rs485_label14 = _('放电MOS故障')
bms_rs485_label15 = _('电芯故障')
bms_rs485_label16 = _('单体过压')
bms_rs485_label17 = _('单体低压')
bms_rs485_label18 = _('总压过压')
bms_rs485_label19 = _('总压低压')
bms_rs485_label20 = _('低电量')