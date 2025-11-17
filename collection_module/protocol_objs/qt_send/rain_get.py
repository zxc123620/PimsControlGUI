#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :rain_get.py
# @Time      :2025/11/17 15:24
# @Author    :zhouxiaochuan
# @Description: 
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class RainGet(BasicFormat):

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.RAIN_DATA, data_raw)
        self.rain_id = self.data_inner[0:2]
        self.rain_type = int(self.data_inner[2:], 16)

    def __str__(self):
        return self.get_infos() + f"功能: 温湿度读取, ID: {self.rain_id}, 类型: {self.rain_type}"

