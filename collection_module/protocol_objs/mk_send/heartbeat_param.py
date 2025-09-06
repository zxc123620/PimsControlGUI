#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :heartbeat_param.py
# @Time      :2025/8/9 11:46
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class HeartBeatData(BasicFormat):
    VERSION_BYTE_NUM = 4

    def __init__(self, data_raw):
        " 19 00 06 00 18 00 11 00 30 00 2B  00 20 25 06 23 "
        BasicFormat.__init__(self, FunctionCode.HEARTBEAT, data_raw)
        # self.year = int(data_inner_converted[0:4], 16)
        # self.month = int(data_inner_converted[4:8], 16)
        # self.day = int(data_inner_converted[8:12], 16)
        # self.hour = int(data_inner_converted[12:16], 16)
        # self.minute = int(data_inner_converted[16:20], 16)
        # self.seconds = int(data_inner_converted[20:24], 16)
        # self.fc_version = self.data_inner[24:32]
        # self.device_date_text = self.get_date_text(data_inner_converted[0:24])
        # 软件版本
        start_index = 0
        end_index = start_index + self.VERSION_BYTE_NUM * 2
        self.mk_soft_version = self.data_inner[start_index:end_index]
        # 硬件版本
        start_index = end_index
        end_index = start_index + self.VERSION_BYTE_NUM * 2
        self.mk_hark_version = self.data_inner[start_index:end_index]

    def __repr__(self):
        return self.get_infos() + f"功能: 心跳, 硬件版本:{self.mk_hark_version}, 软件版本: {self.mk_soft_version}"
