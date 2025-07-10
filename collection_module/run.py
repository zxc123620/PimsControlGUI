#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :run.py
# @Time      :2025/6/24 18:56
# @Author    :zhouxiaochuan
# @Description:
import sys
import collection_module.pims_logger
from PyQt5.QtWidgets import QApplication

from collection_module.ui.collection_module_ui import CollectionModuleUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = CollectionModuleUi()
    ui.show()
    sys.exit(app.exec_())
