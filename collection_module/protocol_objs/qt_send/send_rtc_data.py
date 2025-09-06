#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 09:12
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class SendRtcTime(BasicFormat):
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.SET_TIME, data_raw)
        self.date_time = self.get_datetime_format(self.data_inner)

    def __str__(self):
        return self.get_infos() + f"功能: 设置RTC时间, 时间: {self.date_time.strftime('%Y-%m-%d %H:%M:%S')} "
