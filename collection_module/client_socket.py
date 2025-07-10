#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_socket.py
# @Time      :2025/6/20 14:22
# @Author    :zhouxiaochuan
# @Description:
import binascii
import datetime
import logging
import socket
import time
from enum import Enum
from queue import Queue
from threading import Thread, Event

from PyQt5.QtCore import QThread, pyqtSignal

import collection_module.pims_logger
from collection_module.tool import crc_16_modbus
from collection_module.data_format import HumAndTempData, NetData, DeviceData, VersionData, \
    IsSuccessData, HeartBeatData, DoorStateUpload, BasicFormat, ConnectData
from collection_module.function_code import FunctionCode, FanControl, Enable, TimingType, ConnectStatusCode


class MKClientSocketThread(QThread):
    signal = pyqtSignal(object)
    HEADER = "E3E4"

    def __init__(self, device_id="aa00"):
        QThread.__init__(self)
        self.socket = None
        self.server_port = None
        self.server_ip = None
        self.send_queue = Queue()
        self.recv_queue = Queue()
        self.__inner_event = Event()
        # self.header = "e3e4"
        self.device_id = device_id
        self.flag = True
        self.heartbeat_flag = True
        self.send_flag = True
        self.heartbeat_close_event = Event()
        self.send_close_event = Event()
        self.outer_event = Event()
        self.send_msg_thread = Thread(target=self.send_data_event, daemon=True, name="ClientSocketSendThread")
        self.heartbeat_thread = Thread(target=self.send_heartbeat_event, daemon=True, name="SendHeartBeatThread")
        self.send_msg_thread.start()
        self.heartbeat_thread.start()

    def __get_header(self):
        return f"{self.HEADER}{self.device_id}"

    def send_heartbeat_event(self):
        """
        心跳发送线程
        :return:
        """
        while self.heartbeat_flag:
            self.__inner_event.wait()
            time.sleep(10)
            date_length = "0000"
            data = f"{self.__get_header()}{FunctionCode.HEARTBEAT.value}{date_length}"
            self.send_queue.put(data + crc_16_modbus(data))
        self.heartbeat_close_event.set()
        logging.info("心跳线程关闭")

    def set_net_param_data(self, ip_addr, port, gateway, mask, mac, main_dns, back_up_dns, heartbeat_interval):
        """
        设置网络参数
        :param heartbeat_interval:
        :param ip_addr:
        :param port:
        :param gateway:
        :param mask:
        :param mac:
        :param main_dns:
        :param back_up_dns:
        :return:
        """
        if not (ip_addr and port and gateway and mask and mac and main_dns and back_up_dns and heartbeat_interval):
            return
        length = "1e00"
        ip_addr = BasicFormat.convert_addr_to_hex(ip_addr)
        gateway = BasicFormat.convert_addr_to_hex(gateway)
        mask = BasicFormat.convert_addr_to_hex(mask)
        main_dns = BasicFormat.convert_addr_to_hex(main_dns)
        back_up_dns = BasicFormat.convert_addr_to_hex(back_up_dns)
        port = BasicFormat.convert(f"{int(port):04x}")
        mac = str(mac).replace(":", "")
        heartbeat_interval = BasicFormat.convert(f"{int(heartbeat_interval):04x}")
        data = f"{self.__get_header()}{FunctionCode.SET_NET_PARAM.value}{length}" \
               f"{ip_addr}{port}{gateway}{mask}{mac}{main_dns}{back_up_dns}" \
               f"{heartbeat_interval}"
        self.send_queue.put(data + crc_16_modbus(data))

    def send_param_data(self, hum_enable: Enable, hum_id, fan_open_temp, fan_close_temp, timing_type: TimingType,
                        time_interval,
                        fixed_ntp_server, fix_ntp_port, dynamic_ntp_server: str, dynamic_ntp_port, dns_server,
                        device_id):
        """
        发送设备参数
        :param device_id:
        :param hum_enable:
        :param hum_id:
        :param fan_open_temp:
        :param fan_close_temp:
        :param timing_type:
        :param time_interval:
        :param fixed_ntp_server:
        :param fix_ntp_port:
        :param dynamic_ntp_server:
        :param dynamic_ntp_port:
        :param dns_server:
        :return:
        """
        if not (
                hum_enable and hum_id and fan_open_temp and fan_close_temp and timing_type and time_interval and fixed_ntp_server and fix_ntp_port and dynamic_ntp_server and dynamic_ntp_port and device_id):
            return
        length = "3800"
        hum_enable = BasicFormat.convert(f"{hum_enable.value:04x}")
        hum_id = BasicFormat.convert(f"{int(hum_id):04x}")
        fan_open_temp = BasicFormat.convert(f"{int(fan_open_temp):04x}")
        fan_close_temp = BasicFormat.convert(f"{int(fan_close_temp):04x}")
        timing_type = BasicFormat.convert(f"{timing_type.value:04x}")
        time_interval = BasicFormat.convert(f"{int(time_interval):04x}")
        fixed_ntp_server = BasicFormat.convert_addr_to_hex(fixed_ntp_server)
        fix_ntp_port = BasicFormat.convert(f"{int(fix_ntp_port):04x}")
        dynamic_ntp_server = binascii.hexlify(dynamic_ntp_server.encode()).decode('utf-8').ljust(60, '0')
        dynamic_ntp_port = BasicFormat.convert(f"{int(dynamic_ntp_port):04x}")
        dns_server = BasicFormat.convert_addr_to_hex(dns_server)
        data = f"{self.__get_header()}{FunctionCode.SET_DEVICE_PARAM.value}{length}" \
               f"{device_id}{hum_enable}{hum_id}{fan_open_temp}{fan_close_temp}{timing_type}{time_interval}{fixed_ntp_server}" \
               f"{fix_ntp_port}{dynamic_ntp_server}{dynamic_ntp_port}{dns_server}"
        self.send_queue.put(data + crc_16_modbus(data))

    def get_hum_and_temp_data(self):
        """
        获取温湿度数据
        :return:
        """
        data_length = "0000"
        data = f"{self.__get_header()}{FunctionCode.GET_HUM_TMP.value}{data_length}"
        self.send_queue.put(data + crc_16_modbus(data))

    def get_net_data(self):
        """
        获取温湿度数据
        :return:
        """
        data_length = "0000"
        data = f"{self.__get_header()}{FunctionCode.GET_NET_DATA.value}{data_length}"
        self.send_queue.put(data + crc_16_modbus(data))

    def get_device_param_data(self):
        """
        获取设备参数
        :return:
        """
        data_length = "0000"
        data = f"{self.__get_header()}{FunctionCode.GET_DEVICE_DATA.value}{data_length}"
        self.send_queue.put(data + crc_16_modbus(data))

    def fan_control(self, control: FanControl):
        """
        开启风扇
        :return:
        """
        data_length = "0200"
        data = f"{self.__get_header()}{FunctionCode.CONTROL_FAN.value}{data_length}{control.value}"
        self.send_queue.put(data + crc_16_modbus(data))

    def get_version(self):
        """
        获取版本
        :return:
        """
        data_length = "0000"
        data = f"{self.__get_header()}{FunctionCode.GET_VERSION.value}{data_length}"
        self.send_queue.put(data + crc_16_modbus(data))

    def judge_rtc_time(self, data):
        """
        判断是否是读取rtc时间
        :param data:
        :return:
        """
        data_length = data[12:16]
        if data_length == "0000":
            self.send_rtc_time()

    def send_rtc_time(self):
        """
        发送校时
        :return:
        """
        data_length = "0c00"
        temp_date = datetime.datetime.now()
        year = BasicFormat.convert(f"{temp_date.year:04x}")
        month = BasicFormat.convert(f"{temp_date.month:04x}")
        day = BasicFormat.convert(f"{temp_date.day:04x}")
        hour = BasicFormat.convert(f"{temp_date.hour:04x}")
        minute = BasicFormat.convert(f"{temp_date.minute:04x}")
        seconds = BasicFormat.convert(f"{temp_date.second:04x}")
        data = f"{self.__get_header()}{FunctionCode.SET_RTC_TIME.value}{data_length}{year}{month}{day}{hour}" \
               f"{minute}{seconds}"
        self.send_queue.put(data + crc_16_modbus(data))

    def send_data_event(self):
        """
        发送数据线程
        :return:
        """
        while self.send_flag:
            self.__inner_event.wait()
            if self.socket is None:
                self.__inner_event.clear()
                continue
            data = self.send_queue.get()
            logging.info(f"发送数据:{data}")
            try:
                self.socket.sendall(bytes.fromhex(str(data)))
            except socket.error as e:
                self.__inner_event.clear()
                # 发送状态
                self.signal.emit(ConnectData("已断开", ConnectStatusCode.BREAK))
        self.send_close_event.set()
        logging.info("发送线程关闭")

    def set_server_data(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def start_connection(self):
        """
        连接
        :return:
        """
        logging.info("连接tcp...")
        self.__inner_event.clear()
        if self.socket is not None:
            self.socket.close()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(3)
            self.socket.connect((self.server_ip, int(self.server_port)))
            self.__inner_event.set()
            self.outer_event.set()
            self.signal.emit(ConnectData("已连接", ConnectStatusCode.CONNECTED))
            logging.info("tcp连接成功")
        except socket.timeout as e:
            logging.exception(e)
            self.signal.emit(ConnectData("连接失败", ConnectStatusCode.BREAK))
        except TimeoutError as e:
            logging.exception(e)
            self.signal.emit(ConnectData("断开", ConnectStatusCode.BREAK))
            return

    def close(self):
        """
        关闭
        :return:
        """
        self.heartbeat_flag = False
        self.send_flag = False
        self.flag = False

    def run(self) -> None:
        while self.flag:
            if not self.__inner_event.isSet():
                self.start_connection()
                continue
            try:
                data = self.socket.recv(1024).hex()
                logging.info(f"收到数据:{data}")
                header = data[:4]
                if header != "6869":
                    continue
                function_code = data[8:12]
                if function_code == FunctionCode.GET_HUM_TMP.value:
                    self.signal.emit(HumAndTempData(data))
                if function_code == FunctionCode.HEARTBEAT.value:
                    self.signal.emit(HeartBeatData(data))
                elif function_code == FunctionCode.GET_NET_DATA.value:
                    self.signal.emit(NetData(data))
                elif function_code == FunctionCode.GET_DEVICE_DATA.value:
                    self.signal.emit(DeviceData(data))
                elif function_code == FunctionCode.GET_VERSION.value:
                    self.signal.emit(VersionData(data))
                elif function_code == FunctionCode.DOOR_STATE.value:
                    self.signal.emit(DoorStateUpload(data))
                elif function_code == FunctionCode.SET_RTC_TIME.value:
                    # rtc校时
                    self.judge_rtc_time(data)
                elif function_code in [
                    FunctionCode.CONTROL_FAN.value,
                    FunctionCode.SET_DEVICE_PARAM.value,
                    FunctionCode.SET_NET_PARAM.value
                ]:
                    self.signal.emit(IsSuccessData(FunctionCode.CONTROL_FAN, data))
            except socket.timeout:
                pass
            except socket.error as e:
                logging.exception(e)
                self.__inner_event.clear()
        self.heartbeat_close_event.wait()
        self.send_close_event.wait()
        logging.info("关闭socket...")
        if self.socket is not None:
            self.socket.close()
        self.outer_event.set()
        logging.info("socket关闭")


if __name__ == '__main__':
    print(crc_16_modbus("E3 E3 AA 00 FF 00 00 00"))
