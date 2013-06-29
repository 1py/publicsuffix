#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Updated 06/28/2013
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Copyright (c) 2011 Tomaz Solc <tomaz.solc@tablix.org>
# Copyright (C) 2011 Rob Stradling of Comodo
#
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
#
""" Unit tests for publicsuffix.py
"""
print('Executing %s' %  __file__)

import unittest
import os, sys, time

from netutils import publicsuffix
#import publicsuffix

class Test_get_public_suffix (unittest.TestCase):
    """ Test the main publicsuffix.get_public_suffix() interface.
    """
    def test_basic (self):
        for d in [
            '3ld.google.com',
            '4ld.3ld.google.com',
            '5ld.4ld.3ld.google.com',
        ]:
            self.assertEqual('google.com',
                publicsuffix.get_public_suffix(d))


    # The following test cases are originally from
    # http://mxr.mozilla.org/mozilla-central/source/netwerk/test/unit/data/test_psl.txt?raw=1
    # and adapted by Tomaz Solc

    def _checkPublicSuffix(self, a, b):
        self.assertEqual(publicsuffix.get_public_suffix(a), b)

    def test_mixed_case (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('COM', 'com');
        checkPublicSuffix('example.COM', 'example.com');
        checkPublicSuffix('WwW.example.COM', 'example.com');

    def test_leading_dot (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('.com', 'com');
        checkPublicSuffix('.example', 'example');
        checkPublicSuffix('.example.com', 'example.com');
        checkPublicSuffix('.example.example', 'example');

    def test_unlisted_tld (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('example', 'example');
        checkPublicSuffix('example.example', 'example');
        checkPublicSuffix('b.example.example', 'example');
        checkPublicSuffix('a.b.example.example', 'example');

    def test_listed_but_non_internet_tld (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('local', 'local');
        checkPublicSuffix('example.local', 'local');
        checkPublicSuffix('b.example.local', 'local');
        checkPublicSuffix('a.b.example.local', 'local');

    def test_tld_with_only_1_rule (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('biz', 'biz');
        checkPublicSuffix('domain.biz', 'domain.biz');
        checkPublicSuffix('b.domain.biz', 'domain.biz');
        checkPublicSuffix('a.b.domain.biz', 'domain.biz');

    def test_tld_with_some_2_level_rules (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('com', 'com');
        checkPublicSuffix('example.com', 'example.com');
        checkPublicSuffix('b.example.com', 'example.com');
        checkPublicSuffix('a.b.example.com', 'example.com');
        checkPublicSuffix('uk.com', 'uk.com');
        checkPublicSuffix('example.uk.com', 'example.uk.com');
        checkPublicSuffix('b.example.uk.com', 'example.uk.com');
        checkPublicSuffix('a.b.example.uk.com', 'example.uk.com');
        checkPublicSuffix('test.ac', 'test.ac');

    def test_tld_with_only_1_wildcard_rule (self):
        """ For example,
            // bd : http://en.wikipedia.org/wiki/.bd
            *.bd

            To be distinguished from
            // eu : http://en.wikipedia.org/wiki/.eu
            eu

            It seems that the effective_tld_names list has a bug on this.
            If there is a wildcard rule '*.bd', there should also be a rule
            'bd', or other exception rules.
        """
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('cy', 'cy');
        checkPublicSuffix('c.cy', 'c.cy');
        checkPublicSuffix('b.c.cy', 'b.c.cy');
        checkPublicSuffix('a.b.c.cy', 'b.c.cy');
        # These may seem counter-intuitive. No body believes that '2011.il' is
        # a valid TLD.
        checkPublicSuffix('www.2011.il', 'www.2011.il')
        checkPublicSuffix('www.aabop-ziiy.kw', 'www.aabop-ziiy.kw')

    def test_tld_with_wildcard_rule_and_exceptions (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('om', 'om');
        checkPublicSuffix('test.om', 'test.om');
        checkPublicSuffix('b.test.om', 'b.test.om');
        checkPublicSuffix('a.b.test.om', 'b.test.om');
        checkPublicSuffix('songfest.om', 'songfest.om');
        checkPublicSuffix('www.songfest.om', 'songfest.om');

    def test_more_complex_tld (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('jp', 'jp');
        checkPublicSuffix('test.jp', 'test.jp');
        checkPublicSuffix('www.test.jp', 'test.jp');
        checkPublicSuffix('ac.jp', 'ac.jp');
        checkPublicSuffix('test.ac.jp', 'test.ac.jp');
        checkPublicSuffix('www.test.ac.jp', 'test.ac.jp');
        checkPublicSuffix('kobe.jp', 'kobe.jp');
        checkPublicSuffix('c.kobe.jp', 'c.kobe.jp');
        checkPublicSuffix('b.c.kobe.jp', 'b.c.kobe.jp');
        checkPublicSuffix('a.b.c.kobe.jp', 'b.c.kobe.jp');
        checkPublicSuffix('city.kobe.jp', 'city.kobe.jp');	# Exception rule.
        checkPublicSuffix('www.city.kobe.jp', 'city.kobe.jp');	# Exception rule.

    def test_us_k12_tld (self):
        checkPublicSuffix = self._checkPublicSuffix
        checkPublicSuffix('us', 'us');
        checkPublicSuffix('test.us', 'test.us');
        checkPublicSuffix('www.test.us', 'test.us');
        checkPublicSuffix('ak.us', 'ak.us');
        checkPublicSuffix('test.ak.us', 'test.ak.us');
        checkPublicSuffix('www.test.ak.us', 'test.ak.us');
        checkPublicSuffix('k12.ak.us', 'k12.ak.us');
        checkPublicSuffix('test.k12.ak.us', 'test.k12.ak.us');
        checkPublicSuffix('www.test.k12.ak.us', 'test.k12.ak.us');


if __name__ == '__main__':
    unittest.main()
