# -*- coding: utf-8 -*-

import unicodedata


def strip_accents(s):
    u = isinstance(s, str) and s or str(s, 'utf8')
    a = ''.join((c for c in unicodedata.normalize('NFKD', u)
                 if unicodedata.category(c) != 'Mn'))
    return str(a)
