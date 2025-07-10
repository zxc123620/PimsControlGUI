#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :function_code.py
# @Time      :2025/6/20 17:01
# @Author    :zhouxiaochuan
# @Description:
from enum import Enum


class FunctionCode(Enum):
    HEARTBEAT = "ff00"
    GET_HUM_TMP = "0101"
    GET_NET_DATA = "0102"  # 获取网络
    GET_DEVICE_DATA = "0302"  # 设备参数
    GET_VERSION = "0201"  # 版本
    CONTROL_FAN = "0103"  # 风扇控制
    DOOR_STATE = "0105"  # 开关门状态
    SET_DEVICE_PARAM = "0402"  # 设备参数配置
    SET_NET_PARAM = "0202"  # 修改网络参数
    SET_RTC_TIME = "0205"  # rtc校时


class ConnectStatusCode(Enum):
    CONNECTED = 1
    BREAK = 0


class FanControl(Enum):
    OPEN = "0100"
    CLOSE = "0000"


class Enable(Enum):
    ENABLE = 1
    DISABLE = 0


class TimingType(Enum):
    MANUAL = 0
    NTP = 1
    DYNAMIC = 2

print(isinstance(ConnectStatusCode.CONNECTED, ConnectStatusCode))