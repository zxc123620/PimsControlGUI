#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :tool.py
# @Time      :2025/7/10 11:21
# @Author    :zhouxiaochuan
# @Description:
from binascii import unhexlify

from crcmod import crcmod


def crc_16_modbus(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "")  # 消除空格
    read_crc_out = hex(crc16(unhexlify(data))).upper()
    # print(read_crc_out)
    str_list = list(read_crc_out)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list)  # 用""把数组的每一位结合起来  组成新的字符串
    read = crc_data[4:] + crc_data[2:4]  # 把源代码和crc校验码连接起来
    return read.lower()

