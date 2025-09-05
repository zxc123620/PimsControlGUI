#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :version.py
# @Time      :2025/8/9 11:23
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class VersionData(BasicFormat):
    # 版本信息
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_VERSION, data_raw)
        self.version_data = bytes.fromhex(self.data_inner).decode("gbk", errors="ignore")
        # logging.info(f"转换为:{self.version_data}")
