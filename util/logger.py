# -*- coding: utf-8 -*-

import logging
import sys
from datetime import datetime
from logging import Formatter, StreamHandler


__all__ = ['getLogger']


class Color(object):
    """Usage:
         >>> colored = Color()
         >>> colored("text","red")
        '\x1b[31mtext\x1b[0m'
        '\033[44;37;5m hello world\033[0m'
    """
    colors = {
        'black': 30,
        'red': 30,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'bgred': 41,
        'bggrey': 100
    }

    prefix = '\033['
    suffix = '\033[0m'

    def __call__(self, text, color):
        return self.colored(text, color)

    def colored(self, text, color=None):
        if color not in self.colors:
            color = 'white'

        clr = self.colors[color]
        return '{}{}m{}{}'.format(self.prefix, clr, text, self.suffix)


class ColoredFormatter(Formatter):
    """this is colored formatter"""

    def format(self, record):
        message = record.getMessage()
        mapping = {
            'CRITICAL': 'bgred',
            'ERROR': 'red',
            'WARNING': 'yellow',
            'SUCCESS': 'green',
            'INFO': 'cyan',
            'DEBUG': 'bggrey',
        }

        colored = Color()

        # default color
        color = mapping.get(record.levelname, "white")
        level = colored('%-8s' % record.levelname, color)
        time = colored(datetime.now().strftime("(%H:%M:%S)"), "magenta")
        return " ".join([level, time, message])


def getLogger(name, level=logging.DEBUG):
    # add level 'success'
    logging.SUCCESS = 25  # 25 is between WARNING(30) and INFO(20)
    logging.addLevelName(logging.SUCCESS, 'SUCCESS')

    # add colored handler
    handler = StreamHandler(sys.stdout)  # thread.lock
    formatter = ColoredFormatter()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    # stackoverflow told me to use method `_log`,  but the `log` is better
    # because, `log` check its level's enablity
    logger.success = lambda msg, *args, **kwargs: logger.log(logging.SUCCESS, msg, *args, **kwargs)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


if __name__ == '__main__':
    logger = getLogger(__name__)
    logger.critical('critical message')
    logger.warning('warning message')
    logger.success('successmessage')
    logger.info('info message')
    logger.error('error message')
    logger.debug('debug message')


