#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from settings.bms_modbus import get_bms_modbus_list
from src.i18n.Bms_i18n import *
from src.OrderList import *
# from src.BMS.tools.Common import Common
from utils.Common import Common
from src.BMS.tools.CRC16Util import calc_crc

sys.path.append(os.getcwd())

# 解析数据
def pars_data(res, data):
    '''
        res: 接收的数据
        data: 解析的字典
    '''
    
    # 1、校验码校验
    crc16 = calc_crc(res[:-4])

    if crc16 != res[-4:]:
        return (0, f'正确校验码为:{crc16},数据包的校验码为:{res[-4:]}')

    # 2、数据切割，去掉 地址码、功能码、校验码 ，按照2字节为1长度转成列表
    res = res[6:-4]
    data_cut = [res[i:i+4] for i in range(0, len(res), 4)]

    # 3、加载协议内容并解析
    # with open(os.path.join(os.getcwd(), 'settings', 'MODBUS.json'), 'r', encoding='utf-8') as f:
    #     json_file = json.load(f)
    json_file = get_bms_modbus_list()
    print_dic = {}
    # 实时监控
    if data[:-4] == bms_monitor:
        for k,v in json_file[bms_monitor].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if k == 'BMS工作状态1' or k == 'BMS工作状态2' or k == '故障位' or k == '警告位1' \
            or k == '警告位2' or k == '保护位1' or k == '保护位2':
                temp = bin(int(temp[0], 16))[2:].rjust(16, '0')
                error_list = []
                for a,b in v[4].items():
                    if temp[-(int(a)+1)] == '1':
                        error_list.append(b)
                print_dic[k] = error_list
            else:
                if v[2] < 0:
                    # print(f'{k}:{temp}')
                    resF = f'{Common.format_num(Common.signBit_func(temp[0]) / abs(v[2]))}'
                    print_dic[k] = f'{resF}{v[3]}'
                else:
                    temp = int(''.join(str(i) for i in temp), 16)
                    print_dic[k] = f'{Common.format_num(temp / v[2])}{v[3]}'
    # 参数设置
    elif data[:-4] == bms_setting:
        for k,v in json_file[bms_setting].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if v[2] < 0:
                resF = f'{Common.format_num(Common.signBit_func(temp[0]) / abs(v[2]))}'
                print_dic[k] = f'{resF}'
            else:
                temp = int(''.join(str(i) for i in temp), 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])}'
    # 历史记录
    elif data[:5] == bms_history[:5]:
        for k,v in json_file[bms_history].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if k == bms_history_label1:
                # 年/月
                year = f'{int(temp[0][:2], 16):02}/'
                month = f'{int(temp[0][2:], 16):02}/'
                # 日/时
                day = f'{int(temp[1][:2], 16):02} '
                hour = f'{int(temp[1][2:], 16):02}'
                # 分/秒
                minute = f'{int(temp[2][:2], 16):02}'
                second = f'{int(temp[2][2:], 16):02}'
                print_dic[k] = f'{year}{month}{day} {hour}:{minute}:{second}'
            elif k == bms_history_label4 + '1' or k == bms_history_label4 + '2' or k == bms_history_label7 or k == bms_history_label6 + '1' \
            or k == bms_history_label6 + '2' or k == bms_history_label5 + '1' or k == bms_history_label5 + '2':
                temp = data_cut[v[0]:v[0]+v[1]]
                temp = bin(int(temp[0], 16))[2:].rjust(16, '0')
                error_list = []
                for a,b in v[4].items():
                    if temp[-(int(a)+1)] == '1':
                        error_list.append(b)
                txt = ', '.join(str(i) for i in error_list)
                print_dic[k] = txt
            elif k == bms_history_label11:
                print_dic[k] = f'{int(temp[0][0], 16)+1}'
            elif k == bms_history_label12:
                print_dic[k] = f'{int(temp[0][1], 16)+1}'
            elif k == bms_history_label13:
                print_dic[k] = f'{int(temp[0][2], 16)+1}'
            elif k == bms_history_label14:
                print_dic[k] = f'{int(temp[0][3], 16)+1}'
            else:
                if v[2] < 0:
                    resF = f'{Common.format_num(Common.signBit_func(temp[0]) / abs(v[2]))}'
                    print_dic[k] = f'{resF}'
                else:
                    temp = int(''.join(str(i) for i in temp), 16)
                    print_dic[k] = f'{Common.format_num(temp / v[2])}'
    # 系统设置-剩余容量，总容量
    elif data[:-4] == bms_sys_set1:
        for k,v in json_file[bms_sys_set1].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            temp = int(''.join(str(i) for i in temp), 16)
            print_dic[k] = f'{Common.format_num(temp / v[2])}'
    # 系统设置-设计容量
    elif data[:-4] == bms_sys_set2:
        for k,v in json_file[bms_sys_set2].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            temp = int(''.join(str(i) for i in temp), 16)
            print_dic[k] = f'{Common.format_num(temp / v[2])}'
    # 系统设置-系统时间
    elif data[:-4] == bms_sys_time:
        for k,v in json_file[bms_sys_time].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            hight_eight = int(temp[0][:2], 16)
            low_eight = int(temp[0][2:], 16)
            print_dic[k] = f'{hight_eight}/{low_eight}'
            
    return print_dic