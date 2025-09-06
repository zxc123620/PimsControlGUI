#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :basic_format.py
# @Time      :2025/8/9 10:24
# @Author    :zhouxiaochuan
# @Description:
import datetime
import logging

from collection_module.tool import crc_16_modbus


class BasicFormat:
    IP_BYTE_NUM = 4
    PORT_BYTE_NUM = 2
    HEADER_BYTE_NUM = 2  # 头部信息字节数
    MAC_ADDRESS_BYTE_NUM = 6  # MAC地址字节数
    DEVICE_ID_BYTE_NUM = 2  # 设备ID字节数
    HEADER_TIME_BYTE_NUM = 6  # 头部时间字节数
    DATA_LENGTH_BYTE_NUM = 2  # 数据长度字节数
    FUNCTION_CODE_BYTE_NUM = 2  # 功能码字节数
    CONTROL_CODE_BYTE_NUM = 2  # 控制指令字节数
    ISVALID = ["离线", "在线"]
    DOOR_STATE = ["开门", "关门"]
    ENABLE = ["停用", "启用"]
    COMMAND_STR = [ "关闭","开启"]
    NTP_TYPE = ["手动", "NTP", "域名"]
    DEFENCE_STATE = ["撤防", "布防"]

    def __init__(self, function_code, data_raw):
        self.function_code = function_code
        start_index = 0
        end_index = start_index + self.HEADER_BYTE_NUM * 2
        self.header = data_raw[start_index:end_index]  # 头部
        start_index = end_index
        end_index = start_index + self.DEVICE_ID_BYTE_NUM * 2
        self.header_device_id = data_raw[start_index:end_index]  # 设备ID
        start_index = end_index
        end_index = start_index + self.FUNCTION_CODE_BYTE_NUM * 2
        self.function_code_raw = data_raw[start_index:end_index]  # 功能码
        start_index = end_index
        end_index = start_index + self.HEADER_TIME_BYTE_NUM * 2
        self.server_date = data_raw[start_index:end_index]  # 日期
        start_index = end_index
        end_index = start_index + self.DATA_LENGTH_BYTE_NUM * 2
        self.date_length = int(self.convert(data_raw[start_index:end_index]), 16)  # 长度
        # logging.info(f"数据长度:{self.date_length}")
        self.data_inner = data_raw[end_index:-4] # 数据区
        data_inner_set = set(self.data_inner)
        self.crc_data = data_raw[-4:]  # crc数据
        if len(data_inner_set) == 1 and "0" in data_inner_set:
            self.valid_data()

    def valid_data(self):
        """
        校验
        :return:
        """
        data_inner_length = int(len(self.data_inner) / 2)
        crc_16_data = str(crc_16_modbus(self.data_inner))
        try:
            assert data_inner_length == self.date_length, f"数据长度校验错误:{data_inner_length} != {self.date_length}"
            assert crc_16_data == self.crc_data, f"CRC校验错误:{crc_16_data} != {self.crc_data}"
        except AssertionError as e:
            logging.exception(e)
            logging.info(str(e))

    @staticmethod
    def convert(data):
        """
        转换 1234 转换为3412
        :param data:
        :return:
        """
        data_converted = ''
        for i in range(2, len(data), 4):
            data_converted += data[i:i + 2] + data[i - 2:i]

        return data_converted

    @staticmethod
    def get_addr_text(data):
        """
        解析为IP地址信息
        :param data:
        :return:
        """
        return f"{int(data[:2], 16)}.{int(data[2:4], 16)}.{int(data[4:6], 16)}.{int(data[6:8], 16)}"

    @staticmethod
    def convert_addr_to_hex(data: str):
        """
        将IP地址转换为在16进制
        :param data:
        :return:
        """
        result = ''
        data_list = data.split(".")
        for data in data_list:
            result += f"{int(data):02x}"
        return result

    @staticmethod
    def get_date_text(data):
        """
        获取时间格式化字符串
        :param data:
        :return:
        """
        year = int(data[0:4], 16)
        month = int(data[4:8], 16)
        day = int(data[8:12], 16)
        hour = int(data[12:16], 16)
        minute = int(data[16:20], 16)
        seconds = int(data[20:24], 16)
        return f"{year}年{month}月{day}日{hour}时{minute}分{seconds}秒"

    @staticmethod
    def get_datetime_format(data):
        year = int(data[0:2], 16) + 2000
        month = int(data[2:4], 16)
        day = int(data[4:6], 16)
        hour = int(data[6:8], 16)
        minute = int(data[8:10], 16)
        second = int(data[10:12], 16)
        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def get_infos(self):
        return f"设备ID: {self.header_device_id}, 数据长度: {self.date_length},功能码: {self.function_code_raw},  "