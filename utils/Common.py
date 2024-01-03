import serial.tools.list_ports
import datetime, os


class Common():
    def __init__(self) -> None:
        pass
    
    # 去掉小数点多余的0
    @classmethod
    def format_num(cls, num):
        s = str(num)
        index = s.find('.')
        if s[index+1:].strip('0') == '':
            return int(s[:index])
        else:
            return num
    
    # 进行 RS485 校验和码计算
    @classmethod
    def rs485_chksum(cls, num):
        num = num.replace(' ', '')[2:]

        # CHKSUM 的计算是除 SOI、EOI 和 CHKSUM 外，其他字符按 ASCII 码值累加求和，所得结果模 65536 余数取反加 1
        chksum = 0
        
        # 除 SOI、EOI 和 CHKSUM 外其他值以16进制相加
        for i in range(0, len(num), 2):
            chksum += int(num[i:i+2], 16)
            
        # 10进制模65536后取反加1
        chksum = list(f'{chksum % 65536:016b}')   # 模65536
        for i in range(len(chksum)):        # 取反
            if chksum[i] == '0':
                chksum[i] = '1'
            else:
                chksum[i] = '0'
        chksum = int(''.join(chksum), 2)+1  # 加一
        chksum = f'{chksum:04x}'.upper()
        chksum_hex = ''
        for i in chksum:                    # 转16进制
            chksum_hex += hex(ord(i))[2:]
        return chksum_hex

    # 符号位的换算
    @classmethod
    def signBit_func(cls, num):
        """符号位转换正负
        例如num = FF36
        if FF36 > 7FFF:
            -(10000 - FF36)
        else:
            FF36
        """
        resF = int(num, 16)
        if resF > int('7FFF', 16):
            return -(int('FFFF', 16) - resF)
        else:
            return resF
    
    # 加载串口列表
    @classmethod
    def load_serial_list(cls):
        port_list = list(serial.tools.list_ports.comports())
        port_choice = [num.device for num in port_list]
        return port_choice

    # 创建日志文件
    @classmethod
    def creat_log_file(cls, log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        cls.now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        cls.log_name = os.path.join(log_dir, f'{cls.now}.txt')
        return cls.log_name