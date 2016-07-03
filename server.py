# -*- coding: utf-8 -*-

import time

from daemon import DDNS

__all__ = ['server']


class Server(object):
    PIDFILE = '/tmp/ddns.pid'

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self.ddns = DDNS(self.PIDFILE)

    @property
    def dnspod(self):
        return self.ddns.dnspod

    def start(self, domain_id, record_id):
        self.ddns.start(domain_id, record_id)

    def stop(self):
        self.ddns.stop()

    def restert(self):
        self.ddns.restert()

    def status(self):
        self.ddns.status()

server = Server()
