#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :device_params.py
# @Time      :2025/8/9 8:40
# @Author    :zhouxiaochuan
# @Description:
import textwrap

from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class BaseObj:
    BYTE_NUM = 0

    def __init__(self, start_index: int):
        self.start_index = start_index
        self.end_index = start_index + self.BYTE_NUM * 2


class AlarmDeviceEnableObj(BaseObj):
    BYTE_NUM = 4

    def __init__(self, start_index, data=None):
        BaseObj.__init__(self, start_index)
        self.light_1_enable = None
        self.light_3_enable = None
        self.light_4_enable = None
        self.speaker_1_enable = None
        self.speaker_2_enable = None
        self.speaker_3_enable = None
        self.speaker_4_enable = None
        self.speaker_5_enable = None
        self.speaker_6_enable = None
        self.speaker_7_enable = None
        self.speaker_8_enable = None
        self.speaker_9_enable = None
        self.speaker_10_enable = None
        self.speaker_11_enable = None
        self.speaker_12_enable = None
        self.intercom_enable = None
        self.g_net_enable = None
        self.light_2_enable = None

        if data is not None:
            self.hex_to_obj(data)

    def hex_to_obj(self, data):
        """
        :param data: 数据区
        :return:
        """
        temp = data[self.start_index:self.start_index+ self.BYTE_NUM * 2].replace('00', '')
        temp_1 = ""
        for i in range(0, len(temp), 2):
            temp_1 = temp[i:i + 2] + temp_1
        device_enable_raw = int(temp_1, 16)
        device_enable = f"{device_enable_raw:018b}"
        self.g_net_enable, self.intercom_enable, self.speaker_12_enable, self.speaker_11_enable, \
        self.speaker_10_enable, self.speaker_9_enable, self.speaker_8_enable, self.speaker_7_enable, \
        self.speaker_6_enable, self.speaker_5_enable, self.speaker_4_enable, self.speaker_3_enable, \
        self.speaker_2_enable, self.speaker_1_enable, self.light_4_enable, self.light_3_enable, \
        self.light_2_enable, self.light_1_enable = device_enable


class SpeakeIDObj(BaseObj):
    BYTE_NUM = 13

    def __init__(self, start_index: int, data: str = None):
        BaseObj.__init__(self, start_index)
        self.speaker_voice_num = None
        self.speaker_12_id = None
        self.speaker_11_id = None
        self.speaker_10_id = None
        self.speaker_9_id = None
        self.speaker_8_id = None
        self.speaker_7_id = None
        self.speaker_6_id = None
        self.speaker_5_id = None
        self.speaker_4_id = None
        self.speaker_3_id = None
        self.speaker_2_id = None
        self.speaker_1_id = None
        if data is not None:
            self.hex_to_obj(data)

    def hex_to_obj(self, data):
        self.speaker_1_id, self.speaker_2_id, self.speaker_3_id, self.speaker_4_id, self.speaker_5_id, \
        self.speaker_6_id, self.speaker_7_id, self.speaker_8_id, self.speaker_9_id, self.speaker_10_id, \
        self.speaker_11_id, self.speaker_12_id, self.speaker_voice_num = \
            [data[i:i + 2] for i in range(0, len(data[self.start_index:self.end_index]), 2)]


class DeviceParamsObj(BasicFormat):
    INSPECTION_BYTE_NUM = 1
    TIME_TYPE_BYTE_NUM = 2
    TIME_INTERVAL_BYTE_NUM = 2

    DYNAMIC_BYTE_NUM = 30

    def __init__(self, data_raw=None):
        """
        :param data_raw: 数据区域
        """
        BasicFormat.__init__(self, FunctionCode.GET_DEVICE_DATA, data_raw)
        self.dns_server = None
        self.dynamic_ntp_port = None
        self.device_id = None  # 设备ID
        self.alarm_device_enable = None  # 设备使能
        self.speaker_id_obj = None  # 喇叭ID
        self.inspection_date = None  # 自检时间
        self.timing_type = None  # 校时方式
        self.time_interval = None  # 校时间隔
        self.fixed_ntp_server = None  # 固定ntp服务器
        self.fixed_ntp_port = None  # 固定ntp端口
        self.dynamic_ntp_server = None  # dns
        self.hex_to_obj(self.data_inner)

    def hex_to_obj(self, data: str):
        start_index = 0
        data_converted = self.convert(data)
        end_index = start_index + self.DEVICE_ID_BYTE_NUM * 2
        # 设备ID
        self.device_id = data_converted[start_index: end_index]
        # 设备使能
        self.alarm_device_enable = AlarmDeviceEnableObj(start_index=end_index+4, data=data)
        # 喇叭ID
        self.speaker_id_obj = SpeakeIDObj(start_index=self.alarm_device_enable.end_index, data=data)
        # 自检时间
        start_index = self.speaker_id_obj.end_index
        end_index = start_index + self.INSPECTION_BYTE_NUM * 2
        self.inspection_date = int(data[start_index:end_index], 16)
        # 校时方式
        start_index = end_index
        end_index = start_index + +self.TIME_TYPE_BYTE_NUM * 2
        self.timing_type = int(data[start_index:end_index])  # 校时方式
        # 校时周期
        start_index = end_index
        end_index = start_index + self.TIME_INTERVAL_BYTE_NUM * 2
        self.time_interval = int(data_converted[start_index:end_index], 16)
        # 固定ntp服务
        start_index = end_index
        end_index = start_index + self.IP_BYTE_NUM * 2
        self.fixed_ntp_server = self.get_addr_text(data[start_index:end_index])  # 固定ntp服务器
        # 固定ntp端口
        start_index = end_index
        end_index = start_index + self.PORT_BYTE_NUM * 2
        self.fixed_ntp_port = int(data_converted[start_index:end_index], 16)  # 固定ntp端口
        # 动态ntp服务
        start_index = end_index
        end_index = start_index + self.DYNAMIC_BYTE_NUM * 2
        self.dynamic_ntp_server = bytes.fromhex(data[start_index:end_index].replace("00", "")).decode("gbk",
                                                                                                      errors="ignore")  # 动态ntp服务器
        # 动态ntp端口
        start_index = end_index
        end_index = start_index + self.PORT_BYTE_NUM * 2
        self.dynamic_ntp_port = int(data_converted[start_index:end_index], 16)  # 动态ntp端口
        # DNS服务
        start_index = end_index
        end_index = start_index + self.IP_BYTE_NUM * 2
        self.dns_server = self.get_addr_text(data[start_index:end_index])