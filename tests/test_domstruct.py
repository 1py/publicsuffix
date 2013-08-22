#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 08/19/2013, updated 08/21/2013
#
""" Unit tests for domstruct.py
"""
print('Executing %s' %  __file__)

import unittest
import os, sys, time

from netutils import publicsuffix


class Test_get_domain_struct (unittest.TestCase):
    """
    """
    def test_normal_fqdn_level6 (self):
        domain = '6.5.4.3.google.co.uk'
        ds = publicsuffix.DomainStruct(domain)
        self.assertEqual (ds.nowww, '6.5.4.3.google.co.uk')
        self.assertEqual (ds.eSLD, 'google')
        self.assertEqual (ds.sub, '6.5.4.3')
        self.assertEqual (ds.isFQDN, True)
        self.assertListEqual(ds.eTkLD, [
            'co.uk',  # eTLD
            'google.co.uk',
            '3.google.co.uk',
            '4.3.google.co.uk',
            '5.4.3.google.co.uk',
            '6.5.4.3.google.co.uk',
        ])

    def test_normal_fqdn_level3 (self):
        domain = 'www.google.co.uk'
        ds = publicsuffix.DomainStruct(domain)
        self.assertEqual (ds.nowww, 'google.co.uk')
        self.assertEqual (ds.eSLD, 'google')
        self.assertEqual (ds.sub, 'www')
        self.assertEqual (ds.isFQDN, True)
        self.assertListEqual(ds.eTkLD, [
            'co.uk',  # eTLD
            'google.co.uk',
            'www.google.co.uk',
        ])

    def test_normal_fqdn_level2 (self):
        domain = 'google.co.uk'
        ds = publicsuffix.DomainStruct(domain)
        self.assertEqual (ds.nowww, 'google.co.uk')
        self.assertEqual (ds.eSLD, 'google')
        self.assertEqual (ds.sub, '')
        self.assertEqual (ds.isFQDN, True)
        self.assertListEqual(ds.eTkLD, [
            'co.uk',  # eTLD
            'google.co.uk',
        ])

    def test_normal_nonfqdn (self):
        domain = 'www.user.local'
        ds = publicsuffix.DomainStruct (domain)
        self.assertEqual (ds.nowww, 'user.local')
        self.assertEqual (ds.eSLD, None)
        self.assertEqual (ds.isFQDN, False)
        self.assertListEqual(ds.eTkLD, [])


if __name__ == '__main__':
    unittest.main()
