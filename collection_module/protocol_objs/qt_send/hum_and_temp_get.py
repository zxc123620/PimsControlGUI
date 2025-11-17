#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :hum_and_temp_get.py
# @Time      :2025/11/17 14:29
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class HumAndTempGet(BasicFormat):
    TYPE = [0, "温湿度"]

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.HUM_AND_TEMP, data_raw)
        self.hum_and_temp_id = self.data_inner[0:2]
        self.hum_and_temp_type = self.TYPE[int(self.data_inner[2:], 16)]

    def __str__(self):
        return self.get_infos() + f"功能: 温湿度读取, ID: {self.hum_and_temp_id}, 类型: {self.hum_and_temp_type}"
