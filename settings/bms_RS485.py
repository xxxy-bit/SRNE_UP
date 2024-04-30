from src.i18n.Bms_i18n import *
from src.OrderList import *

def get_bms_rs485_list():
    bms_rs485_list = {
        # 已被动态获取取代
        "获取PACK模拟量响应信息":{
            "Command":[0, 4, 1, ""],
            "电池单体个数":[4, 4, 1, ""],
            
            f"Cell{palnum_label1}_1":[8, 8, 1, "mV"],
            f"Cell{palnum_label1}_2":[16, 8, 1, "mV"],
            f"Cell{palnum_label1}_3":[24, 8, 1, "mV"],
            f"Cell{palnum_label1}_4":[32, 8, 1, "mV"],
            f"Cell{palnum_label1}_5":[40, 8, 1, "mV"],
            f"Cell{palnum_label1}_6":[48, 8, 1, "mV"],
            f"Cell{palnum_label1}_7":[56, 8, 1, "mV"],
            f"Cell{palnum_label1}_8":[64, 8, 1, "mV"],
            f"Cell{palnum_label1}_9":[72, 8, 1, "mV"],
            f"Cell{palnum_label1}_10":[80, 8, 1, "mV"],
            f"Cell{palnum_label1}_11":[88, 8, 1, "mV"],
            f"Cell{palnum_label1}_12":[96, 8, 1, "mV"],
            f"Cell{palnum_label1}_13":[104, 8, 1, "mV"],
            f"Cell{palnum_label1}_14":[112, 8, 1, "mV"],
            f"Cell{palnum_label1}_15":[120, 8, 1, "mV"],
            f"Cell{palnum_label1}_16":[128, 8, 1, "mV"],
            
            "监测温度个数":[136, 4, 1, ""],
            f"{palnum_label2}_1":[140, 8, -10, "℃"],
            f"{palnum_label2}_2":[148, 8, -10, "℃"],
            f"{palnum_label2}_3":[156, 8, -10, "℃"],
            f"{palnum_label2}_4":[164, 8, -10, "℃"],
            f"{palnum_label2}_5":[172, 8, -10, "℃"],
            f"{palnum_label2}_6":[180, 8, -10, "℃"],
            f"{palnum_label2}_7":[188, 8, -10, "℃"],
            f"{palnum_label2}_8":[196, 8, -10, "℃"],
            f"{palnum_label2}_9":[204, 8, -10, "℃"],
            
            palnum_label3:[212, 8, -100, "A"],              # PACK电流
            f"PACK {paldata_label4}":[220, 8, -100, "V"],    # 总电压
            f"PACK {battery_label3}":[228, 8, 100, "AH"],    # 剩余容量
            "用户自定义个数":[236, 4, 1, ""],
            f"PACK {battery_label4}":[240, 8, 100, "AH"],    # 充满容量
            palnum_label7:[248, 8, 1, ""],                  # 充放电循环次数
            palnum_label8:[256, 8, 100, "AH"],              # PACK设计容量
            "PACK SOC":[264, 8, 1, "%"]
        },
        # 已被动态获取取代
        "获取PACK告警量":{
            "Command":[0, 4, 1, ""],
            "电池单体告警个数":[4, 4, 1, ""],
            
            f"Cell{palnum_label9}_1":[8, 4, 1, ""],
            f"Cell{palnum_label9}_2":[12, 4, 1, ""],
            f"Cell{palnum_label9}_3":[16, 4, 1, ""],
            f"Cell{palnum_label9}_4":[20, 4, 1, ""],
            f"Cell{palnum_label9}_5":[24, 4, 1, ""],
            f"Cell{palnum_label9}_6":[28, 4, 1, ""],
            f"Cell{palnum_label9}_7":[32, 4, 1, ""],
            f"Cell{palnum_label9}_8":[36, 4, 1, ""],
            f"Cell{palnum_label9}_9":[40, 4, 1, ""],
            f"Cell{palnum_label9}_10":[44, 4, 1, ""],
            f"Cell{palnum_label9}_11":[48, 4, 1, ""],
            f"Cell{palnum_label9}_12":[52, 4, 1, ""],
            f"Cell{palnum_label9}_13":[56, 4, 1, ""],
            f"Cell{palnum_label9}_14":[60, 4, 1, ""],
            f"Cell{palnum_label9}_15":[64, 4, 1, ""],
            f"Cell{palnum_label9}_16":[68, 4, 1, ""],
            "监测温度告警个数":[72, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_1":[76, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_2":[80, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_3":[84, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_4":[88, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_5":[92, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_6":[96, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_7":[100, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_8":[104, 4, 1, ""],
            f"{palnum_label2}{palnum_label9}_9":[108, 4, 1, ""],
            
            palnum_label10:[112, 4, 1, ""],
            palnum_label11:[116, 4, 1, ""],
            palnum_label12:[120, 4, 1, ""],
            f"{group_tabel10}_1":[124, 4, 1, "", {
                "0":bms_rs485_label1,
                "1":parset2_label2,
                "2":bms_rs485_label2,
                "3":bms_rs485_label3,
                "4":bms_rs485_label4,
                "5":bms_rs485_label5,
                "6":bms_rs485_label6
            }],
            f"{group_tabel10}_2":[128, 4, 1, "", {
                "0":parset5_label2,
                "1":parset5_label5,
                "2":parset6_label2,
                "3":parset6_label5,
                "4":bms_parse_label7,
                "5":bms_parse_label8,
                "6":bms_parse_label9,
                "7":bms_rs485_label7
            }],
            palnum_label14:[132, 4, 1, "", {
                "0":bms_rs485_label8,
                "1":"CFET",
                "2":"DFET",
                "3":bms_rs485_label9,
                "4":bms_history_label20,
                "5":"ACin",

                "7":bms_rs485_label10
                }],
            palnum_label15:[136, 4, 1, "", {
                "0":bms_rs485_label11,

                "4":bms_rs485_label12,
                "5":f"LED{palnum_label9}"
            }],
            group_tabel8:[140, 4, 1, "", {
                "0":bms_rs485_label13,
                "1":bms_rs485_label14,
                "2":bms_parse_label17,
                
                "4":bms_rs485_label15,
                "5":bms_parse_label19
            }],
            f"{palnum_label16}_1":[144, 4, 1, ""],
            f"{palnum_label16}_2":[148, 4, 1, ""],
            f"{group_tabel9}_1":[152, 4, 1, "", {
                "0":bms_rs485_label16,
                "1":bms_rs485_label17,
                "2":bms_rs485_label18,
                "3":bms_rs485_label19,
                "4":bms_parse_label36,
                "5":bms_parse_label37
            }],
            f"{group_tabel9}_2":[156, 4, 1, "", {
                "0":bms_parse_label28,
                "1":bms_parse_label29,
                "2":bms_parse_label30,
                "3":bms_parse_label31,
                "4":bms_parse_label32,
                "5":bms_parse_label33,
                "6":bms_parse_label34,
                "7":bms_rs485_label20
            }]
        },
        # 静态获取
        "获取电池系统运行模拟量信息":{
            "电池组系统总平均电压":[0, 8, 100, ""],
            "电池组系统总电流":[8, 16, -100, ""],
            "电池组系统SOC":[24, 4, 1, ""],
            # "平均循环次数":[28, 8, 1, ""],
            # "最大循环次数":[36, 8, 1, ""],
            # "平均SOH":[44, 4, 1, ""],
            # "最小SOH":[48, 4, 1, ""],
            "单芯最高电压":[52, 8, 1, ""],
            "单芯最高电压所在模块":[60, 8, 1, ""],
            "单芯最低电压":[68, 8, 1, ""],
            "单芯最低电压所在模块":[76, 8, 1, ""],
            # "单芯平均温度":[84, 8, 1, ""],
            "单芯最高温度":[92, 8, -10, ""],
            "单芯最高温度所在模块":[100, 8, 1, ""],
            "单芯最低温度":[108, 8, -10, ""],
            "单芯最低温度所在模块":[116, 8, 1, ""],
            # "MOSFET平均温度":[124, 8, 1, ""],
            # "MOSFET最高温度":[132, 8, 1, ""],
            # "MOSFET最高温度所在模块":[140, 8, 1, ""],
            # "MOSFET最低温度":[148, 8, 1, ""],
            # "MOSFET最低温度所在模块":[156, 8, 1, ""],
            # "BMS平均温度":[164, 8, 1, ""],
            # "BMS最高温度":[172, 8, 1, ""],
            # "BMS最高温度所在模块":[180, 8, 1, ""],
            # "BMS最低温度":[188, 8, 1, ""],
            # "BMS最低温度所在模块":[196, 8, 1, ""],
        }
    }
    return bms_rs485_list