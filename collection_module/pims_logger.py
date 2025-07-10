#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :pims_logger.py
# @Time      :2025/2/23 18:50
# @Author    :zhouxiaochuan
# @Description: 
import logging
import logging.config
import os

log_dir_name = "logs"
os.makedirs(log_dir_name, exist_ok=True)
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
        }
    },
    "filters": {
        "filter_other_module": {
            "name_to_filter": "webstompy.receiver.StompReceiver"  # 指定要过滤的名称
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
            "filters": ["filter_other_module"]
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": os.path.join(log_dir_name, "info.log"),
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": os.path.join(log_dir_name, "debug.log"),
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": os.path.join(log_dir_name, "errors.log"),
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "info_file_handler", "error_file_handler", "debug_file_handler"]
    }
}
logging.config.dictConfig(log_config)
