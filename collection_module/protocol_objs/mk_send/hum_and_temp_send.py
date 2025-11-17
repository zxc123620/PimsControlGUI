#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :hum_and_temp_send.py
# @Time      :2025/11/17 14:50
# @Author    :zhouxiaochuan
# @Description: 
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class HumAndTempSend(BasicFormat):
    BYTE__DATA_NUM = 2

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.HUM_AND_TEMP, data_raw)
        self.hum_id = int(self.data_inner[:self.BYTE__DATA_NUM], 16)  # 温湿度ID
        self.hum_type = int(self.data_inner[self.BYTE__DATA_NUM:self.BYTE__DATA_NUM * 2], 16)  # 温湿度类型
        self.hum_state = self.data_inner[self.BYTE__DATA_NUM * 2:self.BYTE__DATA_NUM * 3]  # 执行状态
        self.result_code, self.result_text = self.state_convert(self.hum_state)  # 执行状态码,执行状态解析
        self.temp, self.hum = None, None
        if self.result_code == 1:
            data_inner_converted = self.convert(self.data_inner[self.BYTE__DATA_NUM * 3:])
            self.temp = int(data_inner_converted[:self.BYTE__DATA_NUM * 2], 16) / 10
            self.hum = int(data_inner_converted[self.BYTE__DATA_NUM * 2:], 16) / 10

    def __repr__(self):
        return self.get_infos() + f"功能: 温湿度, ID: {self.hum_id}, 类型: {self.hum_type}, 执行状态:{self.result_code} / {self.result_text}, " \
                                  f"温度: {self.temp}, 湿度:{self.temp}"
