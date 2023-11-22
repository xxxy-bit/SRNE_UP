# BMS指令集

bms_version = '010300140002'              # BMS 版本号
bms_reset = '0106400b0001'              # 恢复默认值(出厂设置)
bms_clear_history = '0106300b0001'      # 擦除历史数据
bms_recent_history = '0103f0000001'     # 获取最近历史数据的总数
bms_sleep_on = '0106300c0001'           # 开启强制休眠
bms_sleep_off = '0106300c0000'          # 关闭强制休眠

bms_monitor = '01030300005e'    # 实时监控
bms_setting = '01032007005b'    # 参数设置 地址：2007-2061
bms_history = '0103f0010036'    # 历史记录
bms_sys_set1 = '010303180003'   # 系统设置页的 剩余容量，总容量
bms_sys_set2 = '010340000001'   # 系统设置页的 设计容量
bms_sys_time = '010320040003'   # 系统设置页的 系统时间