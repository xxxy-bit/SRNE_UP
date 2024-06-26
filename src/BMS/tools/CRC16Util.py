def calc_crc(data: str):
    data = bytearray.fromhex(data)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    crc = hex(((crc & 0xff) << 8) + (crc >> 8))[2:]

    while len(crc) < 4:
        crc = '0' + str(crc)

    return crc

if __name__ == '__main__':
    # crc = calc_crc('01 03 BC 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0001 0002 0003 0004')
    crc = calc_crc('0103f0000001')
    print(crc)



