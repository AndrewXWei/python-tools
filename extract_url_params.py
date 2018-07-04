# encoding=utf8
"""
解析url参数列表
"""
import urlparse
from urllib import unquote as unquote


def get_params_dict(url):
    """
    获得参数字典
    :param url:
    :param param:
    :return:
    """
    query = urlparse.urlparse(url).query
    return dict([(k, unquote(v[0])) for k, v in urlparse.parse_qs(query).items()])