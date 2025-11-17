#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :pdu_control.py
# @Time      :2025/11/17 16:42
# @Author    :zhouxiaochuan
# @Description: 

from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class PduControl(BasicFormat):

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.PDU_CONTROL, data_raw)
        self.pdu_id = self.data_inner[0:2]
        self.pdu_type = int(self.data_inner[2:4], 16)
        self.pdu_no = int(self.data_inner[4:6], 16)
        self.pdu_control = self.COMMAND_STR[int(self.data_inner[6:8], 16)]

    def __str__(self):
        return self.get_infos() + f"功能: PDU控制, ID: {self.pdu_id}, 类型: {self.pdu_type}, PDU编号:{self.pdu_no}, 指令:{self.pdu_control}"

