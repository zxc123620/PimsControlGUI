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
from queue import Queue
from threading import Thread, Event

from PyQt5.QtCore import QThread, pyqtSignal

from collection_module.protocol_objs.basic_format import BasicFormat
from collection_module.protocol_objs.connect_data import ConnectData
from collection_module.protocol_objs.mk_send.defence import DefenceStateData
from collection_module.protocol_objs.mk_send.device_datetime import DeviceDateTimeData
from collection_module.protocol_objs.mk_send.device_net_param import DeviceNetData
from collection_module.protocol_objs.mk_send.device_params import DeviceParamsObj
from collection_module.protocol_objs.mk_send.heartbeat_param import HeartBeatData
from collection_module.protocol_objs.mk_send.is_success_data import IsSuccessData
from collection_module.protocol_objs.mk_send.version import VersionData
from collection_module.tool import crc_16_modbus
from collection_module.function_code import FunctionCode, Enable, TimingType, ConnectStatusCode, \
    SpeakerType, ControlType, LightNo, SpeakerPlayType, ClientType, DefenceControl, GNetSendType


class MKClientSocketThread(QThread):
    signal = pyqtSignal(object)
    HEADER = "e3e4"
    TAIL = "00"

    def __init__(self, device_id="00aa"):
        QThread.__init__(self)
        self.socket = None
        self.server_port = None
        self.server_ip = None
        self.send_queue = Queue()
        self.recv_queue = Queue()
        self.__inner_event = Event()
        # self.header = "e3e4"
        self.device_id = BasicFormat.convert(device_id)
        self.flag = True
        self.heartbeat_flag = True
        self.send_flag = True
        self.heartbeat_close_event = Event()
        self.send_close_event = Event()
        self.outer_event = Event()
        self.connect_flag = False
        self.send_msg_thread = Thread(target=self.send_data_event, daemon=True, name="ClientSocketSendThread")
        self.heartbeat_thread = Thread(target=self.send_heartbeat_event, daemon=True, name="SendHeartBeatThread")
        self.send_msg_thread.start()
        self.heartbeat_thread.start()

    @staticmethod
    def data_valid(data):
        """
        数据验证
        :return:
        """
        BasicFormat(function_code=None, data_raw=data).valid_data()

    def __get_header(self, function_code: FunctionCode):
        """
        组成头部
        :param function_code:
        :return:
        """
        return f"{self.HEADER}{self.device_id}{function_code.value}{self.__get_time()}"

    @staticmethod
    def __get_time():
        """
        获取时间
        :return:
        """
        temp_date = datetime.datetime.now()
        year = f"{(temp_date.year - 2000):02x}"
        month = f"{temp_date.month:02x}"
        day = f"{temp_date.day:02x}"
        hour = f"{temp_date.hour:02x}"
        minute = f"{temp_date.minute:02x}"
        seconds = f"{temp_date.second:02x}"
        data = f"{year}{month}{day}{hour}{minute}{seconds}"
        # logging.info(f"生成指令时间:{data}")
        return data

    def __send_data(self, function_code: FunctionCode, data=''):
        """
        发送数据
        :param data:
        :return:
        """
        header = self.__get_header(function_code)
        data_length = BasicFormat.convert(f"{int(len(data) / 2):04x}") if data else "0000"
        crc_16_data = crc_16_modbus(data) if data else "0000"
        self.send_queue.put(f"{header}{data_length}{data}{crc_16_data}")

    def send_heartbeat_event(self):
        """
        心跳发送线程
        :return:
        """
        while self.heartbeat_flag:
            if self.connect_flag is False:
                continue
            # self.__inner_event.wait()
            time.sleep(3)
            # date_length = "0000"
            # data = f"{}{date_length}"
            self.__send_data(FunctionCode.HEARTBEAT)
            # self.send_queue.put(data + crc_16_modbus(data))
        self.heartbeat_close_event.set()
        logging.info("心跳线程关闭")

    def get_server_time(self):
        """
        获取时间
        :return:
        """
        self.__send_data(FunctionCode.GET_TIME)

    def set_server_time(self):
        """
        设置服务时间为当前时间
        :return:
        """
        self.__send_data(FunctionCode.SET_TIME, self.__get_time())

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
        ip_addr = BasicFormat.convert_addr_to_hex(ip_addr)
        gateway = BasicFormat.convert_addr_to_hex(gateway)
        mask = BasicFormat.convert_addr_to_hex(mask)
        main_dns = BasicFormat.convert_addr_to_hex(main_dns)
        back_up_dns = BasicFormat.convert_addr_to_hex(back_up_dns)
        port = BasicFormat.convert(f"{int(port):04x}")
        mac = str(mac).replace(":", "")
        heartbeat_interval = BasicFormat.convert(f"{int(heartbeat_interval):04x}")
        data = f"{ip_addr}{port}{gateway}{mask}{mac}{main_dns}{back_up_dns}" \
               f"{heartbeat_interval}"
        self.__send_data(FunctionCode.SET_NET_PARAM, data)

    def send_param_data(self,
                        device_id,
                        light_1_enable: Enable,
                        light_2_enable: Enable,
                        light_3_enable: Enable,
                        light_4_enable: Enable,
                        intercom_enable: Enable,
                        g_net_enable: Enable,
                        speaker_1_id,
                        speaker_2_id,
                        speaker_3_id,
                        speaker_4_id,
                        speaker_5_id,
                        speaker_6_id,
                        speaker_7_id,
                        speaker_8_id,
                        speaker_9_id,
                        speaker_10_id,
                        speaker_11_id,
                        speaker_12_id,
                        timing_type: TimingType,
                        time_interval,
                        fixed_ntp_server,
                        fix_ntp_port,
                        dynamic_ntp_server: str,
                        dynamic_ntp_port,
                        dns_server,
                        speaker_1_enable: Enable,
                        speaker_2_enable: Enable,
                        speaker_3_enable: Enable,
                        speaker_4_enable: Enable,
                        speaker_5_enable: Enable,
                        speaker_6_enable: Enable,
                        speaker_7_enable: Enable,
                        speaker_8_enable: Enable,
                        speaker_9_enable: Enable,
                        speaker_10_enable: Enable,
                        speaker_11_enable: Enable,
                        speaker_12_enable: Enable,
                        speaker_type
                        ):
        """
        发送设备参数
        :param speaker_6_enable:
        :param speaker_5_enable:
        :param speaker_4_enable:
        :param speaker_3_enable:
        :param speaker_2_enable:
        :param speaker_1_enable:
        :param g_net_enable:
        :param speaker_6_id:
        :param speaker_5_id:
        :param speaker_4_id:
        :param speaker_3_id:
        :param speaker_2_id:
        :param speaker_1_id:
        :param intercom_enable:
        :param light_4_enable:
        :param light_3_enable:
        :param light_2_enable:
        :param light_1_enable:
        :param device_id:
        :param timing_type:
        :param time_interval:
        :param fixed_ntp_server:
        :param fix_ntp_port:
        :param dynamic_ntp_server:
        :param dynamic_ntp_port:
        :param dns_server:
        :return:
        """
        enable_data = f"{g_net_enable.value}{intercom_enable.value}{speaker_12_enable.value}{speaker_11_enable.value}{speaker_10_enable.value}" \
                      f"{speaker_9_enable.value}{speaker_8_enable.value}{speaker_7_enable.value}{speaker_6_enable.value}{speaker_5_enable.value}" \
                      f"{speaker_4_enable.value}{speaker_3_enable.value}{speaker_2_enable.value}{speaker_1_enable.value}{light_4_enable.value}" \
                      f"{light_3_enable.value}{light_2_enable.value}{light_1_enable.value}"
        speaker_1_id = str(speaker_1_id).zfill(2)
        speaker_2_id = str(speaker_2_id).zfill(2)
        speaker_3_id = str(speaker_3_id).zfill(2)
        speaker_4_id = str(speaker_4_id).zfill(2)
        speaker_5_id = str(speaker_5_id).zfill(2)
        speaker_6_id = str(speaker_6_id).zfill(2)
        speaker_7_id = str(speaker_6_id).zfill(2)
        speaker_8_id = str(speaker_6_id).zfill(2)
        speaker_9_id = str(speaker_6_id).zfill(2)
        speaker_10_id = str(speaker_6_id).zfill(2)
        speaker_12_id = str(speaker_6_id).zfill(2)
        speaker_13_id = str(speaker_6_id).zfill(2)
        speaker_type = str(speaker_type).zfill(2)
        timing_type = BasicFormat.convert(f"{timing_type.value:04x}")
        time_interval = BasicFormat.convert(f"{int(time_interval):04x}")
        fixed_ntp_server = BasicFormat.convert_addr_to_hex(fixed_ntp_server)
        fix_ntp_port = BasicFormat.convert(f"{int(fix_ntp_port):04x}")
        dynamic_ntp_server = binascii.hexlify(dynamic_ntp_server.encode()).decode('utf-8').ljust(60, '0')
        dynamic_ntp_port = BasicFormat.convert(f"{int(dynamic_ntp_port):04x}")
        device_id = BasicFormat.convert(device_id)
        dns_server = BasicFormat.convert_addr_to_hex(dns_server)
        data_inner = f"{device_id}{light_enable}{speaker_enable}{intercom_enable}{speaker_1_id}{speaker_2_id}" \
                     f"{speaker_3_id}{speaker_4_id}{speaker_5_id}{speaker_6_id}{speaker_type}" \
                     f"{timing_type}{time_interval}{fixed_ntp_server}" \
                     f"{fix_ntp_port}{dynamic_ntp_server}{dynamic_ntp_port}{dns_server}"
        self.__send_data(FunctionCode.SET_DEVICE_PARAM, data_inner)

    # def get_hum_and_temp_data(self):
    #     """
    #     获取温湿度数据
    #     :return:
    #     """
    #     data_length = "0000"
    #     data = f"{self.__get_header()}{FunctionCode.GET_HUM_TMP.value}{data_length}"
    #     self.send_queue.put(data + crc_16_modbus(data))

    def get_net_data(self):
        """
        获取网络参数
        :return:
        """
        # data_length = "0000"
        # data = f"{self.__get_header()}{FunctionCode.GET_NET_DATA.value}{data_length}"
        self.__send_data(FunctionCode.GET_NET_DATA)
        # self.send_queue.put(data + crc_16_modbus(data))

    def get_device_param_data(self):
        """
        获取设备参数
        :return:
        """
        # data_length = "0000"
        # data = f"{self.__get_header()}{FunctionCode.GET_DEVICE_DATA.value}{data_length}"
        self.__send_data(FunctionCode.GET_DEVICE_DATA)
        # self.send_queue.put(data + crc_16_modbus(data))

    # def fan_control(self, control: FanControl):
    #     """
    #     开启风扇
    #     :return:
    #     """
    #     data_length = "0200"
    #     data = f"{self.__get_header()}{FunctionCode.CONTROL_FAN.value}{data_length}{control.value}"
    #     self.send_queue.put(data + crc_16_modbus(data))

    def get_version(self):
        """
        获取版本
        :return:
        """
        # data_length = "0000"
        # data = f"{self.__get_header()}{FunctionCode.GET_VERSION.value}{data_length}"
        # self.send_queue.put(data + crc_16_modbus(data))
        self.__send_data(FunctionCode.GET_VERSION)

    def judge_rtc_time(self, data):
        """
        判断是否是读取rtc时间
        :param data:
        :return:
        """
        # data_length = data[12:16]
        # if data_length == "0000":
        self.send_rtc_time()

    def send_rtc_time(self):
        """
        发送校时
        :return:
        """
        # data_length = "0c00"
        date_now = self.__get_time()
        # data = f"{self.__get_header()}{FunctionCode.SET_RTC_TIME.value}{data_length}{date_now}"
        self.__send_data(FunctionCode.SET_RTC_TIME, date_now)
        # self.send_queue.put(data + crc_16_modbus(data))

    def control_light(self, light_no: LightNo, control_type: ControlType):
        """
        信号灯控制
        :param light_no:
        :param control_type:
        :return:
        """
        self.__send_data(FunctionCode.CONTROL_LIGHT, f"{light_no.value}{control_type.value}")

    def control_intercom(self, voice_number, control: ControlType):
        """
        列调控制
        :param voice_number: 语音序号
        :param control: 控制指令
        :return:
        """
        voice_number = f"{int(voice_number):02x}"
        data = f"{control.value}{voice_number}"
        self.__send_data(FunctionCode.INTERCOM_CONTROL, data)

    def control_defence(self, control: DefenceControl):
        """
        布撤防控制
        :param control:
        :return:
        """
        self.__send_data(FunctionCode.DEFENCE_CONTROL, f"{control.value}")

    def set_name(self, client_type: ClientType, name: str):
        """
        设置名称
        :param client_type:
        :param name:
        :return:
        """

        data = f"{client_type.value}{name.encode().hex()}{self.TAIL}"
        self.__send_data(FunctionCode.RENAME, data)

    def get_door_state(self):
        """
        获取门控,布撤防信息
        :return:
        """
        self.__send_data(FunctionCode.GET_DOOR_STATE)

    def control_speaker(self, speaker_id: str, control: ControlType, speaker_type: SpeakerType, speaker_volume: int,
                        speaker_play_type: SpeakerPlayType):
        """
        喇叭控制
        :param control:
        :param speaker_id:
        :param speaker_type: 语音类型
        :param speaker_volume:
        :param speaker_play_type:
        :return:
        """
        speaker_light_color = "01"
        speaker_light_control = "01"
        speaker_volume = f"{speaker_volume:02x}"
        data = f"{speaker_id.zfill(2)}{speaker_type.value}{speaker_light_color}{speaker_light_control}{speaker_volume}" \
               f"{control.value}{speaker_play_type.value}"
        self.__send_data(FunctionCode.SPEAKER_CONTROL, data)

    def g_net_control(self, control: ControlType, voice_type, send_type: GNetSendType, phone_number):
        """
        G网呼叫
        :param control:
        :param voice_type:
        :param send_type:
        :param phone_number:
        :return:
        """
        pass

    def server_reboot(self):
        """
        模块重启
        :return:
        """
        self.__send_data(FunctionCode.DEVICE_REBOOT)

    def send_data_event(self):
        """
        发送数据线程
        :return:
        """
        while self.send_flag:
            # self.__inner_event.wait()
            if self.socket is None or self.connect_flag is False:
                # self.__inner_event.clear()
                continue
            data = self.send_queue.get()
            logging.info(f"发送数据:{data}")
            try:
                self.socket.sendall(bytes.fromhex(str(data)))
            except socket.error as e:
                self.connect_flag = False
                # self.__inner_event.clear()
                # 发送状态
                self.signal.emit(ConnectData("已断开", ConnectStatusCode.BREAK))
        self.send_close_event.set()
        logging.info("发送线程关闭")

    def set_server_data(self, server_ip, server_port):
        """
        设置服务IP地址
        :param server_ip:
        :param server_port:
        :return:
        """
        self.server_ip = server_ip
        self.server_port = server_port

    def start_connection(self):
        """
        连接
        :return:
        """
        logging.info("连接tcp...")
        # self.__inner_event.clear()
        if self.socket is not None:
            self.socket.close()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(3)
            self.socket.connect((self.server_ip, int(self.server_port)))
            # self.__inner_event.set()
            self.outer_event.set()
            self.signal.emit(ConnectData("已连接", ConnectStatusCode.CONNECTED))
            self.connect_flag = True
            logging.info("tcp连接成功")
        except (socket.timeout, TimeoutError, ConnectionRefusedError) as e:
            logging.exception(e)
            self.signal.emit(ConnectData(str(e), ConnectStatusCode.BREAK))
            self.connect_flag = False
        # except TimeoutError as e:
        #     logging.exception(e)
        #     self.signal.emit(ConnectData("断开", ConnectStatusCode.BREAK))
        #     self.connect_flag = False
        # except ConnectionRefusedError as e:
        #     logging.exception(e)
        #     self.signal.emit(ConnectData("目标计算机拒绝", ConnectStatusCode.BREAK))

    def close(self):
        """
        关闭
        :return:
        """
        self.heartbeat_flag = False
        self.send_flag = False
        self.flag = False

    def control(self):
        """
        控制逻辑
        :return:
        """
        while self.flag:
            if self.connect_flag is False:
                self.start_connection()
                continue
            try:
                data = self.socket.recv(1024).hex()
                logging.info(f"收到数据:{data}")
                header = data[:4]
                if header != "6869":
                    continue
                function_code = data[8:12]
                self.data_valid(data)
                # if function_code == FunctionCode.GET_HUM_TMP.value:
                #     self.signal.emit(HumAndTempData(data))
                if function_code == FunctionCode.HEARTBEAT.value:
                    self.signal.emit(HeartBeatData(data))
                elif function_code == FunctionCode.GET_NET_DATA.value:
                    self.signal.emit(DeviceNetData(data))
                elif function_code == FunctionCode.GET_DEVICE_DATA.value:
                    self.signal.emit(DeviceParamsObj(data))
                elif function_code == FunctionCode.GET_VERSION.value:
                    self.signal.emit(VersionData(data))
                # elif function_code == FunctionCode.DOOR_STATE.value:
                #     self.signal.emit(DoorStateUpload(data))
                elif function_code in [FunctionCode.DEFENCE_STATE.value, FunctionCode.GET_DOOR_STATE.value]:
                    self.signal.emit(DefenceStateData(data))
                elif function_code == FunctionCode.GET_TIME.value:
                    self.signal.emit(DeviceDateTimeData(data))
                elif function_code == FunctionCode.SET_RTC_TIME.value:
                    # rtc校时
                    self.send_rtc_time()
                    # self.judge_rtc_time(data)
                elif function_code in [
                    FunctionCode.CONTROL_FAN.value,
                    FunctionCode.SET_DEVICE_PARAM.value,
                    FunctionCode.SET_NET_PARAM.value,
                    FunctionCode.SPEAKER_CONTROL.value,
                    FunctionCode.RENAME.value,
                    FunctionCode.DEFENCE_CONTROL.value,
                    FunctionCode.INTERCOM_CONTROL.value,
                    FunctionCode.SET_TIME.value
                ]:
                    # logging.info("发送弹窗")
                    self.signal.emit(IsSuccessData(data))
            except socket.timeout:
                pass
            except socket.error as e:
                logging.exception(e)
                self.connect_flag = False
                # self.__inner_event.clear()
        # self.heartbeat_close_event.wait()
        # self.send_close_event.wait()
        logging.info("关闭socket...")
        if self.connect_flag is True and self.socket is not None:
            self.socket.close()
        self.outer_event.set()
        logging.info("socket关闭")

    def format(self):
        """
        格式化
        :return:
        """
        pass

    def run(self) -> None:
        self.control()


if __name__ == '__main__':
    print(crc_16_modbus("E3 E3 AA 00 FF 00 00 00"))
