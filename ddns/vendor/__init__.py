# -*- coding: utf-8 -*-
import os
import time

from util import get_real_ip, split_domain
from util.daemon import Daemon
from vendor.dnspod import DNSPod

DNSPOD = DNSPod.NAME
SUPPORT_VENDOR = (DNSPOD, )


class DDNS(Daemon):
    LAST_IP = None

    def __init__(self, vendor, *args, **kwargs):
        self.server = None
        if vendor not in SUPPORT_VENDOR:
            raise Exception('vendor {} not support'.format(vendor))

        if vendor == DNSPOD:
            token = os.environ.get('DNSPOD_TOKEN')
            assert token, 'Not Found DNSPod Token In Environ'
            self.server = DNSPod(token)

        super().__init__(*args, **kwargs)

    def run(self, domain):
        while True:
            ip = get_real_ip()
            if ip != self.LAST_IP:
                domain_name, sub_domain = split_domain(domain)
                self.server.update(domain_name, sub_domain, ip)

            time.sleep(600)
