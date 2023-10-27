import os, sys, binascii
from utils.Common import Common
from utils.CRC16Util import calc_crc
from settings.ivpo_modbus import ivpo_data_list
from src.OrderList import *


# 解析 工频离网逆变器 数据
def ivpo_data_analysis(res, send_data):
    '''
        res: 串口接收到的数据
        send_data: 给串口发送的指令
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
    if send_data == ivpo_product_msg:
        ...
        
    
    return print_dic, source_res
    
    