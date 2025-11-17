#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :hum_and_temp_send.py
# @Time      :2025/11/17 14:50
# @Author    :zhouxiaochuan
# @Description: 
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class PDUSend(BasicFormat):
    BYTE__DATA_NUM = 2
    RELAY_TEXT = ["关闭", "开启"]
    ALARM_TEXT = ["过压告警", "欠压告警", "过流告警", "过功率告警"]

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.HUM_AND_TEMP, data_raw)
        self.pdu_id = int(self.data_inner[:self.BYTE__DATA_NUM], 16)  # ID
        self.pdu_type = int(self.data_inner[self.BYTE__DATA_NUM:self.BYTE__DATA_NUM * 2], 16)  # 类型
        self.pdu_state = self.data_inner[self.BYTE__DATA_NUM * 2:self.BYTE__DATA_NUM * 3]  # 执行状态
        self.result_code, self.result_text = self.state_convert(self.pdu_state)  # 执行状态码,执行状态解析
        self.relay_state_text = None
        self.alarm_state_text = None
        if self.result_code == 1:
            data_inner_converted = self.convert(self.data_inner[self.BYTE__DATA_NUM * 3:])  # 3跳到4,因为有个字节是自动补位
            # print(data_inner_converted)
            relay_state = f"{int(data_inner_converted[:self.BYTE__DATA_NUM * 2], 16):08b}"[::-1]
            self.relay_state_text = [self.RELAY_TEXT[int(i)] for i in relay_state]
            alarm_state = f"{int(data_inner_converted[self.BYTE__DATA_NUM * 2:self.BYTE__DATA_NUM * 4], 16):04b}"[
                          ::-1]
            self.alarm_state_text = [self.ALARM_TEXT[index] for index, data in enumerate(alarm_state) if data == 1]

    def __repr__(self):
        return self.get_infos() + f"功能: 温湿度, ID: {self.pdu_id}, 类型: {self.pdu_type}, 执行状态:{self.result_code} / {self.result_text}, " \
                                  f"继电器1-8状态(/0关闭/1开启): {self.relay_state_text}, 告警状态:{self.alarm_state_text}"
