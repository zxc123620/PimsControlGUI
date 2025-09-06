#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 09:11
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class LightControl(BasicFormat):
    LIGHT_NO_BYTES = 1
    CONTROL_COMMAND_BYTES = 1

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.CONTROL_LIGHT, data_raw)
        start_index = 0
        end_index = start_index + self.CONTROL_CODE_BYTE_NUM * 2
        self.control_command = self.data_inner[start_index:end_index]
        self.light_no, self.control_command = int(self.control_command[:2]), int(self.control_command[2:])
        self.control_command_str = self.COMMAND_STR[self.control_command]



    def __str__(self):
        return self.get_infos() + f"功能: 信号灯控制, 编号:{self.light_no}, 指令: {self.control_command_str}"