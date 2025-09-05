#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :connect_data.py
# @Time      :2025/8/9 11:53
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import ConnectStatusCode


class ConnectData:
    def __init__(self, text, function_code: ConnectStatusCode):
        self.function_code = function_code
        self.text = text
