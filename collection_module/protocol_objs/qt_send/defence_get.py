#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 09:11
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class DefenceGet(BasicFormat):
    BYTES_NUM_LIST = [1, 2]

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_DOOR_STATE, data_raw)

    def __str__(self):
        return self.get_infos() + f"功能: 读取布撤防信息"
