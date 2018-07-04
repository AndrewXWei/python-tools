# encoding=utf8
"""
工具集
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import threading
import os

# 省份列表
provinceList = [
    '内蒙古',
    '湖南',
    '吉林',
    '安徽',
    '澳门',
    '辽宁',
    '上海',
    '江西',
    '广东',
    '山东',
    '天津',
    '河南',
    '甘肃',
    '宁夏',
    '浙江',
    '台湾',
    '陕西',
    '江苏',
    '湖北',
    '贵州',
    '新疆',
    '黑龙江',
    '海南',
    '河北',
    '广西',
    '山西',
    '北京',
    '香港',
    '福建',
    '重庆',
    '云南',
    '四川',
    '西藏',
    '青海']


# 执行系统命令并获取状态
import commands
status, output = commands.getstatusoutput('ls')

