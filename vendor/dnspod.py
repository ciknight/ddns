# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

import requests

from util.logger import getLogger

logger = getLogger(__name__)


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

    def _add_record(self, domain_id, sub_domain, ip):
        """Add record
        """
        url = 'https://dnsapi.cn/Record.Create'
        data = {
            'domain_id': domain_id,  # or domain name
            'record_type': 'A',
            'value': ip,
            'sub_domain': sub_domain,
            'record_line': '默认'

        }
        assert self._fetch(url, data)
        return True

    def _update_record(self, domain_id, record_id, sub_domain, ip):
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
        assert self._fetch(url, data)
        return True

    def update(self, domain, sub_domain, ip):
        try:
            domain_id = self._get_domain_id_by_name(domain)
            assert domain_id

            record_id = self._get_record_id_by_name(domain_id, sub_domain)
            if not record_id:
                self._add_record(domain_id, sub_domain, ip)
            else:
                self._update_record(domain_id, record_id, sub_domain, ip)

            return True
        except Exception:
            logger.info('update domain {} failed'.format(domain))
            return False


if __name__ == '__main__':
    dnspod = DNSPod(token='51780,b2560cab1a46f378d8311ba4f92bf83f')
    dnspod.update('whnzy.com', 'www', '127.0.0.1')
