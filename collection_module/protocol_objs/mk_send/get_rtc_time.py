#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 10:41
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class GetRTCTIme(BasicFormat):
    BYTES_NUM_LIST = [1, 2]

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_TIME, data_raw)

    def __str__(self):
        return self.get_infos() + f"功能: 获取RTC时间"
