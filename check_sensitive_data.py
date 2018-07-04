# encoding=utf8
"""
check sensitive data
"""
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import re

search_pattern = re.compile(r'[a-zA-Z0-9\-]+')
clean_pattern = re.compile(r"""
(^(13[0-9]|14[57]|15[012356789]|17[0678]|18[0-9])[0-9]{8}$)  # 13x 14x 15x 17x 18x开头的手机号码
|(^(^0\d{2}-?\d{8}$)|(^0\d{3}-?\d{7}$)|(^0\d2-?\d{8}$)|(^0\d3-?\d{7}$)$) # 固定电话号码
|(^(\d{16}|\d{19})$) # 16位或者19位银行卡
|(^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$) # 15位身份证
|(^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$) # 18位身份证
|(^[1-9][0-9]{4,10}$) # 腾讯QQ号，从10000开始
|(^[1-9]\d{3}-?((0\d)|(1[0-2]))-?(([0|1|2]\d)|3[0-1])$) # 生日 1990101 或者 1990-01-01
|(^[0-9]{6}$) # 6位银行卡密码
""", re.VERBOSE)

def check_sensitive_data(content):
    """
    check sensitive data
    :param content:
    :return:
    """
    sensitive_items = []
    # filter by character format
    for item in search_pattern.findall(content):
        # check by regulars
        if clean_pattern.match(item):
            sensitive_items.append(item)
    if len(sensitive_items) > 0:
        return(True, sensitive_items)
    else:
        return(False, sensitive_items)

if __name__ == '__main__':
    log = '生日电话19910101'
    print check_sensitive_data(log)[0]
    if ('密码' in log or '电话' in log or '身份证' in log
        or '卡号' in log):
        print log
