#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :data_fromat_emum.py
# @Time      :2025/6/20 16:54
# @Author    :zhouxiaochuan
# @Description:
import binascii
import datetime
import logging
from configparser import ConfigParser

from scapy.layers.inet import TCP, IP
from scapy.packet import Raw, NoPayload
from scapy.sendrecv import sniff

from collection_module.function_code import FunctionCode


def sticky_check(data):
    """粘包检查"""
    import re
    if len(re.findall("6869", str(data))) > 2:
        return "远控单元发送的数据存在粘包"
    if len(re.findall("e3e4", str(data))) > 2:
        return "QT发送的数据存在粘包"
    return None


def packet_callback(data_packet):
    src_ip = data_packet[IP].src
    dst_ip = data_packet[IP].dst
    if data_packet.haslayer(TCP):
        src_port = data_packet[TCP].sport
        dst_port = data_packet[TCP].dport
        if isinstance(data_packet[TCP].payload, NoPayload):
            return
        data = data_packet[TCP].payload.load.hex()
        function_code = data[8:12]
        if function_code == FunctionCode.CONTROL_LIGHT.value:
            pass
        else:
            pass




class DataFormatThread(Thread):
    def run(self) -> None:
        config = ConfigParser()
        config.read("config.ini", encoding='utf-8')
        interface = config.get("config", "interface")
        interface_filter = config.get("config", "filter")
        print(f"interface:{interface}, filter:{interface_filter}")
        sniff(prn=packet_callback, iface=interface, store=0, filter=interface_filter)
        while True:
            pass
