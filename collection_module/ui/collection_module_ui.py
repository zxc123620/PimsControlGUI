#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :collection_module_ui.py
# @Time      :2025/6/20 13:54
# @Author    :zhouxiaochuan
# @Description:
import logging
import socket

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from pims.collection_module.client_socket import MKClientSocketThread
from pims.collection_module.function_code import FunctionCode, FanControl, Enable, TimingType, ConnectStatusCode
from pims.collection_module.ui.untitled import Ui_MainWindow


class CollectionModuleUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.mk_client_socket_thread = None
        self.btn_bind()
        self.set_validator()
        self.setWindowTitle("前端采集单元-采集模块上位机-中试-V1.0")

    def set_validator(self):
        self.server_port.setValidator(QIntValidator())
        self.net_port.setValidator(QIntValidator())
        self.net_heatbeat_interval.setValidator(QIntValidator())
        self.fan_open_tem.setValidator(QIntValidator())
        self.fan_close_tem.setValidator(QIntValidator())
        self.hum_id_edit.setValidator(QIntValidator())
        self.ntp_interval.setValidator(QIntValidator())
        self.net_addr.setInputMask("000.000.000.000")
        self.server_ip.setInputMask("000.000.000.000")
        self.net_mask.setInputMask("000.000.000.000")
        self.net_gateway.setInputMask("000.000.000.000")
        self.net_dns_1.setInputMask("000.000.000.000")
        self.net_dns_2.setInputMask("000.000.000.000")
        self.net_mac.setInputMask("HH:HH:HH:HH:HH:HH")

    def btn_bind(self):
        self.get_hum_and_temp_data.clicked.connect(self.get_hum_and_tem_data_event)
        self.get_net_btn.clicked.connect(self.get_net_data_event)
        self.get_device_param_btn.clicked.connect(self.get_device_param_event)
        self.open_fan_btn.clicked.connect(lambda: self.fan_control(FanControl.OPEN))
        self.close_fan_btn.clicked.connect(lambda: self.fan_control(FanControl.CLOSE))
        self.connect_server.clicked.connect(self.start_connect)
        self.close_server.clicked.connect(self.close_connect)
        self.get_version_btn.clicked.connect(self.get_version_event)
        self.set_param_btn.clicked.connect(self.send_device_param_event)
        self.set_net_btn.clicked.connect(self.send_net_param_event)

    def show_data(self, obj):
        """
        显示数据
        :param obj:
        :return:
        """
        logging.info("收到数据,更新到界面")
        if obj.function_code == FunctionCode.GET_HUM_TMP:
            # 温湿度
            self.device_time.setText(obj.device_date_text)
            self.hum_tem_state.setText(obj.hum_state_text)
            self.tem_data.setText(str(obj.tem_data))
            self.hum_data.setText(str(obj.hum_data))
            self.door_state.setText(obj.door_state_text)
            self.door_state_edit.setText(obj.door_state_text)

        elif obj.function_code == FunctionCode.GET_NET_DATA:
            # 网络参数
            self.net_addr.setText(obj.ip_addr_text)
            self.net_port.setText(str(obj.ip_port))
            self.net_gateway.setText(obj.gateway_text)
            self.net_mask.setText(obj.mask_text)
            self.net_dns_1.setText(obj.dns_1_text)
            self.net_dns_2.setText(obj.dns_2_text)
            self.net_mac.setText(obj.mac)
            self.net_heatbeat_interval.setText(str(obj.heartbeat_interval))

        elif obj.function_code == FunctionCode.GET_DEVICE_DATA:
            # 设备参数
            self.hum_enable_radio.setChecked(obj.hum_enable == 1)
            self.hum_disable_radio.setChecked(obj.hum_enable == 0)
            self.ntp_man.setChecked(obj.timing_type == 0)
            self.ntp_ntp.setChecked(obj.timing_type == 1)
            self.ntp_dn.setChecked(obj.timing_type == 2)
            self.hum_id_edit.setText(str(obj.hum_id))
            self.fan_open_tem.setText(str(obj.fan_open_temp))
            self.fan_close_tem.setText(str(obj.fan_close_temp))
            self.fixed_ntp_server.setText(obj.fixed_ntp_server)
            self.fixed_ntp_port.setText(str(obj.fixed_ntp_port))
            self.dynamic_ntp_server.setText(obj.dynamic_ntp_server)
            self.dynamic_ntp_port.setText(str(obj.dynamic_ntp_port))
            self.ntp_interval.setText(str(obj.time_interval))
            self.dns_analysis.setText(obj.dns_server)

        elif obj.function_code == FunctionCode.DOOR_STATE:
            # 开关门
            self.door_state_edit.setText(obj.door_state_text)

        elif obj.function_code == FunctionCode.GET_VERSION:
            # 版本信息
            self.version_edit.setText(obj.version_data)
        elif obj.function_code == FunctionCode.HEARTBEAT:
            # 心跳
            self.heartbeat_date_edit.setText(obj.device_date_text)
            self.soft_version_edit.setText(obj.fc_version)
        elif obj.function_code == FunctionCode.CONTROL_FAN:
            # 其他
            QMessageBox.information(self, "控制结果", obj.is_success_text)
        elif isinstance(obj.function_code, ConnectStatusCode):
            self.status_label.setText(obj.text)

    def send_device_param_event(self):
        """
        发送设备参数
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        result = QMessageBox.warning(self, "设备参数配置", "请再次确认", QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        hum_enable = Enable.ENABLE if self.hum_enable_radio.isChecked() else Enable.DISABLE
        if self.ntp_man.isChecked():
            timing_type = TimingType.MANUAL
        elif self.ntp_ntp.isChecked():
            timing_type = TimingType.NTP
        else:
            timing_type = TimingType.DYNAMIC
        hum_id = self.hum_id_edit.text()
        fan_open_temp = self.fan_open_tem.text()
        fan_close_temp = self.fan_close_tem.text()
        time_interval = self.ntp_interval.text()
        fixed_ntp_server = self.fixed_ntp_server.text()
        fix_ntp_port = self.fixed_ntp_port.text()
        dynamic_ntp_server = self.dynamic_ntp_server.text()
        dynamic_ntp_port = self.dynamic_ntp_port.text()
        dns_server = self.dns_analysis.text()
        device_id_set = self.device_id_set.text()
        self.mk_client_socket_thread.send_param_data(hum_enable=hum_enable, hum_id=hum_id,
                                                     fan_open_temp=fan_open_temp, fan_close_temp=fan_close_temp,
                                                     timing_type=timing_type, time_interval=time_interval,
                                                     fixed_ntp_server=fixed_ntp_server,
                                                     fix_ntp_port=fix_ntp_port, dynamic_ntp_server=dynamic_ntp_server,
                                                     dynamic_ntp_port=dynamic_ntp_port, dns_server=dns_server,device_id=device_id_set)

    def send_net_param_event(self):
        """
        设置网络参数
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        result = QMessageBox.warning(self, "设备参数配置", "请再次确认", QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        ip_addr = self.net_addr.text()
        port = self.net_port.text()
        gateway = self.net_gateway.text()
        mask = self.net_mask.text()
        mac = self.net_mac.text()
        main_dns = self.net_dns_1.text()
        back_up_dns = self.net_dns_2.text()
        heartbeat_interval = self.net_heatbeat_interval.text()
        self.mk_client_socket_thread.set_net_param_data(ip_addr=ip_addr, port=port, gateway=gateway, mask=mask, mac=mac,
                                                        main_dns=main_dns, back_up_dns=back_up_dns,
                                                        heartbeat_interval=heartbeat_interval)

    def get_net_data_event(self):
        """
        获取网络参数
        :return:
        """
        self.net_addr.clear()
        self.net_port.clear()
        self.net_gateway.clear()
        self.net_dns_1.clear()
        self.net_dns_2.clear()
        self.net_mac.clear()
        self.net_heatbeat_interval.clear()
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.get_net_data()

    def fan_control(self, control: FanControl):
        """
        风扇控制
        :param control:
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.fan_control(control)

    def get_device_param_event(self):
        """
        获取设备参数
        :return:
        """
        self.hum_enable_radio.setChecked(False)
        self.hum_disable_radio.setChecked(False)
        self.ntp_man.setChecked(False)
        self.ntp_ntp.setChecked(False)
        self.ntp_dn.setChecked(False)
        self.hum_id_edit.clear()
        self.fan_open_tem.clear()
        self.fan_open_tem.clear()
        self.fixed_ntp_server.clear()
        self.fixed_ntp_port.clear()
        self.dynamic_ntp_server.clear()
        self.dynamic_ntp_port.clear()
        self.dns_analysis.clear()
        self.dns_analysis.clear()
        # self.ntp_server.clear()
        # self.ntp_port.clear()
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.get_device_param_data()

    def get_hum_and_tem_data_event(self):
        """
        获取温湿度
        :return:
        """
        self.device_time.clear()
        self.hum_tem_state.clear()
        self.tem_data.clear()
        self.hum_data.clear()
        self.door_state.clear()
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.get_hum_and_temp_data()

    def get_version_event(self):
        self.version_edit.clear()
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.get_version()

    def start_connect(self):
        """
        连接
        :return:
        """
        server_ip = self.server_ip.text()
        logging.info(server_ip)
        server_port = self.server_port.text()
        if not(server_port and server_ip and self.local_device_id.text()):
            return
        self.mk_client_socket_thread = MKClientSocketThread(self.local_device_id.text())
        event = self.mk_client_socket_thread.outer_event
        self.mk_client_socket_thread.signal.connect(self.show_data)
        self.mk_client_socket_thread.set_server_data(server_ip, server_port)
        self.mk_client_socket_thread.start()
        self.status_label.setText("连接中...")
        event.wait(3)
        if event.isSet():
            self.status_label.setText("已连接")
            self.connect_server.setEnabled(False)
            self.close_server.setEnabled(True)
        else:
            self.status_label.setText("连接失败")
            self.mk_client_socket_thread.close()
        event.clear()

    def close_connect(self):
        """
        关闭
        :return:
        """
        if self.mk_client_socket_thread is not None:
            event = self.mk_client_socket_thread.outer_event
            event.clear()
            self.mk_client_socket_thread.close()
            event.wait()
        self.mk_client_socket_thread = None
        self.status_label.setText("已断开")
        self.connect_server.setEnabled(True)
        self.close_server.setEnabled(False)
