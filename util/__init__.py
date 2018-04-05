# -*- coding: utf-8 -*-
import logging
import re

import requests


def get_real_ip():
    try:
        response = requests.get('https://myip.ipip.net', timeout=10)
    except Exception:
        return None

    if response.status_code != 200:
        logging.error('http request error, response error_code is {}'.format(response.status_code))
        return None

    IP = re.findall(r"(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])", response.content.decode())
    return IP and IP[0] or None


def split_domain(domain):
    """
    return: domain, sub_domain
    """
    tmp = domain.rsplit('.', maxsplit=2)
    return '.'.join(tmp[-2:]), '.'.join(tmp[:-2])
