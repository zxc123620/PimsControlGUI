#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :device_net_param.py
# @Time      :2025/8/9 11:27
# @Author    :zhouxiaochuan
# @Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class DeviceNetData(BasicFormat):
    """
    网络参数
    """
    HEARTBEAT_INTERVAL_BYTE_MUL = 2

    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.GET_NET_DATA, data_raw)
        # IP地址
        start_index = 0
        end_index = start_index + self.IP_BYTE_NUM * 2
        data_inner_converted = self.convert(self.data_inner)
        self.ip_addr_text = self.get_addr_text(self.data_inner[start_index:end_index])
        # 端口
        start_index = end_index
        end_index = start_index + self.PORT_BYTE_NUM * 2
        self.ip_port = int(data_inner_converted[start_index:end_index], 16)
        # 网关
        start_index = end_index
        end_index = start_index + self.IP_BYTE_NUM * 2
        self.gateway_text = self.get_addr_text(self.data_inner[start_index:end_index])
        # 子网掩码
        start_index = end_index
        end_index = start_index + self.IP_BYTE_NUM * 2
        self.mask_text = self.get_addr_text(self.data_inner[start_index:end_index])
        # mac地址
        start_index = end_index
        end_index = start_index + self.MAC_ADDRESS_BYTE_NUM * 2
        mac_raw = self.data_inner[start_index: end_index]
        self.mac = ":".join([mac_raw[i:i + 2] for i in range(0, len(mac_raw), 2)])
        # dns1
        start_index = end_index
        end_index = start_index + self.IP_BYTE_NUM * 2
        self.dns_1_text = self.get_addr_text(self.data_inner[start_index:end_index])
        # dns2
        start_index = end_index
        end_index = start_index + self.IP_BYTE_NUM * 2
        self.dns_2_text = self.get_addr_text(self.data_inner[start_index:end_index])
        # 心跳间隔
        start_index = end_index
        end_index = start_index + self.HEARTBEAT_INTERVAL_BYTE_MUL * 2
        self.heartbeat_interval = int(data_inner_converted[start_index:end_index], 16)
