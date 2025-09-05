#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :defence.py
# @Time      :2025/8/9 11:24
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class DefenceStateData(BasicFormat):
    BYTE_NUM = 1

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.DEFENCE_STATE, data_raw)
        # data_inner_converted = self.convert(self.data_inner)
        self.def_state = int(self.data_inner[:self.BYTE_NUM*2], 16)
        self.def_state_text = self.DEFENCE_STATE[int(self.def_state)]
