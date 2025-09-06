#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :result_status_code.py
# @Time      :2025/7/30 19:17
# @Author    :zhouxiaochuan
# @Description:
from enum import Enum


class ResultStatusCode(Enum):
    DEV_OK = 1
    DEV_ENABLE = 2
    DEV_DISABLE = 3
    OtherQtclient_Open_DEV = 4
    QTCLIENT_MASTER = 5
    QTCLIENT_SLAVE = 6
    RM8000_NoCarrier = 7
    RM8000_Busy = 8
    RM8000_NoAnswer = 9
    RM8000_On_Pho = 10
    RM8000_Off_pho = 11
    OtherQtclient_Open_Led = 12
    MODBUS_ERR_NOT_MASTER = -1
    MODBUS_ERR_POLLING = -2
    MODBUS_ERR_BUFF_OVERFLOW = -3
    MODBUS_ERR_BAD_CRC = -4
    MODBUS_ERR_EXCEPTION = -5
    MODBUS_ERR_BAD_SIZE = -6
    MODBUS_ERR_BAD_ADDRESS = -7
    MODBUS_ERR_TIME_OUT = -8
    MODBUS_ERR_BAD_SLAVE_ID = -9
    MODBUS_ERR_BAD_TCP_ID = -10
    MODBUS_ERR_OK_QUERY = -11
    RM8000_PHO_Err = -12
    RM8000_Error = -13
    YX9100_INIT = -14
    YX9100_NOT_RECV_CPL = -15
    YX9100_CRC_ERR = -16
    YX9100_FOLDER_OVER_RANGE = -17
    YX9100_FOLDER_NOT_FIND = -18
    YX9100_DATA_ERR = -19
    DEV_NO_RESPONSE = -20
    Alarm_Music_Err = -21
    DEV_TEST_Err = -22
    Alarmled_Num_err = -23
    Alarmled_ACSAMP_err = -24

