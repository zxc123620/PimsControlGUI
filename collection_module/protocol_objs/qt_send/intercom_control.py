#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 09:11
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class IntercomControl(BasicFormat):
    BYTES_NUM_LIST = [1, 2]
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.INTERCOM_CONTROL, data_raw)
        self.command_control_str = self.COMMAND_STR[int(self.data_inner[0:self.BYTES_NUM_LIST[0]*2])]
        self.intercom_type_str = str(int(self.data_inner[self.BYTES_NUM_LIST[0]*2:self.BYTES_NUM_LIST[1]*2],16))


    def __str__(self):
        return self.get_infos() + f"功能: 450M列调控制, 指令: {self.command_control_str}"