#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :hum_and_temp_send.py
# @Time      :2025/11/17 14:50
# @Author    :zhouxiaochuan
# @Description: 
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class RainSend(BasicFormat):
    BYTE__DATA_NUM = 2

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.RAIN_DATA, data_raw)
        self.rain_id = int(self.data_inner[:self.BYTE__DATA_NUM], 16)  # 温湿度ID
        self.rain_type = int(self.data_inner[self.BYTE__DATA_NUM:self.BYTE__DATA_NUM*2], 16)  # 温湿度类型
        self.rain_state = self.data_inner[self.BYTE__DATA_NUM * 2:self.BYTE__DATA_NUM * 3]  # 执行状态
        self.result_code, self.result_text = self.state_convert(self.rain_state)  # 执行状态码,执行状态解析
        self.today_rain = self.instance_rain = self.yesterday_rain = self.total_rain = self.hour_rain = self.last_hour_rain = self.max_24_rain = self.min_24_rain = None
        if self.result_code == 1:
            data_inner_converted = self.convert(self.data_inner[self.BYTE__DATA_NUM * 3:])
            self.today_rain = int(data_inner_converted[:self.BYTE__DATA_NUM * 2], 16) / 10  # 当天
            self.instance_rain = int(data_inner_converted[self.BYTE__DATA_NUM * 2:self.BYTE__DATA_NUM * 4],
                                     16) / 10  # 瞬时
            self.yesterday_rain = int(data_inner_converted[self.BYTE__DATA_NUM * 4:self.BYTE__DATA_NUM * 6],
                                      16) / 10  # 昨日
            self.total_rain = int(data_inner_converted[self.BYTE__DATA_NUM * 6:self.BYTE__DATA_NUM * 8], 16) / 10  # 总雨量
            self.hour_rain = int(data_inner_converted[self.BYTE__DATA_NUM * 8:self.BYTE__DATA_NUM * 10],
                                 16) / 10  # 小时雨量
            self.last_hour_rain = int(data_inner_converted[self.BYTE__DATA_NUM * 10:self.BYTE__DATA_NUM * 12],
                                      16) / 10  # 上个小时降雨量
            self.max_24_rain = int(data_inner_converted[self.BYTE__DATA_NUM * 12:self.BYTE__DATA_NUM * 14],
                                   16) / 10  # 24小时最大雨量
            self.min_24_rain = int(data_inner_converted[self.BYTE__DATA_NUM * 16:self.BYTE__DATA_NUM * 18],
                                   16) / 10  # 24小时最小雨量

    def __repr__(self):
        return self.get_infos() + f"功能: 雨量数据, ID: {self.rain_id}, 类型: {self.rain_type}, 执行状态:{self.result_code} / {self.result_text}, " \
                                  f"当天雨量: {self.today_rain}, 瞬时雨量:{self.instance_rain}, 昨日雨量:{self.yesterday_rain}, " \
                                  f"总降雨量: {self.total_rain}, 小时雨量:{self.hour_rain}, 上小时雨量:{self.last_hour_rain}, " \
                                  f"24小时最大降雨量: {self.max_24_rain}, 24小时最小降雨量: {self.min_24_rain}"
