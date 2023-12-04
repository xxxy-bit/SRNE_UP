# 读取日志文件内容
with open(f'\\log\\2023-12-04_11_49_42.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 遍历每两行进行判断
for i in range(len(lines) - 1):
    line1 = lines[i].strip()
    line2 = lines[i + 1].strip()

    # 判断连续两行是否都包括"send"或"receive"字段
    if "send" in line1 and "send" in line2:
        print('send:' + line1)
    elif "receive" in line1 and "receive" in line2:
        print('receive:' + line1)
    