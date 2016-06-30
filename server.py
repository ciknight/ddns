# -*- coding: utf-8 -*-

import time

from daemon import DDNS

__all__ = ['server']


class Server(object):
    PIDFILE = 'ddns.pid'
    HOME_DIR = '/tmp'

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self.ddns = DDNS(self.PIDFILE, home_dir=self.HOME_DIR)

    @property
    def dnspod(self):
        return self.ddns.dnspod

    def run(self, domain_id, record_id):
        self.ddns.run(domain_id, record_id)

    def stop(self):
        self.ddns.stop()

    def restert(self):
        self.ddns.restert()

    def status(self):
        self.ddns.status()

server = Server()
