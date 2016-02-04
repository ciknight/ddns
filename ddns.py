# -*- coding: utf-8 -*-

from vender.dnspod import DNSPod
from util import get_real_ip


class DDNS(Daemon):
    TIME_INTERVAL = 60 * 60 * 1    # one hours

    def __init__(self, *args, **kwargs):
        super(DDNS, self).__init__(*args, **kwargs)
        self.ddns = DNSPod(is_token=True)

    @property
    def dnspod(self):
        return self.ddns

    def run(self, domain_id, record_id):
        while 1:
            local_ip = get_real_ip()
            if not id:
                raise

            record = self.ddns.get_single_record(domain_id, record_id)
            record_ip = record['value']
            if record_ip != local_ip:
                self._run(record, domain_id, local_ip)
            time.sleep(self.TIME_INTERVAL)

    def _run(self, record, domain_id, local_ip):
        i = 0
        while 1:
            if self.ddns.update_record(domain_id, record['id'], record['sub_domain'], local_ip):
                break
            i += 1
            if i >= 5:
                break
        return 1

