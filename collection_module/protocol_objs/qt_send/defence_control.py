#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 09:11
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class DefenceControl(BasicFormat):
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.DEFENCE_CONTROL, data_raw)
        start_index = 0
        end_index = start_index + self.CONTROL_CODE_BYTE_NUM *2
        self.control_command = self.data_inner[start_index:end_index]
        self.control_command_str = self.DEFENCE_STATE[int(self.control_command)]


    def __str__(self):
        return self.get_infos() + f"功能: 布撤防控制, 指令: {self.control_command_str}, 类型: {self.control_command_str}"