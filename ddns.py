# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

from HTTPClient import HttpClient
from config import *
import json

httpclent = HttpClient()

FORMAT = 'json'

login_data = {
    'login_email': login_email,
    'login_password': login_password
}

common_data = {'format': FORMAT, 'lang': 'cn'}
common_data.update(login_data)


def getdomain():
    url = 'https://dnsapi.cn/Domain.List'
    data = {'type': 'all'}
    data.update(common_data)

    code, response = httpclent.Post(url, data)
    if code == 200:
        result = json.loads(response)
    else:
        return '请求失败'

    status = result['status']
    if status['code'] == '1':
        domains = result['domains']
        for index, domain in enumerate(domains):
            print index+1, domain['id'], domain['name']
    else:
        print status['code'], status['message']

def getrecord():
    url = 'https://dnsapi.cn/Record.List'
    data = {''}
    httpclent.Post(url, )


if __name__ == '__main__':
    getdomain()