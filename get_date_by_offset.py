# encoding=utf8
"""
日期换算
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import threading
import os

def getDateOf(today, offset):
    """
    获取指定日期
    :param today:
    :param offset:
    :return:
    """
    todaytimeStamp = int(time.mktime(time.strptime(today, '%Y%m%d')))
    wanttimeStamp = todaytimeStamp + 3600 * 24 * offset
    wantdate = time.strftime("%Y%m%d", time.localtime(wanttimeStamp))
    return wantdate
