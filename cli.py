# -*- coding: utf-8 -*-
"""
@auther: ci_knight <ci_knight@msn.cn>
@date: 2016-02-03 19:24:33
"""

from docopt import docopt


def main():
    """Usage:
    cli.py run <record_id>
    cli.py getrecord <domain_id>
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
    # print arguments
    if arguments['run']:
        print 'run'
    elif arguments['getdomain']:
        from ddns import getdomain
        getdomain()
    elif arguments['create']:
        print 'create'
    elif arguments['getrecord']:
        print 'getrecord'
    else:
        exit(main.__doc__)



if __name__ == "__main__":
    main()
