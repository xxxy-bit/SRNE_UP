from src.i18n.Bms_i18n import *
from src.OrderList import *

def get_bms_rs485_list():
    bms_rs485_list = {
        "获取 PACK 模拟量响应信息":{
            "Command":[0, 4, 1, ""],
            "电池单体个数":[4, 4, 1, ""],
            "cell1电压":[8, 8, 1, "mV"],
            "cell2电压":[16, 8, 1, "mV"],
            "cell3电压":[24, 8, 1, "mV"],
            "cell4电压":[32, 8, 1, "mV"],
            "cell5电压":[40, 8, 1, "mV"],
            "cell6电压":[48, 8, 1, "mV"],
            "cell7电压":[56, 8, 1, "mV"],
            "cell8电压":[64, 8, 1, "mV"],
            "cell9电压":[72, 8, 1, "mV"],
            "cell10电压":[80, 8, 1, "mV"],
            "cell11电压":[88, 8, 1, "mV"],
            "cell12电压":[96, 8, 1, "mV"],
            "cell13电压":[104, 8, 1, "mV"],
            "cell14电压":[112, 8, 1, "mV"],
            "cell15电压":[120, 8, 1, "mV"],
            "cell16电压":[128, 8, 1, "mV"],
            "监测温度个数":[136, 4, 1, ""],
            "温度1":[140, 8, -1, "℃"],
            "温度2":[148, 8, -1, "℃"],
            "温度3":[156, 8, -1, "℃"],
            "温度4":[164, 8, -1, "℃"],
            "温度5":[172, 8, -1, "℃"],
            "温度6":[180, 8, -1, "℃"],
            "温度7":[188, 8, -1, "℃"],
            "温度8":[196, 8, -1, "℃"],
            "温度9":[204, 8, -1, "℃"],
            "PACK电流":[212, 8, -1, "mV"],
            "PACK总电流":[220, 8, -1, "mV"],
            "PACK剩余容量":[228, 8, 1, "AH"],
            "用户自定义个数":[236, 4, 1, ""],
            "PACK满充容量":[240, 8, 1, "AH"],
            "充放电循环次数":[248, 8, 1, ""],
            "PACK设计容量":[256, 8, 1, "AH"],
            "PACK SOC":[264, 8, 1, "%"]
        },
        "获取 PACK 告警量":{
            "Command":[0, 4, 1, ""],
            "电池单体告警个数":[4, 4, 1, ""],
            "cell1告警":[8, 4, 1, ""],
            "cell2告警":[12, 4, 1, ""],
            "cell3告警":[16, 4, 1, ""],
            "cell4告警":[20, 4, 1, ""],
            "cell5告警":[24, 4, 1, ""],
            "cell6告警":[28, 4, 1, ""],
            "cell7告警":[32, 4, 1, ""],
            "cell8告警":[36, 4, 1, ""],
            "cell9告警":[40, 4, 1, ""],
            "cell10告警":[44, 4, 1, ""],
            "cell11告警":[48, 4, 1, ""],
            "cell12告警":[52, 4, 1, ""],
            "cell13告警":[56, 4, 1, ""],
            "cell14告警":[60, 4, 1, ""],
            "cell15告警":[64, 4, 1, ""],
            "cell16告警":[68, 4, 1, ""],
            "监测温度告警个数":[72, 4, 1, ""],
            "温度1告警":[76, 4, 1, ""],
            "温度2告警":[80, 4, 1, ""],
            "温度3告警":[84, 4, 1, ""],
            "温度4告警":[88, 4, 1, ""],
            "温度5告警":[92, 4, 1, ""],
            "温度6告警":[96, 4, 1, ""],
            "温度7告警":[100, 4, 1, ""],
            "温度8告警":[104, 4, 1, ""],
            "温度9告警":[108, 4, 1, ""],
            "PACK充电电流告警":[112, 4, 1, ""],
            "PACK总电压告警":[116, 4, 1, ""],
            "PACK放电电流告警":[120, 4, 1, ""],
            "保护状态1":[124, 4, 1, "", {
                "0":"单体过压保护",
                "1":"单体过放保护",
                "2":"总压过压保护",
                "3":"总压过放保护",
                "4":"充电过流保护",
                "5":"放电过流保护",
                "6":"短路"
            }],
            "保护状态2":[128, 4, 1, "", {
                "0":"充电高温保护",
                "1":"放电高温保护",
                "2":"充电低温保护",
                "3":"放电低温保护",
                "4":"MOS高温保护",
                "5":"环境高温保护",
                "6":"环境低温保护",
                "7":"Fully充满"
            }],
            "指示状态":[132, 4, 1, "", {
                "0":"限流",
                "1":"CFET",
                "2":"DFET",
                "3":"Pack供电",
                "4":"充电器反接",
                "5":"ACin",

                "7":"加热膜"
                }],
            "控制状态":[136, 4, 1, "", {
                "0":"蜂鸣器告警",

                "4":"充电限流",
                "5":"LED告警"
            }],
            "故障状态":[140, 4, 1, "", {
                "0":"充电MOS故障",
                "1":"放电MOS故障",
                "2":"温度传感器故障",
                
                "4":"电芯故障",
                "5":"采样故障"
            }],
            "均衡状态1":[144, 4, 1, ""],
            "均衡状态2":[148, 4, 1, ""],
            "告警状态1":[152, 4, 1, "", {
                "0":"单体过压",
                "1":"单体低压",
                "2":"总压过压",
                "3":"总压低压",
                "4":"充电过流",
                "5":"放点过流"
            }],
            "告警状态2":[156, 4, 1, "", {
                "0":"充电高温",
                "1":"放电高温",
                "2":"充电低温",
                "3":"放点低温",
                "4":"环境高温",
                "5":"环境低温",
                "6":"MOS高温",
                "7":"低电量"
            }]
        }
    }
    return bms_rs485_list