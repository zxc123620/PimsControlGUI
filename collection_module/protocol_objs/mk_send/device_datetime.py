#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :device_datetime.py
# @Time      :2025/8/9 11:27
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class DeviceDateTimeData(BasicFormat):
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_TIME, data_raw)
        self.server_date = self.get_datetime_format(self.data_inner)
