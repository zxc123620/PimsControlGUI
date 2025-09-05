#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :function_code.py
# @Time      :2025/6/20 17:01
# @Author    :zhouxiaochuan
# @Description:
from enum import Enum


class FunctionCode(Enum):
    HEARTBEAT = "ff00"
    GET_VERSION = "0101"
    GET_NET_DATA = "0102"  # 获取网络
    GET_DEVICE_DATA = "0302"  # 设备参数
    GET_DOOR_STATE = "0201"  # 读取布撤防、开关门信息
    CONTROL_FAN = "0103"  # 风扇控制
    DOOR_STATE = "0105"  # 开关门状态
    SET_DEVICE_PARAM = "0402"  # 设备参数配置
    SET_NET_PARAM = "0202"  # 修改网络参数
    SET_RTC_TIME = "0205"  # rtc校时
    SPEAKER_CONTROL = "0203"  # 喇叭控制
    RENAME = "0802"  # 重命名
    COMMAND_RESULT = "_"
    CONTROL_LIGHT = "0103"  # 信号灯控制
    DEFENCE_CONTROL = "0503"  # 布撤防控制
    DEFENCE_STATE = "0105"  # 布撤防发送
    INTERCOM_CONTROL = "0303"  # 列调控制
    GET_TIME = "0502"  # 获取时间
    SET_TIME = "0602"  # 设置时间
    DEVICE_REBOOT = "2003"  # 重启


class ConnectStatusCode(Enum):
    CONNECTED = 1
    BREAK = 0


class FanControl(Enum):
    OPEN = "0100"
    CLOSE = "0000"


class ClientType(Enum):
    MAIN = "01"
    SUB = "02"


class Enable(Enum):
    ENABLE = 1
    DISABLE = 0


class TimingType(Enum):
    MANUAL = 0
    NTP = 1
    DYNAMIC = 2


class SpeakerType(Enum):
    ALARM = "01"
    EVICTION = "02"


class IntercomType(Enum):
    INTERCOM = "01"
    G_NET = "10"


class ControlType(Enum):
    OPEN = "01"
    CLOSE = "00"


class DefenceControl(Enum):
    DEF = "0000"
    UN_DEF = "0100"


class LightNo(Enum):
    ONE = "01"
    TWO = "02"


class SpeakerPlayType(Enum):
    """
    单曲/循环
    """
    LOOP = "02"
    SIGNAL = "01"


class GNetSendType(Enum):
    """
    G网呼叫类型
    """
    SIGNAL = "01"
    GROUP = "02"


print(isinstance(ConnectStatusCode.CONNECTED, ConnectStatusCode))
