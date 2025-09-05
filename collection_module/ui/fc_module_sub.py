#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :collection_module_ui.py
# @Time      :2025/6/20 13:54
# @Author    :zhouxiaochuan
# @Description:
import logging

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from collection_module.client_socket import MKClientSocketThread
from collection_module.function_code import FunctionCode, FanControl, Enable, TimingType, ConnectStatusCode, \
    IntercomType, ControlType, SpeakerType, SpeakerPlayType, ClientType, LightNo, DefenceControl
from collection_module.ui.fc_module import Ui_MainWindow


class FCModuleSubUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.mk_client_socket_thread = None
        self.btn_bind()
        self.set_validator()
        self.setWindowTitle("控制模块上位机-中试-V1.0")

    def set_validator(self):
        """
        验证
        :return:
        """
        self.server_port.setValidator(QIntValidator())
        self.speaker_volume.setValidator(QIntValidator())
        self.net_port.setValidator(QIntValidator())
        self.net_heatbeat_interval.setValidator(QIntValidator())
        self.ntp_interval.setValidator(QIntValidator())
        self.net_addr.setInputMask("000.000.000.000")
        self.server_ip.setInputMask("000.000.000.000")
        self.net_mask.setInputMask("000.000.000.000")
        self.net_gateway.setInputMask("000.000.000.000")
        self.net_dns_1.setInputMask("000.000.000.000")
        self.net_dns_2.setInputMask("000.000.000.000")
        self.net_mac.setInputMask("HH:HH:HH:HH:HH:HH")

    def btn_bind(self):
        """
        绑定
        :return:
        """
        self.get_net_btn.clicked.connect(self.get_net_data_event)
        self.get_device_param_btn.clicked.connect(self.get_device_param_event)
        self.connect_server.clicked.connect(self.start_connect)
        self.close_server.clicked.connect(self.close_connect)
        self.get_version_btn.clicked.connect(self.get_version_event)
        self.set_param_btn.clicked.connect(self.send_device_param_event)
        self.set_net_btn.clicked.connect(self.send_net_param_event)
        self.open_speaker.clicked.connect(lambda: self.speaker_control_event(ControlType.OPEN))
        self.close_speaker.clicked.connect(lambda: self.speaker_control_event(ControlType.CLOSE))
        self.set_qt_name.clicked.connect(self.rename_event)
        self.open_light.clicked.connect(lambda: self.light_control_event(ControlType.OPEN))
        self.close_light.clicked.connect(lambda: self.light_control_event(ControlType.CLOSE))
        self.defence_control.clicked.connect(lambda: self.defence_control_event(DefenceControl.DEF))
        self.undefence_control.clicked.connect(lambda: self.defence_control_event(DefenceControl.UN_DEF))
        self.get_defence_state.clicked.connect(self.get_door_state_event)
        self.intercom_open.clicked.connect(lambda: self.intercom_control_event(ControlType.OPEN))
        self.intercom_close.clicked.connect(lambda: self.intercom_control_event(ControlType.CLOSE))
        self.get_fc_time.clicked.connect(self.get_server_time_event)
        self.set_fc_time.clicked.connect(self.set_server_time_event)
        self.server_restart_btn.clicked.connect(self.server_restart_event)

    def show_data(self, obj):
        """
        显示数据
        :param obj:
        :return:
        """
        logging.info("收到数据,更新到界面")
        if obj.function_code == FunctionCode.GET_NET_DATA:
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
            self.ntp_man.setChecked(obj.timing_type == 0)
            self.ntp_ntp.setChecked(obj.timing_type == 1)
            self.ntp_dn.setChecked(obj.timing_type == 2)
            self.fixed_ntp_server.setText(obj.fixed_ntp_server)
            self.fixed_ntp_port.setText(str(obj.fixed_ntp_port))
            self.dynamic_ntp_server.setText(obj.dynamic_ntp_server)
            self.dynamic_ntp_port.setText(str(obj.dynamic_ntp_port))
            self.ntp_interval.setText(str(obj.time_interval))
            self.dns_analysis.setText(obj.dns_server)
            self.device_id_set.setText(obj.device_id)
            self.light_1_enable.setChecked(obj.alarm_device_enable.light_1_enable == "1")
            self.light_2_enable.setChecked(obj.alarm_device_enable.light_2_enable == "1")
            self.light_3_enable.setChecked(obj.alarm_device_enable.light_3_enable == "1")
            self.light_4_enable.setChecked(obj.alarm_device_enable.light_4_enable == "1")
            self.speaker_1_enable.setChecked(obj.alarm_device_enable.speaker_1_enable == "1")
            self.speaker_2_enable.setChecked(obj.alarm_device_enable.speaker_2_enable == "1")
            self.speaker_3_enable.setChecked(obj.alarm_device_enable.speaker_3_enable == "1")
            self.speaker_4_enable.setChecked(obj.alarm_device_enable.speaker_4_enable == "1")
            self.speaker_5_enable.setChecked(obj.alarm_device_enable.speaker_5_enable == "1")
            self.speaker_6_enable.setChecked(obj.alarm_device_enable.speaker_6_enable == "1")
            self.speaker_7_enable.setChecked(obj.alarm_device_enable.speaker_7_enable == "1")
            self.speaker_8_enable.setChecked(obj.alarm_device_enable.speaker_8_enable == "1")
            self.speaker_9_enable.setChecked(obj.alarm_device_enable.speaker_9_enable == "1")
            self.speaker_10_enable.setChecked(obj.alarm_device_enable.speaker_10_enable == "1")
            self.speaker_11_enable.setChecked(obj.alarm_device_enable.speaker_11_enable == "1")
            self.speaker_12_enable.setChecked(obj.alarm_device_enable.speaker_12_enable == "1")
            self.intercom_checkbox.setChecked(obj.alarm_device_enable.intercom_enable == "1")
            self.g_net_checkbox.setChecked(obj.alarm_device_enable.g_net_enable == "1")
            self.speaker_1_id.setText(obj.speaker_id_obj.speaker_1_id)
            self.speaker_2_id.setText(obj.speaker_id_obj.speaker_2_id)
            self.speaker_3_id.setText(obj.speaker_id_obj.speaker_3_id)
            self.speaker_4_id.setText(obj.speaker_id_obj.speaker_4_id)
            self.speaker_5_id.setText(obj.speaker_id_obj.speaker_5_id)
            self.speaker_6_id.setText(obj.speaker_id_obj.speaker_6_id)
            self.speaker_7_id.setText(obj.speaker_id_obj.speaker_7_id)
            self.speaker_8_id.setText(obj.speaker_id_obj.speaker_8_id)
            self.speaker_9_id.setText(obj.speaker_id_obj.speaker_9_id)
            self.speaker_10_id.setText(obj.speaker_id_obj.speaker_10_id)
            self.speaker_11_id.setText(obj.speaker_id_obj.speaker_11_id)
            self.speaker_12_id.setText(obj.speaker_id_obj.speaker_12_id)

            self.speaker_colunm_num.setText(obj.speaker_id_obj.speaker_voice_num)
            # self.ntp_man.setChecked(obj.timing_type == 0)
            # self.ntp_ntp.setChecked(obj.timing_type == 1)
            # self.ntp_dn.setChecked(obj.timing_type == 2)
            # self.fixed_ntp_server.setText(obj.fixed_ntp_server)
            # self.fixed_ntp_port.setText(str(obj.fixed_ntp_port))
            # self.dynamic_ntp_server.setText(obj.dynamic_ntp_server)
            # self.dynamic_ntp_port.setText(str(obj.dynamic_ntp_port))
            # self.ntp_interval.setText(str(obj.time_interval))
            # self.dns_analysis.setText(obj.dns_server)
            # self.device_id_set.setText(obj.device_id_2)
            # self.light_1_enable.setChecked(obj.light_1_enable == "1")
            # self.light_2_enable.setChecked(obj.light_2_enable == "1")
            # self.light_3_enable.setChecked(obj.light_3_enable == "1")
            # self.light_4_enable.setChecked(obj.light_4_enable == "1")
            # self.speaker_1_enable.setChecked(obj.speaker_1_enable == "1")
            # self.speaker_2_enable.setChecked(obj.speaker_2_enable == "1")
            # self.speaker_3_enable.setChecked(obj.speaker_3_enable == "1")
            # self.speaker_4_enable.setChecked(obj.speaker_4_enable == "1")
            # self.speaker_5_enable.setChecked(obj.speaker_5_enable == "1")
            # self.speaker_6_enable.setChecked(obj.speaker_6_enable == "1")
            # self.speaker_7_enable.setChecked(obj.speaker_7_enable == "1")
            # self.speaker_8_enable.setChecked(obj.speaker_8_enable == "1")
            # self.speaker_9_enable.setChecked(obj.speaker_9_enable == "1")
            # self.speaker_10_enable.setChecked(obj.speaker_10_enable == "1")
            # self.speaker_11_enable.setChecked(obj.speaker_11_enable == "1")
            # self.speaker_12_enable.setChecked(obj.speaker_12_enable == "1")
            # self.speaker_1_id.setText(obj.speaker_1_id)
            # self.speaker_2_id.setText(obj.speaker_2_id)
            # self.speaker_3_id.setText(obj.speaker_3_id)
            # self.speaker_4_id.setText(obj.speaker_4_id)
            # self.speaker_5_id.setText(obj.speaker_5_id)
            # self.speaker_6_id.setText(obj.speaker_6_id)
            # self.speaker_7_id.setText(obj.speaker_7_id)
            # self.speaker_8_id.setText(obj.speaker_8_id)
            # self.speaker_9_id.setText(obj.speaker_9_id)
            # self.speaker_10_id.setText(obj.speaker_10_id)
            # self.speaker_11_id.setText(obj.speaker_11_id)
            # self.speaker_12_id.setText(obj.speaker_12_id)
            # self.intercom_checkbox.setChecked(obj.intercom_enable == "1")
            # self.g_net_checkbox.setChecked(obj.g_net_enable == "1")
            # self.speaker_colunm_num.setText(obj.speaker_type)
        elif obj.function_code == FunctionCode.GET_TIME:
            # 时间
            self.fc_time_edit.setDateTime(obj.server_date)
        elif obj.function_code == FunctionCode.DEFENCE_STATE:
            # 布撤防与开关门
            self.defence_edit.setText(obj.def_state_text)
            # self.front_door.setText(obj.front_door_state_text)
            # self.back_door.setText(obj.back_door_state_text)
        # elif obj.function_code == FunctionCode.DOOR_STATE:
        #     # 开关门
        #     self.door_state_edit.setText(obj.door_state_text)

        elif obj.function_code == FunctionCode.GET_VERSION:
            # 版本信息
            self.version_edit.setText(obj.version_data)
        elif obj.function_code == FunctionCode.HEARTBEAT:
            # 心跳
            self.hard_version_edit.setText(obj.mk_hark_version)
            self.soft_version_edit.setText(obj.mk_soft_version)
        elif obj.function_code == FunctionCode.COMMAND_RESULT:
            # 其他
            QMessageBox.information(self, "控制返回结果", f"{obj.result_text}")
        elif isinstance(obj.function_code, ConnectStatusCode):
            self.status_label.setText(obj.text)

    def server_restart_event(self):
        """
        重启操作
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        result = QMessageBox.warning(self, "设备重启", "确定下发重启指令?", QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            self.mk_client_socket_thread.server_reboot()

    def light_control_event(self, control_type: ControlType):
        """
        信号灯控制
        :param control_type:
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        light_id = LightNo.ONE if self.ligh_1_radio.isChecked() else LightNo.TWO
        self.mk_client_socket_thread.control_light(light_no=light_id, control_type=control_type)

    def get_door_state_event(self):
        """
        获取布撤防信息
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.get_door_state()

    def get_server_time_event(self):
        """
        获取时间
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.get_server_time()

    def set_server_time_event(self):
        """
        设置当前时间
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.set_server_time()

    def defence_control_event(self, control: DefenceControl):
        """
        布撤防控制
        :param control:
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.control_defence(control=control)

    def speaker_control_event(self, control_type: ControlType):
        """
        喇叭控制
        :param control_type:
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        speaker_id = self.speaker_id_set.text()
        speaker_type = SpeakerType.ALARM if self.speaker_type_1.isChecked() else SpeakerType.EVICTION
        speaker_volume = self.speaker_volume.text()
        speaker_play_type = SpeakerPlayType.SIGNAL if self.signal_play.isChecked() else SpeakerPlayType.LOOP
        self.mk_client_socket_thread.control_speaker(speaker_id=speaker_id,
                                                     control=control_type,
                                                     speaker_type=speaker_type,
                                                     speaker_volume=int(speaker_volume),
                                                     speaker_play_type=speaker_play_type
                                                     )

    def rename_event(self):
        """
        重命名
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        client_type = ClientType.MAIN if self.main_qt.isChecked() else ClientType.SUB
        client_name = self.qt_name.text()
        self.mk_client_socket_thread.set_name(client_type=client_type, name=client_name)

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
        if self.ntp_man.isChecked():
            timing_type = TimingType.MANUAL
        elif self.ntp_ntp.isChecked():
            timing_type = TimingType.NTP
        else:
            timing_type = TimingType.DYNAMIC
        time_interval = self.ntp_interval.text()
        fixed_ntp_server = self.fixed_ntp_server.text()
        fix_ntp_port = self.fixed_ntp_port.text()
        dynamic_ntp_server = self.dynamic_ntp_server.text()
        dynamic_ntp_port = self.dynamic_ntp_port.text()
        dns_server = self.dns_analysis.text()
        device_id_set = self.device_id_set.text()
        light_1_enable = Enable.ENABLE if self.light_1_enable.isChecked() else Enable.DISABLE
        light_2_enable = Enable.ENABLE if self.light_2_enable.isChecked() else Enable.DISABLE
        light_3_enable = Enable.ENABLE if self.light_3_enable.isChecked() else Enable.DISABLE
        light_4_enable = Enable.ENABLE if self.light_4_enable.isChecked() else Enable.DISABLE
        speaker_1_enable = Enable.ENABLE if self.speaker_1_enable.isChecked() else Enable.DISABLE
        speaker_2_enable = Enable.ENABLE if self.speaker_2_enable.isChecked() else Enable.DISABLE
        speaker_3_enable = Enable.ENABLE if self.speaker_3_enable.isChecked() else Enable.DISABLE
        speaker_4_enable = Enable.ENABLE if self.speaker_4_enable.isChecked() else Enable.DISABLE
        speaker_5_enable = Enable.ENABLE if self.speaker_5_enable.isChecked() else Enable.DISABLE
        speaker_6_enable = Enable.ENABLE if self.speaker_6_enable.isChecked() else Enable.DISABLE
        intercom_enable = Enable.ENABLE if self.intercom_checkbox.isChecked() else Enable.DISABLE
        g_net_enable = Enable.ENABLE if self.g_net_checkbox.isChecked() else Enable.DISABLE
        speaker_1_id = self.speaker_1_id.text()
        speaker_2_id = self.speaker_2_id.text()
        speaker_3_id = self.speaker_3_id.text()
        speaker_4_id = self.speaker_4_id.text()
        speaker_5_id = self.speaker_5_id.text()
        speaker_6_id = self.speaker_6_id.text()
        self.mk_client_socket_thread.send_param_data(
            device_id=device_id_set,
            light_1_enable=light_1_enable,
            light_2_enable=light_2_enable,
            light_3_enable=light_3_enable,
            light_4_enable=light_4_enable,
            intercom_enable=intercom_enable,
            g_net_enable=g_net_enable,
            speaker_1_id=speaker_1_id,
            speaker_2_id=speaker_2_id,
            speaker_3_id=speaker_3_id,
            speaker_4_id=speaker_4_id,
            speaker_5_id=speaker_5_id,
            speaker_6_id=speaker_6_id,
            timing_type=timing_type,
            time_interval=time_interval,
            fixed_ntp_server=fixed_ntp_server,
            fix_ntp_port=fix_ntp_port,
            dynamic_ntp_server=dynamic_ntp_server,
            dynamic_ntp_port=dynamic_ntp_port,
            dns_server=dns_server,
            speaker_1_enable=speaker_1_enable,
            speaker_2_enable=speaker_2_enable,
            speaker_3_enable=speaker_3_enable,
            speaker_4_enable=speaker_4_enable,
            speaker_5_enable=speaker_5_enable,
            speaker_6_enable=speaker_6_enable,
            speaker_type=int(self.speaker_colunm_num.text())
        )

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
        self.mk_client_socket_thread.set_net_param_data(ip_addr=ip_addr, port=port, gateway=gateway, mask=mask,
                                                        mac=mac,
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
        # self.hum_enable_radio.setChecked(False)
        # self.hum_disable_radio.setChecked(False)

        self.ntp_man.setChecked(False)
        self.ntp_ntp.setChecked(False)
        self.ntp_dn.setChecked(False)
        # self.hum_id_edit.clear()
        # self.fan_open_tem.clear()
        # self.fan_open_tem.clear()
        self.fixed_ntp_server.clear()
        self.fixed_ntp_port.clear()
        self.dynamic_ntp_server.clear()
        self.dynamic_ntp_port.clear()
        self.dns_analysis.clear()
        self.dns_analysis.clear()
        self.light_1_enable.setChecked(False)
        self.light_2_enable.setChecked(False)
        self.light_3_enable.setChecked(False)
        self.light_4_enable.setChecked(False)
        self.intercom_checkbox.setChecked(False)
        self.g_net_checkbox.setChecked(False)
        self.speaker_1_id.clear()
        self.speaker_2_id.clear()
        self.speaker_3_id.clear()
        self.speaker_4_id.clear()
        self.speaker_5_id.clear()
        self.speaker_6_id.clear()
        self.speaker_1_enable.setChecked(False)
        self.speaker_2_enable.setChecked(False)
        self.speaker_3_enable.setChecked(False)
        self.speaker_4_enable.setChecked(False)
        self.speaker_5_enable.setChecked(False)
        self.speaker_6_enable.setChecked(False)
        self.speaker_colunm_num.clear()
        # self.ntp_server.clear()
        # self.ntp_port.clear()
        if self.mk_client_socket_thread is None:
            return
        self.mk_client_socket_thread.get_device_param_data()

    def intercom_control_event(self, control: ControlType):
        """
        列调控制
        :param control:
        :return:
        """
        if self.mk_client_socket_thread is None:
            return
        if self.intercom_voice_1.isChecked():
            voice_num = 1
        elif self.intercom_voice_2.isChecked():
            voice_num = 2
        elif self.intercom_voice_3.isChecked():
            voice_num = 3
        else:
            voice_num = 4
        self.mk_client_socket_thread.control_intercom(voice_num, control)

    def get_hum_and_tem_data_event(self):
        """
        获取温湿度
        :return:
        """
        # self.device_time.clear()
        # self.hum_tem_state.clear()
        # self.tem_data.clear()
        # self.hum_data.clear()
        # self.door_state.clear()
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
        if not (server_port and server_ip and self.local_device_id.text()):
            return
        self.mk_client_socket_thread = MKClientSocketThread(self.local_device_id.text())
        # self.mk_client_socket_thread.heartbeat_flag = False
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
