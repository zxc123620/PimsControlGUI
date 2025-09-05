#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :run.py
# @Time      :2025/6/24 18:56
# @Author    :zhouxiaochuan
# @Description:
import sys
sys.path.append(r"D:\csrd\xlza\pythonScript\FJMK")
import collection_module.pims_logger
from PyQt5.QtWidgets import QApplication

# from collection_module.ui.collection_module_ui import CollectionModuleUi
from collection_module.ui.fc_module_sub import FCModuleSubUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ui = CollectionModuleUi()
    ui = FCModuleSubUi()
    ui.show()
    sys.exit(app.exec_())
