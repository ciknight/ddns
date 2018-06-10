#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

from docopt import docopt

from server import Server


def main():
    """Usage:
cli.py start --vendor=<vendor> --domain=<domain> [--daemon] [--config=<config_file>]
cli.py stop --vendor=<vendor>
cli.py restart --vendor=<vendor>
cli.py status --vendor=<vendor>
cli.py [-h|-v]

Options:
  -h --help     show this help message
  -v --version  show version
  --watch       watch source files for changes

Commands:
  start         run ddns server
  stop          stop ddns server"""

    arguments = docopt(main.__doc__, version="DDNS 2.0.0")
    if arguments['start']:
        vendor = arguments['--vendor']
        domain = arguments['--domain']
        if arguments['--daemon']:
            Server(vendor).start(domain)
        else:
            Server(vendor).run(domain)
    elif arguments['stop']:
        vendor = arguments['--vendor']
        Server(vendor).stop()
    elif arguments['restart']:
        vendor = arguments['--vendor']
        Server(vendor).restart()
    elif arguments['status']:
        vendor = arguments['--vendor']
        Server(vendor).status()
    else:
        exit(main.__doc__)


if __name__ == "__main__":
    main()
