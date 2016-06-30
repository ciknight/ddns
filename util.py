# -*- coding: utf-8 -*-

import re
import requests


def smart_str(s, encoding='utf-8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    return s

def get_real_ip():
    response = requests.get('http://www.ip.cn')
    if response.status_code != 200: raise Exception, 'Get IP Error'

    IP = re.findall(r"(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])", response.content)
    if not IP: raise Exception, 'Get IP Error'

    return IP[0]

