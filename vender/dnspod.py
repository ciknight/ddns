# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

import logging

import requests

logger = logging.getLogger(__name__)


class DNSPodError(Exception):
    """
    DNSPod request Exception
    """
    pass


class DNSPod():
    """
    Usage DNSPod API Implemented
    """

    ERROR_ON_EMPTY = 'no'
    IS_TOKEN = True

    def __init__(self, token, format='json', lang='cn'):
        """dnspod api document url https://www.dnspod.cn/docs/info.html
        :param token: dnspod api token, token format 'ID,Token'
        :param format: support json & xml
        :param lang: support cn & en
        """
        self._default_params = dict(
            error_on_empty=self.ERROR_ON_EMPTY,
            format=format,
            lang=lang
        )

        if self.IS_TOKEN:
            self._default_params.update(dict(
                login_token=token
            ))
        else:
            # Usage login_email & login_password
            raise NotImplementedError

    def _post(self, url, data=None):
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
