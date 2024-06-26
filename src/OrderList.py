# qss 颜色
color_open = 'background-color: #57C788'    # 按钮开启的颜色
color_close = 'background-color: #F26659'   # 按钮关闭的颜色

# 下位机指令集

# AC-DC充电器
ac_monitor1 = 'ff03000a005f'        # 获取实时数据1
ac_monitor2 = 'ff0301000023'        # 获取实时数据2
ac_get_chgstatus = 'ff03df000001'   # 获取开关机状态
ac_get_testmode = 'ff03e0020001'    # 获取测试模式状态
ac_get_setting = 'ff03e001003a'     # 获取参数设置

ac_sw_on = 'ff06df000001'           # 开机
ac_sw_off = 'ff06df000000'          # 关机
ac_device_reset = 'ff06df010001'    # 设备复位
ac_fact_reset = 'ff06df020001'      # 恢复出厂
ac_cl_history = 'ff06df030001'      # 清除历史记录
ac_testmode_on = 'ff06e00222b8'     # 进入测试模式


# DC-DC充电器
dc_product_monitor = 'ff03000a005f' # 获取产品信息
dc_control_monitor = 'ff030100002b' # 获取控制器信息
dc_setting = 'ff03e001003d'         # 获取参数设置信息
dc_setting_get_chg = 'ff03df000001' # 获取充电模式开关机状态

dc_sw_on = 'ff06df000001'           # 充电模式开机
dc_sw_off = 'ff06df000000'          # 充电模式关机
dc_cv_on = 'ff06e0370001'           # 电源模式开机
dc_cv_off = 'ff06e0370000'          # 电源模式关机

dc_device_reset = 'ff06df010001'    # 复位
dc_fact_reset = 'ff06df020001'      # 恢复出厂
dc_cl_alarm = 'ff06df030001'        # 清除当前告警
dc_cl_statistic = 'ff06df040001'    # 清除统计量
dc_cl_history = 'ff06df050001'      # 清除历史记录


# 工频离网逆变器
ivpo_sw_on = 'ff06df000001'         # 开机
ivpo_sw_off = 'ff06df000000'        # 关机
ivpo_resetting = 'ff06df010001'     # 设备复位
ivpo_fact_reset = 'ff06df020001'    # 恢复出厂

ivpo_product_msg = 'ff03000a0062'   # 产品信息区
ivpo_control_msg = 'ff0301000004'   # 控制器数据区
ivpo_ivt_msg = 'ff0302040028'       # 逆变数据区
ivpo_setting1 = 'ff03e0010020'      # 用户设置区1
ivpo_setting2 = 'ff03e2040013'      # 用户设置区2

ivpo_history_days = 'ff03f0310001'  # 总运行天数


# BMS指令集
bms_reset = '010630090001'              # 恢复默认值(出厂设置)
bms_clear_history = '0106300b0001'      # 擦除历史数据
bms_sleep_on = '0106300c0001'           # 开启强制休眠
# bms_sleep_off = '0106300c0000'        # 关闭强制休眠
bms_buzzer_on = '010630010001'          # 蜂鸣器开
bms_buzzer_off = '010630010000'         # 蜂鸣器关
bms_recent_history = '0103f0000001'     # 获取最近历史数据的总数


bms_version = '010300140002'        # 查询 BMS 版本号
bms_beep = '010330010001'           # 查询蜂鸣器开关状态
bms_monitor = '010303000060'        # 实时监控
bms_setting = '01032007005b'        # 参数设置 地址：2007-2061
bms_history = '0103f0010036'        # 历史记录
bms_sys_set1 = '010303180002'       # 系统设置页的 剩余容量，总容量
bms_sys_set2 = '010340000001'       # 系统设置页的 设计容量
bms_sys_time = '010303000003'       # 系统设置页的 系统时间
bms_sys_protocol = '0103001b0001'   # 系统设置页的 通讯协议