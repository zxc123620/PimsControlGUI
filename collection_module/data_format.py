#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :data_fromat_emum.py
# @Time      :2025/6/20 16:54
# @Author    :zhouxiaochuan
# @Description:
import binascii
import logging

from collection_module.function_code import FunctionCode, ConnectStatusCode


class BasicFormat:
    ISVALID = ["离线", "在线"]
    DOOR_STATE = ["开门", "关门"]
    ENABLE = ["停用", "启用"]
    NTP_TYPE = ["手动", "NTP", "域名"]

    def __init__(self, function_code, data_raw):
        self.function_code = function_code
        self.header = data_raw[0:4]
        self.device_id = data_raw[4:8]
        self.function_code_raw = data_raw[8:12]
        self.date_length = int(data_raw[16:12:-1], 16)
        self.data_inner = data_raw[16:-4]

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


class HumAndTempData(BasicFormat):

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_HUM_TMP, data_raw)
        data_inner_converted = self.convert(self.data_inner)
        # self.year = int(data_inner_converted[0:4], 16)
        # self.month = int(data_inner_converted[4:8], 16)
        # self.day = int(data_inner_converted[8:12], 16)
        # self.hour = int(data_inner_converted[12:16], 16)
        # self.minute = int(data_inner_converted[16:20], 16)
        # self.seconds = int(data_inner_converted[20:24], 16)
        self.device_date_text = self.get_date_text(data_inner_converted[0:24])
        self.hum_state = int(data_inner_converted[24:28], 16)
        self.hum_state_text = self.ISVALID[self.hum_state]
        self.tem_data = float(int(data_inner_converted[28:32], 16) / 10)
        self.hum_data = float(int(data_inner_converted[32:36], 16) / 10)
        self.door_state = int(data_inner_converted[36:40], 16)
        self.door_state_text = self.DOOR_STATE[self.door_state]


class HeartBeatData(BasicFormat):
    def __init__(self, data_raw):
        " 19 00 06 00 18 00 11 00 30 00 2B  00 20 25 06 23 "
        BasicFormat.__init__(self, FunctionCode.HEARTBEAT, data_raw)
        data_inner_converted = self.convert(self.data_inner[:-8])
        # self.year = int(data_inner_converted[0:4], 16)
        # self.month = int(data_inner_converted[4:8], 16)
        # self.day = int(data_inner_converted[8:12], 16)
        # self.hour = int(data_inner_converted[12:16], 16)
        # self.minute = int(data_inner_converted[16:20], 16)
        # self.seconds = int(data_inner_converted[20:24], 16)
        self.fc_version = self.data_inner[24:32]
        self.device_date_text = self.get_date_text(data_inner_converted[0:24])


class NetData(BasicFormat):
    """
    网络参数
    """

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_NET_DATA, data_raw)
        data_inner_converted = self.convert(self.data_inner)
        self.ip_addr_text = self.get_addr_text(self.data_inner[0:8])
        self.ip_port = int(data_inner_converted[8:12], 16)
        self.gateway_text = self.get_addr_text(self.data_inner[12:20])
        self.mask_text = self.get_addr_text(self.data_inner[20:28])
        self.mac = f"{self.data_inner[28:30]}:{self.data_inner[30:32]}:{self.data_inner[32:34]}:{self.data_inner[34:36]}:{self.data_inner[36:38]}:{self.data_inner[38:40]}"
        self.dns_1_text = self.get_addr_text(self.data_inner[40:48])
        self.dns_2_text = self.get_addr_text(self.data_inner[48:56])
        self.heartbeat_interval = int(data_inner_converted[56:60], 16)


