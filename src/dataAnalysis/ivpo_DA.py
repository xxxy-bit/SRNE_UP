import os, sys, binascii
from utils.Common import Common
from utils.CRC16Util import calc_crc
from settings.ivpo_modbus import ivpo_data_list
from src.OrderList import *


# 解析 工频离网逆变器 数据
def ivpo_data_analysis(res, send_data):
    '''
        res:        串口接收的数据
        send_data:  串口发送的数据
    '''

    # 0、记录原始数据res
    source_res = res
    
    # 1、校验码校验
    crc16 = calc_crc(res[:-4])
    if crc16 != res[-4:]:
        return (0, f'正确校验码为:{crc16},数据包的校验码为:{res[-4:]}')

    # 2、数据切割，去掉 地址码、功能码、校验码 ，按照2字节为1长度转成列表
    res = res[6:-4]
    data_cut = [res[i:i+4] for i in range(0, len(res), 4)]

    # 3、解析协议内容
    print_dic = {}

    # 实时监控
    # 产品信息区
    if send_data == ivpo_product_msg:
        for k,v in ivpo_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if k == '系统电压':
                temp = int(temp[0][:2], 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
            elif k == '产品类型':
                for a,b in v[4].items():
                    if temp[0][2:] == a:
                        print_dic[k] = f'{b}'
            elif k == '产品型号':
                temp = ''.join(str(i) for i in temp)
                temp = binascii.a2b_hex(temp)
                temp = str(temp)[2:-1].strip()
                print_dic[k] = f'{temp}'
            elif k == '软件版本':
                # temp1 = int(temp[0][:2], 16)
                temp2 = int(temp[0][2:], 16)
                temp3 = int(temp[1][:2], 16)
                temp4 = int(temp[1][2:], 16)
                print_dic[k] = f'V{temp2}.{temp3}.{temp4}'
            elif k == '硬件版本':
                temp3 = int(temp[1][:2], 16)
                temp4 = int(temp[1][2:], 16)
                print_dic[k] = f'V{temp3}.{temp4}'
            elif k == '产品序列号':
                temp = ''.join(str(i) for i in temp)
                temp = f'{int(temp[:2], 16):02}{int(temp[2:4], 16):02}{int(temp[4:], 16):04}'
                print_dic[k] = f'{temp}'
            elif k == '设备名称':
                temp = ''.join(str(i) for i in temp)
                temp = binascii.a2b_hex(temp)
                temp = temp.decode('gb2312')
                temp = (temp.replace('\x00', '')).strip()
                print_dic[k] = f'{temp}'
            else:
                temp = int(''.join(str(i) for i in temp), 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
    
    # 控制器数据区
    elif send_data == ivpo_control_msg:
        for k,v in ivpo_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if k == '充电状态':
                temp = temp[0][2:]
                for a, b in v[4].items():
                    if temp == a:
                        print_dic[k] = b
            else:
                temp = int(''.join(str(i) for i in temp), 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
                
    # 逆变数据区
    elif send_data == ivpo_ivt_msg:
        for k,v in ivpo_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if k == '当前故障码':
                # error_info0 = bin(int(temp[0], 16))[2:].rjust(16, '0')
                # error_info1 = bin(int(temp[1], 16))[2:].rjust(16, '0')
                error_info2 = bin(int(temp[2], 16))[2:].rjust(16, '0')
                error_info3 = bin(int(temp[3], 16))[2:].rjust(16, '0')
                error_info = f'{error_info2}{error_info3}'
                # error_info = f'{error_info0}{error_info1}{error_info2}{error_info3}'
                
                total_list = []
                for k2, v2 in v[4].items():
                    if error_info[-(int(k2)+1)] == '1':
                        total_list.append(v2)
                print_dic[k] = ', '.join(total_list)
                
            elif k == '当前时间':
                year = int(temp[0][:2], 16)
                month = int(temp[0][2:], 16)
                day = int(temp[1][:2], 16)
                hour = int(temp[1][2:], 16)
                minute = int(temp[2][:2], 16)
                second = int(temp[2][2:], 16)
                
                if year == 0:
                    time = 'not set'
                else:
                    time = f'{year}/{month}/{day} {hour}:{minute}:{second}'
                print_dic[k] = time
            else:
                temp = int(''.join(str(i) for i in temp), 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
                
    # 总运行天数
    elif send_data == ivpo_history_days:
        for k,v in ivpo_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            
            temp = int(temp[0], 16)
            print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
        
    # 用户设置区1
    elif send_data == ivpo_setting1:
        for k,v in ivpo_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]

            if k == '电池充电下限温度(℃)':
                # 取低8位： b7:符号位(0表示+，1表示 - ) b0-b6:温度值
                temp = bin(int(temp[0][2:], 16))[2:].rjust(8, '0')
                tp = int(temp[1:],2)
                if temp[0] == '1':
                    tp = -(tp)
                print_dic[k] = f'{tp}'
            elif k == '温度补偿系数(mV/℃/2V)':
                temp = int(temp[0], 16)
                if temp != 0:
                    temp = -(temp)
                print_dic[k] = temp
            else:
                temp = int(temp[0], 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])}'
        
    # 用户设置区2
    elif send_data == ivpo_setting2:
        for k,v in ivpo_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            
            temp = int(temp[0], 16)
            print_dic[k] = f'{Common.format_num(temp / v[2])}'
        
    return print_dic, source_res
    
    