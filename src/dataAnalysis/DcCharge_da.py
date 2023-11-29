import binascii
from src.OrderList import *
from utils.Common import Common
from utils.CRC16Util import calc_crc
from settings.dc_modbus import dc_data_list


# 解析 AC充电器 协议数据
def dc_data_analysis(res, send_data):
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
    
    # 实时监控-产品信息
    if send_data == dc_product_monitor:
        for k,v in dc_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if k == '系统电压':
                temp = int(temp[0][:2], 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
            elif k == '额定充电电流':
                temp = int(temp[0][2:], 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
            elif k == '产品类型':
                for a,b in v[4].items():
                    if temp[0][2:] == a:
                        print_dic[k] = f'{b}'
            elif k == '产品规格':
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
            elif k == '设备地址':
                temp = int(temp[0], 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
            elif k == 'CAN程序版本':
                temp1 = int(temp[0][:2], 16)
                temp2 = int(temp[0][2:], 16)
                temp3 = int(temp[1][:2], 16)
                temp4 = int(temp[1][2:], 16)
                print_dic[k] = f'V{temp1}.{temp2}.{temp3}.{temp4}'
            elif k == '设备名字':
                temp = ''.join(str(i) for i in temp)
                temp = binascii.a2b_hex(temp)
                temp = temp.decode('gb2312')
                temp = (temp.replace('\x00', '')).strip()
                print_dic[k] = f'{temp}'
    # 实时监控-控制器区域
    elif send_data == dc_control_monitor:
        for k,v in dc_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            if k == '设备温度':
                temp = bin(int(temp[0][:2], 16))[2:].rjust(8, '0')
                tp = int(temp[1:],2)
                if temp[0] == '1':
                    tp = -(tp)
                print_dic[k] = f'{tp} {v[3]}'
            elif k == '蓄电池温度':
                temp = bin(int(temp[0][2:], 16))[2:].rjust(8, '0')
                tp = int(temp[1:],2)
                if temp[0] == '1':
                    tp = -(tp)
                print_dic[k] = f'{tp} {v[3]}'
            elif k == '充电状态':
                temp = temp[0][2:]
                for a, b in v[4].items():
                    if temp == a:
                        print_dic[k] = b
            elif k == '控制器故障/告警信息1':
                error_info = bin(int(temp[0], 16))[2:].rjust(16, '0')
                total_list = []
                for ea, eb in v[4].items():
                    if error_info[-(int(ea)+1)] == '1':
                        total_list.append(eb)
                warn_info = bin(int(temp[1], 16))[2:].rjust(16, '0')
                for wa, wb in v[5].items():
                    if warn_info[-(int(wa)+1)] == '1':
                        total_list.append(wb)
                print_dic[k] = ', '.join(total_list)
            else:
                temp = int(''.join(str(i) for i in temp), 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])} {v[3]}'
    # 参数设置区域
    elif send_data == dc_setting:
        for k,v in dc_data_list[send_data].items():
            temp = data_cut[v[0]:v[0]+v[1]]
            
            if k == '系统电压设置':
                temp = int(temp[0][2:], 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])}'
            elif k == '蓄电池类型':
                temp = int(temp[0], 16)
                if temp == 11:
                    temp = 5
                print_dic[k] = temp
            else:
                temp = int(''.join(str(i) for i in temp), 16)
                print_dic[k] = f'{Common.format_num(temp / v[2])}'
            
    return print_dic, source_res
    
    