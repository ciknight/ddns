# -*- coding: utf-8 -*-
from vendor import DDNS

__all__ = ['Server']


class Server():
    PIDFILE_TEMPLATE = '/tmp/ddns_{vendor}.pid'

    def __init__(self, vendor):
        super().__init__()
        pidfile = self.PIDFILE_TEMPLATE.format(vendor=vendor)
        self.ddns = DDNS(vendor, pidfile)

    @property
    def server_name(self):
        return self.ddns.server.NAME

    def run(self, domain):
        self.ddns.run(domain)

    def start(self, domain):
        self.ddns.start(domain)

    def stop(self):
        self.ddns.stop()

    def restert(self):
        self.ddns.restert()

    def status(self):
        self.ddns.status()
