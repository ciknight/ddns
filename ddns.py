# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

from HTTPClient import HttpClient
from config import *
import json
import time

httpclient = HttpClient()

FORMAT = 'json'
TIME_INTERVAL = 60*60*12

login_data = {
    'login_email': login_email,
    'login_password': login_password
}

common_data = {'format': FORMAT, 'lang': 'cn'}
common_data.update(login_data)


def getdomain():
    """get domain list
    """
    url = 'https://dnsapi.cn/Domain.List'
    data = {'type': 'all'}
    data.update(common_data)

    code, response = httpclient.Post(url, data)
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
    """get record list for domain
    """
    url = 'https://dnsapi.cn/Record.List'
    data = {'domain_id': domain_id}
    data.update(common_data)
    code, response = httpclient.Post(url, data)

    if code == 200:
        result = json.loads(response)
    else:
        return '请求失败'

    status = result['status']
    if status['code'] == '1':
        records = result['records']
        for index, record in enumerate(records):
            print index+1, record['id'], record['name'], record['value'], record['type']
    else:
        print status['code'], status['message']


def get_person_record(domain_id, record_id):
    url = 'https://dnsapi.cn/Record.Info'
    data = {'domain_id': domain_id, 'record_id': record_id}
    data.update(common_data)
    code, response = httpclient.Post(url, data)

    if code == 200:
        result = json.loads(response)
    else:
        return '请求失败'

    status = result['status']
    if status['code'] == '1':
        record = result['record']
        return record['value']
    else:
        print status['code'], status['message']
        return None


def run(domain_id, record_id):

    while True:
        __run(domain_id, record_id)
        time.sleep(TIME_INTERVAL)


def __run(domain_id, record_id):
    """modify record ip
        ddns main
    """
    url = 'https://dnsapi.cn/Record.Modify'

    value = get_person_record(domain_id, record_id)
    ip = __get_global_ip()

    if not ip:
        print 'ip 获取失败'
        return None
    if ip == value:
        print 'ip无变动    '
        return None

    data = {'domain_id': domain_id, 'record_id': record_id,
            'record_type': 'A', 'record_line': '默认',
            'value': ip, 'sub_domain': 'my'
            }

    data.update(common_data)

    code, response = httpclient.Post(url, data)

    if code == 200:
        result = json.loads(response)
    else:
        return '请求失败'

    status = result['status']
    if status['code'] == '1':
        print '修改成功'
    else:
        print status['code'], status['message']


def __get_global_ip():
    import re
    url = "http://www.ip.cn/"
    code, request = httpclient.Get(url)
    # print request
    IP = re.findall(r"(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])", request)
    if IP:
        return IP[0]
    return None

if __name__ == '__main__':
    getrecord('24022514')
    print get_person_record('24022514', '113270166')
    # getdomain()