# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

from docopt import docopt
from server import server


def main():
    """Usage:
    cli.py getrecord [<domain_id>]
    cli.py run [<domain_id>] [<record_id>]
    cli.py (create|getdomain)
    cli.py [-h|-v]

Options:
  -h --help     show this help message
  -v --version  show version
  --watch       watch source files for changes

Commands:
  run           deploy ddns in current directory
  getrecord     get record list in current domain
  getdomain     get all domain
  create        create a record"""

    arguments = docopt(main.__doc__, version="dnspod ddns 1.0")
    if arguments['run']:
        domain_id = arguments['<domain_id>']
        record_id = arguments['<record_id>']
        server.run(domain_id, record_id)
    elif arguments['getdomain']:
        server.dnspod.get_domains()
    elif arguments['create']:
        raise NotImplementedError
    elif arguments['getrecord']:
        domain_id = arguments['<domain_id>']
        server.dnspod.get_records(domain_id)
    else:
        exit(main.__doc__)



if __name__ == "__main__":
    main()
