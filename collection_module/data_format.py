#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :data_fromat_emum.py
# @Time      :2025/6/20 16:54
# @Author    :zhouxiaochuan
# @Description:
import logging
import collection_module.pims_logger
from scapy.layers.inet import TCP, IP

from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.mk_send.defence import DefenceStateData
from collection_module.protocol_objs.mk_send.get_rtc_time import GetRTCTIme
from collection_module.protocol_objs.mk_send.heartbeat_param import HeartBeatData
from collection_module.protocol_objs.mk_send.hum_and_temp_send import HumAndTempSend
from collection_module.protocol_objs.mk_send.is_success_data import IsSuccessData
from collection_module.protocol_objs.mk_send.pdu_control_result import PDUControlResult
from collection_module.protocol_objs.mk_send.pdu_send import PDUSend
from collection_module.protocol_objs.mk_send.rain_send import RainSend
from collection_module.protocol_objs.qt_send.defence_control import DefenceControlCMD
from collection_module.protocol_objs.qt_send.defence_get import DefenceGet
from collection_module.protocol_objs.qt_send.heartbeat import HeartBeatSend
from collection_module.protocol_objs.qt_send.hum_and_temp_get import HumAndTempGet
from collection_module.protocol_objs.qt_send.intercom_control import IntercomControl
from collection_module.protocol_objs.qt_send.light_control import LightControl
from collection_module.protocol_objs.qt_send.pdu_control import PduControl
from collection_module.protocol_objs.qt_send.pdu_get import PduGet
from collection_module.protocol_objs.qt_send.rain_get import RainGet
from collection_module.protocol_objs.qt_send.send_qt_name import SetQTName
from collection_module.protocol_objs.qt_send.send_rtc_data import SendRtcTime
from collection_module.protocol_objs.qt_send.speaker_control import SpeakerControl

from scapy.all import *


def sticky_check(data):
    """粘包检查"""
    import re
    if len(re.findall("6869", str(data))) > 2 or len(re.findall("6162", str(data))) > 2:
        return "远控单元发送的数据存在粘包"
    if len(re.findall("e3e4", str(data))) > 2 or len(re.findall("e1e2", str(data))) > 2:
        return "QT发送的数据存在粘包"
    return ""


port_save = {}


def packet_callback(data_packet):
    src_ip = data_packet[IP].src
    dst_ip = data_packet[IP].dst
    key = src_ip + dst_ip
    if key not in port_save.keys():
        port_save[key] = []
    if data_packet.haslayer(TCP):
        src_port = data_packet[TCP].sport
        dst_port = data_packet[TCP].dport
        if [src_port, dst_port] != port_save[key]:
            logging.info(f"端口发生改变, 从 {port_save[key][0]} -> {port_save[key][1]} 变为 {src_port} -> {dst_port}") if \
            port_save[key] != [] else None
            port_save[key] = [src_port, dst_port]
        if isinstance(data_packet[TCP].payload, NoPayload):
            return
        data = data_packet[TCP].payload.load.hex()
        sticky = sticky_check(data)
        if sticky:
            basic_data = \
                f"""\n
                --------------------------------------------------
                {src_ip}:{src_port}----------->{dst_ip}:{dst_port} {data} {sticky}
                """
            logging.info(basic_data)
            return
        try:
            function_code = data[8:12]
            header = data[:4]
            format_obj = ""
            if header == "6869":
                if function_code == FunctionCode.GET_TIME.value:
                    format_obj = GetRTCTIme(data)
                elif function_code == FunctionCode.DEFENCE_STATE.value:
                    format_obj = DefenceStateData(data)
                elif function_code == FunctionCode.HEARTBEAT.value and args.heartbeat:
                    format_obj = HeartBeatData(data)
                elif function_code in [FunctionCode.CONTROL_LIGHT.value, FunctionCode.CONTROL_LIGHT.value,
                                       FunctionCode.SPEAKER_CONTROL.value, FunctionCode.INTERCOM_CONTROL.value,
                                       FunctionCode.DEFENCE_CONTROL.value,
                                       FunctionCode.RENAME.value, FunctionCode.SET_TIME.value]:
                    format_obj = IsSuccessData(data)
            elif header == "e3e4":
                if function_code == FunctionCode.HEARTBEAT.value and args.heartbeat:
                    format_obj = HeartBeatSend(data)
                elif function_code == FunctionCode.CONTROL_LIGHT.value:
                    format_obj = LightControl(data)
                elif function_code == FunctionCode.SPEAKER_CONTROL.value:
                    format_obj = SpeakerControl(data)
                elif function_code == FunctionCode.INTERCOM_CONTROL.value:
                    format_obj = IntercomControl(data)
                elif function_code == FunctionCode.DEFENCE_CONTROL.value:
                    format_obj = DefenceControlCMD(data)
                elif function_code == FunctionCode.GET_DOOR_STATE.value:
                    format_obj = DefenceGet(data)
                elif function_code == FunctionCode.RENAME.value:
                    format_obj = SetQTName(data)
                elif function_code == FunctionCode.SET_TIME.value:
                    format_obj = SendRtcTime(data)
            elif header == "e1e2":
                # qt -> fc
                if function_code == FunctionCode.HUM_AND_TEMP.value:
                    format_obj = HumAndTempGet(data)
                elif function_code == FunctionCode.RAIN_DATA.value:
                    format_obj = RainGet(data)
                elif function_code == FunctionCode.PDU_GET.value:
                    format_obj = PduGet(data)
                elif function_code == FunctionCode.PDU_CONTROL.value:
                    format_obj = PduControl(data)
            elif header == "6162":
                # fc -> qt
                if function_code == FunctionCode.HUM_AND_TEMP.value:
                    format_obj = HumAndTempSend(data)
                elif function_code == FunctionCode.RAIN_DATA.value:
                    format_obj = RainSend(data)
                elif function_code == FunctionCode.PDU_GET.value:
                    format_obj = PDUSend(data)
                elif function_code == FunctionCode.PDU_CONTROL.value:
                    format_obj = PDUControlResult(data)
            if format_obj:
                basic_data = \
                    f"""\n
                    --------------------------------------------------
                    {src_ip}:{src_port}----------->{dst_ip}:{dst_port}
                    --------------------------------------------------
                    {data}
                    --------------------------------------------------
                    {format_obj} : {sticky}
                    """
            else:
                basic_data = f"{src_ip}:{src_port}-->{dst_ip}:{dst_port}: {data} {sticky}"
            logging.info(basic_data)
        except Exception as e:
            logging.exception(e)
            logging.info("数据解析失败")


parser = argparse.ArgumentParser(description="Python 命令行抓包工具")
parser.add_argument("-i", "--iface", help="网卡名", default="以太网")
parser.add_argument("-f", "--filter", help="BPF 过滤", default="tcp port 5001")
parser.add_argument("-heartbeat", "--heartbeat", type=int, help="心跳解析", default=0)
args = parser.parse_args()
sniff(iface=args.iface, filter=args.filter, prn=packet_callback)
# sniff(iface="本地连接", filter="tcp port 5001", prn=packet_callback)
