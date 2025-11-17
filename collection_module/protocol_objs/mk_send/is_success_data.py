#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :is_success_data.py
# @Time      :2025/8/9 11:48
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat
from collection_module.result_status_code import ResultStatusCode


class IsSuccessData(BasicFormat):
    IS_SUCCESS_CONVERT = ["失败", "成功"]
    RESULT_BYTE_NUM = 2

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.COMMAND_RESULT, data_raw)
        data_inner_converted = self.convert(self.data_inner)
        data = data_inner_converted[:self.RESULT_BYTE_NUM * 2]
        self.result_code, self.result_text = self.state_convert(data)  # 执行状态码,执行状态解析

    def __str__(self):
        return self.get_infos() + f"功能: 控制反馈, 结果码: {self.result_code}, 解析: {self.result_text} "
