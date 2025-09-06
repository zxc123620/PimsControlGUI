#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2025/9/6 09:10
# Author:zhouxiaochuan
# Description:
from collection_module.function_code import FunctionCode
from collection_module.protocol_objs.basic_format import BasicFormat


class SpeakerControl(BasicFormat):
    SPEAKER_VOICE_TYPE = ["0", "驱赶动物", "驱赶行人", "其他"]
    SPEAKER_COLOR = ["0", "红色", "黄色", "绿色"]
    PLAYBACK_TYPE = ["0", "单曲", "循环"]
    BYTES_NUM_LIST = [1,2,3,4,5,6,7]
    def __init__(self, data_raw):
        BasicFormat.__init__(self, FunctionCode.SPEAKER_CONTROL, data_raw)
        self.speaker_no = int(self.data_inner[0:self.BYTES_NUM_LIST[0]*2],16)
        self.speaker_voice_type_str = self.SPEAKER_VOICE_TYPE[int(self.data_inner[self.BYTES_NUM_LIST[0]*2:self.BYTES_NUM_LIST[1]*2])]
        self.speaker_color_str = self.SPEAKER_COLOR[int(self.data_inner[self.BYTES_NUM_LIST[1]*2:self.BYTES_NUM_LIST[2]*2])]
        self.speaker_color_control_str = self.COMMAND_STR[int(self.data_inner[self.BYTES_NUM_LIST[2]*2:self.BYTES_NUM_LIST[3]*2])]
        self.speaker_volume_str = str(int(self.data_inner[self.BYTES_NUM_LIST[3] * 2:self.BYTES_NUM_LIST[4] * 2], 16))
        self.speaker_voice_control_str = self.COMMAND_STR[int(self.data_inner[self.BYTES_NUM_LIST[4]*2:self.BYTES_NUM_LIST[5]*2])]
        self.playback_type_str = self.PLAYBACK_TYPE[int(self.data_inner[self.BYTES_NUM_LIST[5]*2:self.BYTES_NUM_LIST[6]*2])]




    def __str__(self):
        return self.get_infos() + (f"功能: 喇叭控制, 喇叭编号: {self.speaker_no}, 声音类型:{self.speaker_voice_type_str}, "
                                   f"灯光: {self.speaker_color_str}, 灯光控制: {self.speaker_color_control_str}, "
                                   f"音量: {self.speaker_volume_str}, 指令: {self.speaker_voice_control_str}, "
                                   f"播放模式: {self.playback_type_str}")