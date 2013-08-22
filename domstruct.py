# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 08/19/2013, updated 08/21/2013
#
""" Domain name structure, a wrapper around
    publicsuffix.get_public_suffix()

"""
__all__ = [
    'DomainStruct',
]
print('Executing %s' %  __file__)

import os, sys, time
from collections import namedtuple

from .publicsuffix import get_public_suffix

class DomainStruct (object):
    """ Return a DomStruct, representing the structure of the input domain

        Example 1 (valid eTLD, and len(domain)>len(eT2LD)):
        domain = 'www.5.4.3.google.co.uk'
        nowww = '5.4.3.google.co.uk'
        et2s = ['google', 'co', 'uk']
        eSLD = 'google'
        sub = 'www.5.4.3'
        subs = ['www', '5', '4', '3']
        eTkLD = [
            'co.uk',
            'google.co.uk',
            '3.google.co.uk',
            '4.3.google.co.uk',
            '5.4.3.google.co.uk',
            'www.5.4.3.google.co.uk',
        ]

        Example 2 (valid eTLD, and len(domain)==len(eT2LD)):
        domain = 'google.co.uk'
        nowww = 'google.co.uk'
        et2s = ['google', 'co', 'uk']
        eSLD = 'google'
        sub = ''
        eTkLD = [
            'co.uk',
            'google.co.uk',
        ]

        Example 3 (invalid eTLD case):
        domain = 'www.bar.local'
        nowww = 'bar.local'
        et2s = ['local']
        eTkLD = []
    """

    #__slots__ = ()

    def __init__ (self, domain):
        """
        """
        eT2LD = get_public_suffix(domain)
        et2s = eT2LD.split('.')
        eTLD = '.'.join(et2s[1:])

        if eTLD == '':
            self.isFQDN = False
            self.eTkLD = []
            self.sub = self.eSLD = None

        else:
            self.isFQDN = True
            self.eTkLD = [eTLD, eT2LD]
            self.eSLD = et2s[0]
            self.sub = domain[:-len(eT2LD)-1]
            _subs = self.sub.split('.') if len(self.sub) > 0 else []
            for i in xrange(len(_subs)):
                # i=0, k=3, x=1
                # i=1, k=4, x=2
                _eTkLD = '.'.join(_subs[-i-1:]+[eT2LD])
                self.eTkLD.append(_eTkLD)

        self.domain = domain
        self.nowww = domain[4:] if domain.startswith('www.') else domain

