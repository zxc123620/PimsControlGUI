#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :pdu_get.py
# @Time      :2025/11/17 15:58
# @Author    :zhouxiaochuan
# @Description: 

from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class PduGet(BasicFormat):

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.PDU_GET, data_raw)
        self.pdu_id = self.data_inner[0:2]
        self.pdu_type = int(self.data_inner[2:], 16)

    def __str__(self):
        return self.get_infos() + f"功能: PDU读取, ID: {self.pdu_id}, 类型: {self.pdu_type}"

