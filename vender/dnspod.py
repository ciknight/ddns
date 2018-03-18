# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

import requests
import sys

from config import login_param

pprint = lambda s: sys.stdout.write('%s\n' % s)


class DNSPodError(Exception):
    """
    DNSPod request Exception
    """
    pass


class DNSPod(object):
    """
    Usage DNSPod API implement
    """
    FORMAT = 'json'

    def __init__(self, *args, **kwargs):
        super(DNSPod, self).__init__()
        self._is_token = kwargs.get('is_token')
        self._request_param = {'format': self.FORMAT, 'lang': 'cn'}
        if self._is_token:
            login_data = {'login_token': login_param['login_token']}
        else:
            login_data = {
                'login_email': login_param['login_email'],
                'login_password': login_param['login_password']
            }
        self._request_param.update(login_data)

    def POST(self, url, data=None):
        request_param = self._request_param.copy()
        if data: request_param.update(data)
        response = requests.post(url, request_param)
        if response.status_code != 200:
            raise 'request error_code: %s' % response.status_code

        response = response.json()
        if response['status']['code'] != '1':
            raise DNSPodError(response['status']['message'])

        return response

    def get_domains(self):
        """
        get domain list
        """
        url = 'https://dnsapi.cn/Domain.List'
        data = {'type': 'all'}
        response = self.POST(url, data)
        for index, domain in enumerate(response['domains']):
            pprint('%d %5s %5s %5s' % (index + 1, domain['id'], domain['name'], domain['status']))

    def get_records(self, domain_id):
        """
        get record list for domain
        """
        url = 'https://dnsapi.cn/Record.List'
        data = {'domain_id': domain_id}
        response = self.POST(url, data)
        for index, record in enumerate(response['records']):
            pprint(
                '%d %5s %5s %5s %5s' %
                (index + 1, record['id'], record['name'], record['value'], record['type'])
            )

    def get_single_record(self, domain_id, record_id):
        """
        get a record
        """
        url = 'https://dnsapi.cn/Record.Info'
        data = {'domain_id': domain_id, 'record_id': record_id}
        response = self.POST(url, data)
        return response['record']

    def update_record(self, domain_id, record_id, sub_domain, ip, record_type='A'):
        """
        update record
        update 5 pre hours is too much
        """
        url = 'https://dnsapi.cn/Record.Modify'
        data = {
            'domain_id': domain_id,
            'record_id': record_id,
            'record_type': record_type,
            'value': ip,
            'sub_domain': sub_domain,
            'record_line': '默认'
        }
        try:
            assert self.POST(url, data)
        except Exception:
            return None
        return 1
