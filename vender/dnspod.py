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
        :token: dnspod api token, token format 'ID,Token'
        :format: support json & xml
        :lang: support cn & en
        """
        self._default_params = dict(error_on_empty=self.ERROR_ON_EMPTY, format=format, lang=lang)

        if self.IS_TOKEN:
            self._default_params.update(dict(login_token=token))
        else:
            # Usage login_email & login_password
            raise NotImplementedError

    def _fetch(self, url, data=None):
        request_param = self._default_params.copy()
        if data:
            request_param.update(data)
        response = requests.post(url, request_param)
        if response.status_code != 200:
            logger.error('http request error, response error_code is {}'.format(response.status_code))
            return None

        content = response.json()
        if str(content.get('status', {}).get('code', 0)) != '1':
            logger.error('dnspod api error, error message is {}'.format(content.get('status', {})))
            return None

        return content

    def _get_domain_id_by_name(self, name):
        """Get domain list
        :name: domain name
        """
        url = 'https://dnsapi.cn/Domain.List'
        resp = self._fetch(url, {'type': 'all'})
        assert resp
        domain_id = None
        for domain in resp['domains']:
            logger.debug('{} {}'.format(domain.get('id'), domain.get('name')))
            if domain.get('status') != 'enable':
                continue

            if domain.get('name') == name:
                domain_id = domain.get('id')

        return domain_id

    def _get_record_id_by_name(self, domain_id, name):
        """Get record list for domain
        :domain_id: dnspod domain id
        :name: record name
        """
        url = 'https://dnsapi.cn/Record.List'
        resp = self._fetch(url, {'domain_id': domain_id})
        assert resp
        record_id = None
        for index, record in enumerate(resp['records']):
            logger.debug(
                '{}. {} {} {} {}'.format(
                    index + 1, record.get('id'), record.get('name'), record.get('type'), record.get('value')
                )
            )

            if record.get('name') == name:
                record_id = record.get('id')

        return record_id

    def update_record(self, domain_id, record_id, sub_domain, ip):
        """Update domain record
        """
        url = 'https://dnsapi.cn/Record.Modify'
        data = {
            'domain_id': domain_id,
            'record_id': record_id,
            'record_type': 'A',
            'value': ip,
            'sub_domain': sub_domain,
            'record_line': '默认'
        }
        try:
            assert self._fetch(url, data)
        except Exception:
            return None
        return 1


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    dnspod = DNSPod(token='51780,b2560cab1a46f378d8311ba4f92bf83f')
    domain_id = dnspod._get_domain_id_by_name('whnzy.com')
    record_id = dnspod._get_record_id_by_name(domain_id, 'www')
    print(domain_id)
    print(record_id)
