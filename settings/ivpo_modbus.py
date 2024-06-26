from src.OrderList import *

ivpo_data_list = {
    # 产品信息区
    ivpo_product_msg:{
        # 地址下标，长度，倍率，单位
        '系统最高支持电压':[0, 1, 1, ''],
        '产品类型':[1, 1, 1, '', {
            '05':'工频离网逆变器',
            '20':'离网逆变器',
            '21':'工频并网逆变器',
            }],
        '产品型号':[2, 8, 1, ''],
        '软件版本':[10, 2, 1, ''],
        '硬件版本':[12, 2, 1, ''],
        '产品序列号':[14, 2, 1, ''],
        '设备地址':[16, 1, 1, ''],
        # '机型编码':[17, 1, 1, ''],
        # 'RS485版本':[18, 2, 1, ''],
        # '生产日期':[20, 2, 1, ''],
        # '产地编码':[22, 1, 1, ''],
        # '软件编译时间':[23, 20, 1, ''],
        # '产品序列号字符串':[43, 20, 1, ''],
        '设备名称':[63, 32, 1, ''],
        # '保留':[95, 3, 1, ''],
    },
    # 控制器数据区
    ivpo_control_msg:{
        # '蓄电池SOC':[0, 1, 1, ''],
        '蓄电池电压':[1, 1, 10, 'V'],
        '充电电流':[2, 1, 10, 'A'],
        '充电状态':[3, 1, 1, '', {
            '00':'空闲',
            '01':'测试充电',
            '02':'大电流充电',
            '03':'均衡充电',
            '04':'提升充电',
            '05':'浮充充电',
            '06':'限流充电',
            '07':'充满',
            '08':'储存充电',
            '09':'电源模式输出',
            '0a':'逆变输出',
            }],
    },
    # 逆变数据区
    ivpo_ivt_msg:{
        '当前故障码':[0, 4, 1, '', {
            '0':'蓄电池过放',
            '1':'蓄电池超压',
            '2':'母线低压',
            '3':'母线过压',
            '4':'母线过流',
            '5':'逆变欠压',
            '6':'逆变过压',
            '7':'逆变过流',
            '8':'负载过流',
            '9':'负载短路',
            '10':'电网输入过流',
            '11':'电网输入过压',
            '16':'A过温',
            '17':'B过温',
            '18':'C过温',
            '19':'D过温',
            '20':'机型故障',
            '21':'风扇故障',
            '22':'输出低压',
            '23':'输出高压',
            '24':'电池超温',
            '28':'蓄电池反接',
            }],
        # '保留':[4, 4, 1, ''],
        '当前时间':[8, 4, 1, ''],
        # '机器当前状态':[12, 1, 1, ''],
        # '密码保护状态标志':[13, 1, 1, ''],
        # '母线电压':[14, 1, 1, ''],
        # '保留':[15, 1, 1, ''],
        # '母线电流':[16, 1, 1, ''],
        '交流输出有功功率':[17, 1, 1000, 'kW'],
        '交流输出电压1':[18, 1, 10, 'V'],
        '交流输出电流':[19, 1, 10, 'A'],
        '交流输出频率':[20, 1, 100, 'Hz'],
        # '负载电流':[21, 1, 1, ''],
        # '负载PF':[22, 1, 1, ''],
        # '负载有功':[23, 1, 1, ''],
        # '负载视在功率':[24, 1, 1, ''],
        # '负载无功':[25, 1, 1, ''],
        # '保留':[26, 1, 1, ''],
        # '负载功率百分比':[27, 1, 1, ''],
        '温度A':[28, 1, 10, '℃'],
        '温度B':[29, 1, 10, '℃'],
        '温度C':[30, 1, 10, '℃'],
        '温度D':[31, 1, 10, '℃'],
        '外部温度':[32, 1, 10, '℃'],
        # '接地电阻':[33, 1, 1, ''],
        '交流输入频率':[34, 1, 100, 'Hz'],
        '交流输入有功功率':[35, 1, 1000, 'kW'],
        # '交流输入无功功率':[36, 1, 1, ''],
        '交流输入电压A':[37, 1, 10, 'V'],
        '交流输入电流A':[38, 1, 100, 'A'],
        '交流输出电压2':[39, 1, 10, 'V'],
    },
    # 总运行天数
    ivpo_history_days:{
        '总运行天数':[0, 1, 1, 'd']
    },
    # 用户设置区1
    ivpo_setting1:{
        # 地址下标，长度，倍率，发送地址
        '充电电流设置(A)':[0, 1, 100, 'e001'],
        # '蓄电池标称容量':[1, 1, 1, ''],
        # '系统电压设置':[2, 1, 1, ''],
        '蓄电池类型':[3, 1, 1, 'e004'],
        '超压电压(V)':[4, 1, 10, 'e005'],
        '充电限制电压(V)':[5, 1, 10, 'e006'],
        '均衡充电电压(V)':[6, 1, 10, 'e007'],
        '提升充电电压(V)':[7, 1, 10, 'e008'],
        '浮充充电电压(V)':[8, 1, 10, 'e009'],
        '提升充电返回电压(V)':[9, 1, 10, 'e00a'],
        '过放返回电压(V)':[10, 1, 10, 'e00b'],
        # '欠压警告电压':[11, 1, 1, ''],
        '过放电压(V)':[12, 1, 10, 'e00d'],
        # '放电限制电压':[13, 1, 1, ''],
        # '充电截止SOC,放电截止SOC':[14, 1, 1, ''],
        # '过放延时时间':[15, 1, 1, ''],
        # '均衡充电时间':[16, 1, 1, ''],
        '提升充电时间(Min)':[17, 1, 1, 'e012'],
        '均衡充电间隔(day)':[18, 1, 1, 'e013'],
        '温度补偿系数(mV/℃/2V)':[19, 1, 1, 'e014'],
        # '电池充电上限温度':[20, 1, 1, ''],
        '电池充电下限温度(℃)':[21, 1, 1, 'e016'],
        # '电池放电上限温度':[22, 1, 1, ''],
        # '电池放电下限温度':[23, 1, 1, ''],
        # '(锂电)加热启动电池温度':[24, 1, 1, ''],
        # '(锂电)加热停止电池温度':[25, 1, 1, ''],
        # '超压恢复电压':[26, 1, 1, ''],
        '充满截止电流(A)':[27, 1, 1, 'e01c'],
        # '充满时间设置':[28, 1, 1, ''],
        '铅酸激活':[29, 1, 1, 'e01d'],
        '锂电池低温充电(℃)':[30, 1, 1, 'e01f'],
        '接地继电器':[31, 1, 1, 'e020'],
    },
    # 用户设置区2
    ivpo_setting2:{
        '输出优先级':[0, 2, 1, 'e204'],
        '风扇启动温度(℃)':[2, 1, 10, 'e206'],
        'ECO启动功率(W)':[3, 1, 1, 'e207'],
        '交流输出电压(V)':[4, 1, 10, 'e208'],
        '交流输出频率(Hz)':[5, 1, 100, 'e209'],
        'ECO启动时间(S)':[6, 2, 1, 'e20a'],
        '逆变状态模式':[8, 1, 1, 'e20c'],
        # '过载自动重启':[9, 1, 1, ''],
        # '过温自动重启':[10, 1, 1, ''],
        # '保留':[11, 4, 1, ''],
        # '记录故障码':[15, 1, 1, ''],
        '蜂鸣器设置':[16, 1, 1, 'e214'],
        '输出切换电压(V)':[17, 1, 10, 'e215'],
        'AC输入电流设置(A)':[18, 1, 1, 'e216'],
    }
}