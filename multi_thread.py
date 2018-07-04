# encoding=utf8
"""
多线程(线程池)
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import threading
import os
import threadpool

class exec_system_command(threading.Thread):
    """
    执行系统命令的线程类
    """

    def __init__(self, command_str):
        threading.Thread.__init__(self)
        self.command_str = command_str

    def run(self):
        os.system(self.command_str)

def exec_system_command(command_str):
    """
    执行系统命令
    :param command_str:
    :return:
    """
    print command_str
    try:
        os.system(command_str)
    except Exception as e:
        print str(e)
        print '[ERROR]something wrong in ' + command_str


# 线程池
pool = threadpool.ThreadPool(100)
thread_exec_commands = []
command = 'xxx'
thread_exec_commands.append(command)
requests = threadpool.makeRequests(exec_system_command, thread_exec_commands)
[pool.putRequest(req) for req in requests]
pool.wait()


