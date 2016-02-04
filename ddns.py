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
            print index+1, domain['id'], domain['name'], domain['status']
    else:
        print status['code'], status['message']

def getrecord(domain_id):
    url = 'https://dnsapi.cn/Record.List'
    data = {'domain_id': domain_id}
    data.update(common_data)
    code, response = httpclent.Post(url, data)

    if code == 200:
        result = json.loads(response)
    else:
        return '请求失败'

    status = result['status']
    if status['code'] == '1':
        records = result['records']
        for index, record in enumerate(records):
            print index+1, record['id'], record['name'], record['type']
    else:
        print status['code'], status['message']

if __name__ == '__main__':
    # getrecord('24022514')
    getdomain()