class DeviceData(BasicFormat):
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_DEVICE_DATA, data_raw)
        data_inner_converted = self.convert(self.data_inner)
        self.device_id_2 = data_inner_converted[:4]  # 设备ID
        self.hum_enable = int(data_inner_converted[4:8], 16)  # 传感器使能
        self.hum_id = int(data_inner_converted[8:12], 16)  # 温湿度ID
        # self.fan_open_temp = float(int(data_inner_converted[12:16], 16) / 10)
        # self.fan_close_temp = float(int(data_inner_converted[16:20], 16) / 10)
        self.fan_open_temp = int(data_inner_converted[12:16], 16)  # 风扇开启温度
        self.fan_close_temp = int(data_inner_converted[16:20], 16)  # 风扇关闭温度
        self.timing_type = int(data_inner_converted[20:24], 16)  # 校时方式
        self.time_interval = int(data_inner_converted[24:28], 16)  # 校时间隔
        self.fixed_ntp_server = self.get_addr_text(self.data_inner[28:36])  # 固定ntp服务器
        self.fixed_ntp_port = int(data_inner_converted[36:40], 16)  # 固定ntp端口
        self.dynamic_ntp_server = bytes.fromhex(self.data_inner[40:100].replace("00", "")).decode("gbk",
                                                                                                  errors="ignore")  # 动态ntp服务器
        self.dynamic_ntp_port = int(data_inner_converted[100:104], 16)  # 动态ntp端口
        self.dns_server = self.get_addr_text(self.data_inner[104:112])
        # self.ntp_server_ip_text = self.get_addr_text(self.data_inner[24:32])
        # self.ntp_port = int(data_inner_converted[32:36], 16)

    def set_data(self, hum_enable, hum_id, fan_open_temp, fan_close_temp, timing_type, time_interval,
                 fixed_ntp_server, fix_ntp_port, dynamic_ntp_server: str, dynamic_ntp_port, dns_server):
        length = "3800"
        hum_enable = self.convert(f"{hum_enable:04x}")
        hum_id = self.convert(f"{hum_id:04x}")
        fan_open_temp = self.convert(f"{fan_open_temp:04x}")
        fan_close_temp = self.convert(f"{fan_close_temp:04x}")
        timing_type = self.convert(f"{timing_type:04x}")
        time_interval = self.convert(f"{time_interval:04x}")
        fix_ntp_port = self.convert(f"{fix_ntp_port:04x}")
        dynamic_ntp_server = binascii.hexlify(dynamic_ntp_server.encode()).decode('utf-8').ljust(60, '0')
        fix_ntp_port = self.convert(f"{dynamic_ntp_port:04x}")
        fixed_ntp_server = self.convert_addr_to_hex(fixed_ntp_server)
        dns_server = self.convert_addr_to_hex(dns_server)
        data = f"{self.header}{self.device_id}{FunctionCode.SET_DEVICE_PARAM.value}{length}" \
               f"{hum_enable}{hum_id}{fan_open_temp}{fan_close_temp}{timing_type}{time_interval}{fixed_ntp_server}" \
               f"{fix_ntp_port}{dynamic_ntp_server}{dynamic_ntp_port}{dns_server}"


class VersionData(BasicFormat):
    # 版本信息
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_VERSION, data_raw)
        self.version_data = bytes.fromhex(self.data_inner).decode("gbk", errors="ignore")
        # logging.info(f"转换为:{self.version_data}")


class IsSuccessData(BasicFormat):
    IS_SUCCESS_CONVERT = ["失败", "成功"]

    def __init__(self, function_code, data_raw):
        BasicFormat.__init__(self, function_code, data_raw)
        data_inner_converted = self.convert(self.data_inner)
        self.is_success = data_inner_converted[:4]
        self.is_success_text = self.IS_SUCCESS_CONVERT[int(self.is_success)]


class DoorStateUpload(BasicFormat):
    # 开关门事件
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.DOOR_STATE, data_raw)
        self.function_code = FunctionCode.DOOR_STATE
        data_inner_converted = self.convert(self.data_inner)
        self.door_state = int(data_inner_converted[:4], 16)
        self.door_state_text = self.DOOR_STATE[int(data_inner_converted[:4], 16)]


class ConnectData:
    def __init__(self, text, function_code:ConnectStatusCode):
        self.function_code = function_code
        self.text = text
