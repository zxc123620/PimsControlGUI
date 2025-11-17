#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :pdu_control_result.py
# @Time      :2025/11/17 16:50
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class PDUControlResult(BasicFormat):
    BYTE__DATA_NUM = 2

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.PDU_CONTROL, data_raw)
        self.pdu_id = int(self.data_inner[:self.BYTE__DATA_NUM], 16)  # 温湿度ID
        self.pdu_type = int(self.data_inner[self.BYTE__DATA_NUM:self.BYTE__DATA_NUM * 2], 16)  # 温湿度类型
        self.pdu_state = self.data_inner[self.BYTE__DATA_NUM * 2:self.BYTE__DATA_NUM * 3]  # 执行状态
        self.result_code, self.result_text = self.state_convert(self.pdu_state)  # 执行状态码,执行状态解析

    def __repr__(self):
        return self.get_infos() + f"功能: PDU控制反馈, ID: {self.pdu_id}, 类型: {self.pdu_type}, 执行状态:{self.result_code} / {self.result_text}"
