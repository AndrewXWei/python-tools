# encoding=utf8
"""
转换字节数为友好单位
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import threading
import os

def get_bytes(size):
    """
    字节转换
    :param size:
    :return:
    """
    if abs(size) < 1024:
        return str(size) + ' byte'
    elif abs(size) >= 1024 and abs(size) < 1024 * 1024:
        return str(round(size / 1024.0)) + ' KB'
    elif abs(size) >= 1024 * 1024 and abs(size) < 1024 * 1024 * 1024:
        return str(round(size / 1024.0 / 1024.0)) + ' MB'
    elif abs(size) >= 1024 * 1024 * 1024 and abs(size) < 1024 * 1024 * 1024 * 1024:
        return str(round(size / 1024.0 / 1024.0 / 1024.0)) + ' GB'
    elif abs(size) >= 1024 * 1024 * 1024 * 1024 and abs(size) < 1024 * 1024 * 1024 * 1024 * 1024:
        return str(round(size / 1024.0 / 1024.0 / 1024.0 / 1024.0, 2)) + ' TB'