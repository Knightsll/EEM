# -*- coding: utf-8 -*-

import re

"""该类用于转换串口指令"""
global top, index, number, unit
top = {
    "go forward": "w",
    "go back": "s",
    "turn left": "a",
    "turn right": "d",
    "stop": "t",
    u"前进": "w",
    u"后退": "s",
    u"左拐": "a",
    u"右拐": "d",
    u"停": "t",
}
"""中文指令优先英文指令"""
index = [u"前进", u"后退", u"左拐", u"右拐", u"停", "go forward", "go back", "turn left", "turn right", "stop"]
number = [u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"零", u"点"]
number_tran = {
    u"一": "1", u"二": "2", u"三": "3", u"四": "4",
    u"五": "5", u"六": "6", u"七": "7", u"八": "8",
    u"九": "9", u"零": "0", u"点": "."
}
unit = [u"度", u"米", "degree", "meter"]
unit_tran = {
    u"度": "o", u"米": "m", "degree": "o", "meter": "m"
}


class word_dispose:

    def __init__(self, word):
        self.word = word
        self.command = []
        self.serial_cmd = ""

    def tran(self):
        """运用预设字典识别主指令"""
        for i in range(len(index)):
            if index[i] in self.word:
                self.command.append(top[index[i]])
                break
        self.word = list(self.word)
        """处理歧义情况"""
        if u"十" in self.word:
            temp = self.word.index(u"十")
            if temp == 0:
                self.word[temp] = "1"
            else:
                if self.word[temp - 1] in number:
                    if self.word[temp + 1] in number:
                        self.word[temp] = ""
                    else:
                        self.word[temp] = "0"
                else:
                    if self.word[temp + 1] in number:
                        self.word[temp] = "1"
                    else:
                        self.word[temp] = "10"

        """中文数字转换阿拉伯数字"""
        for i in range(len(self.word)):
            if self.word[i] in number:
                self.word[i] = number_tran[self.word[i]]
        """运用正则表达式识别阿拉伯数字"""
        self.word = "".join(self.word)
        num_temp = re.findall(r"\d+\.?\d*", self.word)
        if num_temp != []:
            self.command.append(num_temp[0])

        """识别单位"""
        for i in range(len(unit)):
            if unit[i] in self.word:
                self.command.append(unit_tran[unit[i]])
                break
        if self.command == []:
            return "no command"
        else:
            return (self.command)

    def ser_command(self):
        self.command = self.tran()
        if self.command=="no command":
            return "no command"
        else:
            """
            for i in range(len(self.command)):
                if i == len(self.command)-1:
                    self.serial_cmd += self.command[i]+"_*"
                else:
                    self.serial_cmd += self.command[i]+"_"
            """
            self.serial_cmd = self.command[0]
            return self.serial_cmd
