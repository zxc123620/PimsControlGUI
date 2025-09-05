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
        result_int = int(data, 16)
        result_bin = eval(bin(int(data, 16)))
        self.result_text = ""
        if result_bin & (1 << 7):
            self.result_code = result_bin - (1 << 8)
        else:
            self.result_code = result_int
        self.result_text += "结果码: " + str(self.result_code)
        result_code_list = [code.value for code in ResultStatusCode]
        if self.result_code in result_code_list:
            self.result_code_text = ResultStatusCode(self.result_code).name
            self.result_text += " 解析: " + self.result_code_text
