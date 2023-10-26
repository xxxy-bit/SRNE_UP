# qss 颜色
color_open = 'background-color: #57C788'    # 按钮开启的颜色
color_close = 'background-color: #F26659'   # 按钮关闭的颜色

# 指令集
# Ac充电器
ac_monitor1 = 'ff03000a005f' # 获取实时数据1
ac_monitor2 = 'ff0301000023' # 获取实时数据2
ac_get_chgstatus = 'ff03df000001'   # 获取开关机状态
ac_get_testmode = 'ff03e0020001' # 获取测试模式状态
ac_get_setting = 'ff03e001003a'   # 获取参数设置

ac_sw_on = 'ff06df000001'    # 开机
ac_sw_off = 'ff06df000000'    # 关机
ac_device_reset = 'ff06df010001'    # 设备复位
ac_fact_reset = 'ff06df020001'  # 恢复出厂
ac_cl_history = 'ff06df030001'  # 清除历史记录
ac_testmode_on = 'ff06e00222b8'    # 进入测试模式


# 工频离网逆变器
ivpo_sw_on = 'ff06df000001' # 开机
ivpo_sw_off = 'ff06df000000'    # 关机
ivpo_resetting = 'ff06df010001' # 设备复位
ivpo_fact_reset = 'ff06df020001'    # 恢复出厂

ivpo_product_msg = 'ff03000a005f'   # 产品信息区
ivpo_control_msg = 'ff0301000004'   # 控制器数据区
ivpo_ivt_msg = 'ff0302040028'   # 逆变数据区
ivpo_setting1 = 'ff03e0010020'  # 用户设置区1
ivpo_setting2 = 'ff03e2040013'  # 用户设置区2

ivpo_history_days = 'ff03f0310001'  # 总运行天数