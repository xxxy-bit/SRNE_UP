from src.i18n.Bms_i18n import *
from src.OrderList import *

def get_bms_modbus_list():
    bms_data_list = {
        # bms 实时监控
        bms_monitor:{
            "当前时间(年月)":[0, 1, 1, ""],
            "当前时间(日时)":[1, 1, 1, ""],
            "当前时间(分秒)":[2, 1, 1, ""],
            "BMS总运行时间":[3, 1, 1, "day"],
            battery_label2:[4, 1, -100, "A"],
            battery_label1:[5, 1, 100, "V"],
            "SOC":[6, 1, 1, ""],
            "SOH":[7, 1, 1, ""],
            "BMS工作状态1":[8, 1, 1, "", {
                # "0":"告警状态",
                # "1":"保护状态",
                # "2":"预充",
                "3":sys_label1,
                "4":sys_label2,
                # "5":"限流充电",
                "6":sys_label6,
                "7":sys_label5,
                # "8":"充电器反接",
                "9":sys_label3,
                "10":sys_label4,
                # "11":"预充MOS管开启",
                # "12":"激活MOS管开启",
                # "13":"限流充电MOS管开启"
            }],
            "BMS工作状态2":[9, 1, 1, "", {
                "0":"风扇开启",
                "1":"加热开启",
                "2":"干接点1(故障信号)开启",
                "3":"干接点2(电池过放)开启",
                "4":"干接点3(灭火装置)开启",
                "5":"干接点4(二次保护触发)开启"
            }],
            "故障位":[10, 1, 1, "", {
                "0":bms_parse_label15,
                "1":bms_parse_label16,
                "2":bms_parse_label17,
                "3":bms_parse_label18,
                "4":bms_parse_label19,
                "5":bms_parse_label20,
                "6":bms_parse_label21,
                "7":bms_parse_label22
            }],
            "警告位1":[11, 1, 1, "", {
                "0":"301:" + bms_parse_label23,
                "1":"302:" + bms_parse_label24,
                "2":"303:" + bms_parse_label25,
                "3":"304:" + bms_parse_label26,
                "7":"316:" + bms_parse_label27,
                "8":"309:" + bms_parse_label28,
                "9":"310:" + bms_parse_label29,
                "10":"311:" + bms_parse_label30,
                "11":"312:" + bms_parse_label31,
                "12":"313:" + bms_parse_label32,
                "13":"314:" + bms_parse_label33,
                "14":"315:" + bms_parse_label34,
                "15":bms_parse_label35
            }],
            "警告位2":[12, 1, 1, "", {
                "0":"305:" + bms_parse_label36,
                "1":"306:" + bms_parse_label37
            }],
            "保护位1":[13, 1, 1, "", {
                "0":"201:cell" + bms_parse_label1,
                "1":"202:cell" + bms_parse_label2,
                "2":"203:pack" + bms_parse_label1,
                "3":"204:pack" + bms_parse_label2,
                "4":bms_parse_label3,
                "5":"207:" + bms_parse_label4,
                "6":"207:" + bms_parse_label5,
                "7":"208:" + bms_parse_label6,
                "8":"209:" + parset5_label2,
                "9":"210:" + parset5_label5,
                "10":"211:" + parset6_label2,
                "11":"212:" + parset6_label5,
                "12":"213:" + bms_parse_label7,
                "13":"214:" + bms_parse_label8,
                "14":"215:" + bms_parse_label9,
                "15":bms_parse_label10
            }],
            "保护位2":[14, 1, 1, "", {
                "0":"205:" + bms_parse_label11,
                "1":"206:" + bms_parse_label12,
                "2":"205:" + bms_parse_label13,
                "3":"206:" + bms_parse_label14
            }],
            "短路保护次数":[15, 1, 1, ""],
            "温度保护次数":[16, 1, 1, ""],
            "过流保护次数":[17, 1, 1, ""],
            "过压保护次数":[18, 1, 1, ""],
            "均衡位":[19, 1, 1, ""],
            "cell过压告警":[20, 1, 1, ""],
            "cell过压保护":[21, 1, 1, ""],
            "cell欠压告警":[22, 1, 1, ""],
            "cell欠压保护":[23, 1, 1, ""],
            battery_label3:[24, 1, 100, "AH"],
            battery_label4:[25, 1, 100, "AH"],
            battery_label5:[26, 1, 1, ""],
            "Pack地址":[27, 1, 1, ""],
            "剩余可用时间(放电)":[28, 1, 1, "min"],
            "剩余可用时间(充电)":[29, 1, 1, "min"],
            "cell_1(V)":[30, 1, 1000, ''],
            "cell_2(V)":[31, 1, 1000, ''],
            "cell_3(V)":[32, 1, 1000, ''],
            "cell_4(V)":[33, 1, 1000, ''],
            "cell_5(V)":[34, 1, 1000, ''],
            "cell_6(V)":[35, 1, 1000, ''],
            "cell_7(V)":[36, 1, 1000, ''],
            "cell_8(V)":[37, 1, 1000, ''],
            "cell_9(V)":[38, 1, 1000, ''],
            "cell_10(V)":[39, 1, 1000, ''],
            "cell_11(V)":[40, 1, 1000, ''],
            "cell_12(V)":[41, 1, 1000, ''],
            "cell_13(V)":[42, 1, 1000, ''],
            "cell_14(V)":[43, 1, 1000, ''],
            "cell_15(V)":[44, 1, 1000, ''],
            "cell_16(V)":[45, 1, 1000, ''],
            "cell平均电压":[46, 1, 1000, "V"],
            vol_label17 + "(V)":[47, 1, 1000, ""],
            vol_label18 + "(V)":[48, 1, 1000, ""],
            vol_label19 + "(V)":[49, 1, 1000, ""],
            "最低电压对应的cell":[50, 1, 1, ""],
            "最高电压对应的cell":[51, 1, 1, ""],
            "失效的cell":[52, 1, 1, ""],
            "cell_1(℃)":[53, 1, -10, ""],
            "cell_2(℃)":[54, 1, -10, ""],
            "cell_3(℃)":[55, 1, -10, ""],
            "cell_4(℃)":[56, 1, -10, ""],
            "cell_5(℃)":[57, 1, -10, ""],
            "cell_6(℃)":[58, 1, -10, ""],
            "cell_7(℃)":[59, 1, -10, ""],
            "cell_8(℃)":[60, 1, -10, ""],
            "cell_9(℃)":[61, 1, -10, ""],
            "cell_10(℃)":[62, 1, -10, ""],
            "cell_11(℃)":[63, 1, -10, ""],
            "cell_12(℃)":[64, 1, -10, ""],
            "cell_13(℃)":[65, 1, -10, ""],
            "cell_14(℃)":[66, 1, -10, ""],
            "cell_15(℃)":[67, 1, -10, ""],
            "cell_16(℃)":[68, 1, -10, ""],
            "cell平均温度":[69, 1, -10, ""],
            "cell最高温":[70, 1, -10, ""],
            "cell最低温":[71, 1, -10, ""],
            "最高温cell":[72, 1, 1, ""],
            "最低温cell":[73, 1, 1, ""],
            temp_label19 + "(℃)":[74, 1, -10, ""],
            temp_label20 + "(℃)":[75, 1, -10, ""],
            temp_label21 + "(℃)":[76, 1, -10, ""],
            temp_label22 + "(℃)":[77, 1, -10, ""],
            temp_label23 + "(℃)":[78, 1, -10, ""],
            temp_label24 + "(℃)":[79, 1, -10, ""],
            temp_label25 + "(℃)":[80, 1, -10, ""],
            "均衡电阻温度":[81, 1, -10, "℃"],
            "Pack总充电容量":[82, 2, 1, "AH"],
            "Pack总放电容量":[84, 2, 1, "AH"],
            "Pack总充电Kwh":[86, 2, 1, "Kwh"],
            "Pack总放电Kwh":[88, 2, 1, "Kwh"],
            "Pack总充电时间":[90, 2, 1, "H"],
            "Pack总放电时间":[92, 2, 1, "H"]
        },
        # bms 参数设置
        bms_setting:{
            parset3_label1 + "(V)":[0, 1, 100, "2007"],
            "总体过充告警延时(mS)":[1, 1, 1, "2008"],
            "总体过充告警恢复值(V)":[2, 1, 1000, "2009"],
            parset3_label2 + "(V)":[3, 1, 100, "200a"],
            parset3_label3 + "(V)":[4, 1, 100, "200b"],
            parset3_label4 + "(mS)":[5, 1, 1, "200c"],
            parset1_label1 + "(V)":[6, 1, 1000, "200d"],
            "单体过充告警延时(mS)":[7, 1, 1, "200e"],
            "单体过充告警恢复值(V)":[8, 1, 1000, "200f"],
            parset1_label2 + "(V)":[9, 1, 1000, "2010"],
            parset1_label3 + "(V)":[10, 1, 1000, "2011"],
            parset1_label4 + "(mS)":[11, 1, 1, "2012"],
            parset4_label1 + "(V)":[12, 1, 100, "2013"],
            "总体过放告警延时(mS)":[13, 1, 1, "2014"],
            "总体过放告警恢复值(V)":[14, 1, 1000, "2015"],
            parset4_label2 + "(V)":[15, 1, 100, "2016"],
            parset4_label3 + "(V)":[16, 1, 100, "2017"],
            parset4_label4 + "(mS)":[17, 1, 1, "2018"],
            parset2_label1 + "(V)":[18, 1, 1000, "2019"],
            "单体过放告警延时(mS)":[19, 1, 1, "201a"],
            "单体过放告警恢复值(V)":[20, 1, 1000, "201b"],
            parset2_label2 + "(V)":[21, 1, 1000, "201c"],
            parset2_label4 + "(mS)":[22, 1, 1, "201d"],
            parset2_label3 + "(V)":[23, 1, 1000, "201e"],
            parset8_label1 + "(A)":[24, 1, 100, "201f"],
            "充电过流告警延时(mS)":[25, 1, 1, "2020"],
            "充电过流告警恢复值(V)":[26, 1, 1000, "2021"],
            parset8_label2 + "(A)":[27, 1, 100, "2022"],
            parset8_label3 + "(mS)":[28, 1, 1, "2023"],
            parset8_label4 + "(A)":[29, 1, 100, "2024"],
            parset8_label5 + "(mS)":[30, 1, 1, "2025"],
            "充电过流保护最高次数":[31, 1, 1],
            "启动限流充电电流值":[32, 1, 1],
            "启动限流充电延时":[33, 1, 1],
            "是否启用限流充电":[34, 1, 1],
            parset7_label1 + "(A)":[35, 1, 100, "202a"],
            "放电过流告警延时(mS)":[36, 1, 1, "202b"],
            "放电过流告警恢复值(V)":[37, 1, 1000, "202c"],
            parset7_label2 + "(A)":[38, 1, 100, "202d"],
            parset7_label3 + "(mS)":[39, 1, 1, "202e"],
            parset7_label4 + "(A)":[40, 1, 100, "202f"],
            parset7_label5 + "(mS)":[41, 1, 1, "2030"],
            "放电过流保护最高次数":[42, 1, 1],
            "短路保护电流":[43, 1, 1],
            # parset7_label6 + "(uS)":[44, 1, 1, "2033"],
            "短路保护最高次数":[45, 1, 1],
            parset5_label1 + "(℃)":[46, 1, 10, "2035"],
            "充电高温报警恢复温度":[47, 1, 1],
            parset5_label2 + "(℃)":[48, 1, 10, "2037"],
            parset5_label3 + "(℃)":[49, 1, 10, "2038"],
            parset5_label4 + "(℃)":[50, 1, 10, "2039"],
            "放电高温报警恢复温度":[51, 1, 1],
            parset5_label5 + "(℃)":[52, 1, 10, "203b"],
            parset5_label6 + "(℃)":[53, 1, 10, "203c"],
            parset6_label1 + "(℃)":[54, 1, -10, "203d"],
            "充电低温报警恢复温度":[55, 1, -10],
            parset6_label2 + "(℃)":[56, 1, -10, "203f"],
            parset6_label3 + "(℃)":[57, 1, -10, "2040"],
            parset6_label4 + "(℃)":[58, 1, -10, "2041"],
            "放电低温报警恢复温度":[59, 1, -10],
            parset6_label5 + "(℃)":[60, 1, -10, "2043"],
            parset6_label6 + "(℃)":[61, 1, -10, "2044"],
            "MOS超温报警温度":[62, 1, -1],
            "MOS超温报警恢复温度":[63, 1, -1],
            "MOS超温保护温度":[64, 1, -1],
            "MOS超温保护恢复温度":[65, 1, -1],
            "端子高温告警温度":[66, 1, -1],
            "端子高温告警恢复温度":[67, 1, -1],
            "端子高温保护温度":[68, 1, -1],
            "端子高温保护恢复温度":[69, 1, -1],
            "环境超温报警温度":[70, 1, -1],
            "环境超温报警恢复温度":[71, 1, -1],
            "环境超温保护温度":[72, 1, -1],
            "环境超温保护恢复温度":[73, 1, -1],
            "环境低温报警温度":[74, 1, -1],
            "环境低温报警恢复温度":[75, 1, -1],
            "环境低温保护温度":[76, 1, -1],
            "环境低温保护恢复温度":[77, 1, -1],
            "均衡模式":[78, 1, 1],
            parset5_label7 + "(V)":[79, 1, 1000, "2056"],
            parset5_label8 + "(mV)":[80, 1, 1, "2057"],
            "均衡关闭压差":[81, 1, 1],
            "电芯压差保护开启压差值":[82, 1, 1],
            "电芯压差保护解除压差值":[83, 1, 1],
            parset6_label7 + "(V)":[84, 1, 1000, "205b"],
            parset6_label8 + "(A)":[85, 1, 100, "205c"],
            parset5_label9 + "(V)":[86, 1, 1000, "205d"],
            parset5_label10 + "(min)":[87, 1, 1, "205e"],
            "空闲休眠延时":[88, 1, 1],
            parset6_label9 + "(%)":[89, 1, 1, "2060"],
            "soc报警恢复值":[90, 1, 1]
        },
        # bms 历史数据
        bms_history:{
            bms_history_label1:[0, 3, 1],
            "SOC(%)":[3, 1, 1],
            "SOH(%)":[4, 1, 1],
            bms_history_label2 + "(V)":[5, 1, 100],
            bms_history_label3 + "(A)":[6, 1, -100],
            bms_history_label4 + "1":[7, 1, 1, "", {
                "0":group_tabel9,
                "1":group_tabel10,
                "2":bms_history_label18,
                "3":sys_label1,
                "4":sys_label2,
                "5":bms_history_label19,
                "6":sys_label6,
                "7":sys_label5,
                "8":bms_history_label20,
                "9":sys_label3,
                "10":sys_label4,
                "11":bms_history_label21,
                "12":bms_history_label22,
                "13":bms_history_label23
            }],
            bms_history_label4 + "2":[8, 1, 1, "", {
                "0":bms_history_label24,
                "1":bms_history_label25,
                "2":bms_history_label26,
                "3":bms_history_label27,
                "4":bms_history_label28,
                "5":bms_history_label29,
                "6":'BMS 开机动作',
                "7":'BMS 关机动作',
                "8":'时间校准动作'
            }],
            bms_history_label5 + "1":[9, 1, 1, "", {
                "0":"cell" + bms_parse_label1,
                "1":"cell" + bms_parse_label2,
                "2":"pack" + bms_parse_label1,
                "3":"pack" + bms_parse_label2,
                "4":bms_parse_label3,
                "5":bms_parse_label4,
                "6":bms_parse_label5,
                "7":bms_parse_label6,
                "8":parset5_label2,
                "9":parset5_label5,
                "10":parset6_label2,
                "11":parset6_label5,
                "12":bms_parse_label7,
                "13":bms_parse_label8,
                "14":bms_parse_label9,
                "15":bms_parse_label10
            }],
            bms_history_label5 + "2":[10, 1, 1, "", {
                "0":bms_parse_label36 + "1",
                "1":bms_parse_label37 + "1",
                "2":bms_parse_label36 + "2",
                "3":bms_parse_label37 + "2"
            }],
            bms_history_label6 + "1":[11, 1, 1, "", {
                "0":"cell" + bms_parse_label1,
                "1":"cell" + bms_parse_label2,
                "2":"pack" + bms_parse_label1,
                "3":"pack" + bms_parse_label2,
                "7":bms_parse_label27,
                "8":bms_parse_label28,
                "9":bms_parse_label29,
                "10":bms_parse_label30,
                "11":bms_parse_label31,
                "12":bms_parse_label32,
                "13":bms_parse_label33,
                "14":bms_parse_label34,
                "15":bms_parse_label35
            }],
            bms_history_label6 + "2":[12, 1, 1, "", {
                "0":bms_parse_label36,
                "1":bms_parse_label37
            }],
            bms_history_label7:[13, 1, 1, "", {
                "0":bms_parse_label15,
                "1":bms_parse_label16,
                "2":bms_parse_label17,
                "3":bms_parse_label18,
                "4":bms_parse_label19,
                "5":bms_parse_label20,
                "6":bms_parse_label21,
                "7":bms_parse_label22
            }],
            "cell1" + palnum_label1:[14, 1, 1000],
            "cell2" + palnum_label1:[15, 1, 1000],
            "cell3" + palnum_label1:[16, 1, 1000],
            "cell4" + palnum_label1:[17, 1, 1000],
            "cell5" + palnum_label1:[18, 1, 1000],
            "cell6" + palnum_label1:[19, 1, 1000],
            "cell7" + palnum_label1:[20, 1, 1000],
            "cell8" + palnum_label1:[21, 1, 1000],
            "cell9" + palnum_label1:[22, 1, 1000],
            "cell10" + palnum_label1:[23, 1, 1000],
            "cell11" + palnum_label1:[24, 1, 1000],
            "cell12" + palnum_label1:[25, 1, 1000],
            "cell13" + palnum_label1:[26, 1, 1000],
            "cell14" + palnum_label1:[27, 1, 1000],
            "cell15" + palnum_label1:[28, 1, 1000],
            "cell16" + palnum_label1:[29, 1, 1000],
            bms_history_label8:[30, 1, 1000],
            bms_history_label9:[31, 1, 1000],
            bms_history_label10:[32, 1, 1000],
            palnum_label2 + "1(℃)":[33, 1, -10],
            palnum_label2 + "2(℃)":[34, 1, -10],
            palnum_label2 + "3(℃)":[35, 1, -10],
            palnum_label2 + "4(℃)":[36, 1, -10],
            bms_history_label11:[37, 1, 1],
            bms_history_label12:[37, 1, 1],
            bms_history_label13:[37, 1, -10],
            bms_history_label14:[37, 1, -10],
            f"MOS {palnum_label2}(℃)":[38, 1, -10],
            temp_label19 + "(℃)":[39, 1, -10],
            bms_history_label15 + "(℃)":[40, 1, -10]
        },
        # bms 系统设置页 电量1
        bms_sys_set1:{
            battery_label3 + "(AH)":[0, 1, 100],
            "总容量(AH)":[1, 1, 100],
            battery_label5:[1, 1, 1, "此处不解析"]
        },
        # bms 系统设置页 电量2
        bms_sys_set2:{
            "设计容量(AH)":[0, 1, 100]
        },
        # bms 系统设置页 系统时间
        bms_sys_time:{
            "年月":[0, 1, 1, ''],
            "日时":[1, 1, 1, ''],
            "分秒":[2, 1, 1, ''],
        }
    }
    return bms_data_list