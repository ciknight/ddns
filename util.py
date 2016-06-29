# -*- coding: utf-8 -*-


def smart_str(s, encoding='utf-8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    return s
