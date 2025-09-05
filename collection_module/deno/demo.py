#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :demo.py
# @Time      :2025/9/5 14:58
# @Author    :zhouxiaochuan
# @Description:
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw, NoPayload
from scapy.sendrecv import sniff

#
# def get_data(x):
#     # print("类型:", type(x))
#     # print("摘要:", x.summary())
#     # print("has tcp:", x.haslayer(TCP))
#     # print("has IP:", x.haslayer(IP))
#     # if x.haslayer(IP):
#     #     print("源IP:", x[IP].src)
#
#     src_ip = x[IP].src
#     dst_ip = x[IP].dst
#     if x.haslayer(TCP):
#         src_port = x[TCP].sport
#         dst_port = x[TCP].dport
#         print(type(x[TCP].payload))
#         if isinstance(x[TCP].payload, NoPayload):
#             return
#         print(x[TCP].payload.load.hex())
#

if __name__ == "__main__":
    sniff(iface="以太网", filter="tcp port 5001", prn=get_data)
