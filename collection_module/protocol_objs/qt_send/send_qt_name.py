#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 09:11
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class SetQTName(BasicFormat):
    QT_TYPE = ["0", "主", "从"]

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.RENAME, data_raw)
        self.qt_type = self.QT_TYPE[int(self.data_inner[:2])]
        # print(self.data_inner[2:])
        self.qt_name = bytes.fromhex(self.data_inner[2:]).decode("utf-8", "ignore")

    def __str__(self):
        return self.get_infos() + f"功能: 重命名, 类型: {self.qt_type}, 名字: {self.qt_name} "
