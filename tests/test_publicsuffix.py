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


class Test_get_public_suffix (unittest.TestCase):
    """
    """
    def setUp (self):
        """
        """
        pass

    def test_basic (self):
        """
        """
        for d in [
            '3ld.google.com',
            '4ld.3ld.google.com',
            '5ld.4ld.3ld.google.com',
        ]:
            self.assertEqual('google.com',
                publicsuffix.get_public_suffix(d))

    def test_wildcard (self):
        """
            In the effective_tld_names file, some TLDs have only one rule and
            it is wildcard, e.g.

            // bd : http://en.wikipedia.org/wiki/.bd
            *.bd
            // et : http://en.wikipedia.org/wiki/.et
            *.et

            But some TLDs
            // eu : http://en.wikipedia.org/wiki/.eu
            eu

        """
        pass


    def test_publicsuffix_org_list_test_original (self):
        """ Test cases provided by
            http://mxr.mozilla.org/mozilla-central/source/netwerk/test/unit/data/test_psl.txt?raw=1

            Note that Tomaz's version (till v1.0.4)
        """

        def checkPublicSuffix(a, b):
            self.assertEqual(publicsuffix.get_public_suffix(a), b)

        # Mixed case.
        checkPublicSuffix('COM', 'com');
        checkPublicSuffix('example.COM', 'example.com');
        checkPublicSuffix('WwW.example.COM', 'example.com');
        # Leading dot.
        checkPublicSuffix('.com', 'com');
        checkPublicSuffix('.example', 'example');
        checkPublicSuffix('.example.com', 'example.com');
        checkPublicSuffix('.example.example', 'example');
        # Unlisted TLD.
        checkPublicSuffix('example', 'example');
        checkPublicSuffix('example.example', 'example');
        checkPublicSuffix('b.example.example', 'example');
        checkPublicSuffix('a.b.example.example', 'example');
        # Listed, but non-Internet, TLD.
        checkPublicSuffix('local', 'local');
        checkPublicSuffix('example.local', 'local');
        checkPublicSuffix('b.example.local', 'local');
        checkPublicSuffix('a.b.example.local', 'local');
        # TLD with only 1 rule.
        checkPublicSuffix('biz', 'biz');
        checkPublicSuffix('domain.biz', 'domain.biz');
        checkPublicSuffix('b.domain.biz', 'domain.biz');
        checkPublicSuffix('a.b.domain.biz', 'domain.biz');
        # TLD with some 2-level rules.
        checkPublicSuffix('com', 'com');
        checkPublicSuffix('example.com', 'example.com');
        checkPublicSuffix('b.example.com', 'example.com');
        checkPublicSuffix('a.b.example.com', 'example.com');
        checkPublicSuffix('uk.com', 'uk.com');
        checkPublicSuffix('example.uk.com', 'example.uk.com');
        checkPublicSuffix('b.example.uk.com', 'example.uk.com');
        checkPublicSuffix('a.b.example.uk.com', 'example.uk.com');
        checkPublicSuffix('test.ac', 'test.ac');
        # TLD with only 1 (wildcard) rule.
        checkPublicSuffix('cy', 'cy');
        checkPublicSuffix('c.cy', 'c.cy');
        checkPublicSuffix('b.c.cy', 'b.c.cy');
        checkPublicSuffix('a.b.c.cy', 'b.c.cy');
        # More complex TLD.
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
        # TLD with a wildcard rule and exceptions.
        checkPublicSuffix('om', 'om');
        checkPublicSuffix('test.om', 'test.om');
        checkPublicSuffix('b.test.om', 'b.test.om');
        checkPublicSuffix('a.b.test.om', 'b.test.om');
        checkPublicSuffix('songfest.om', 'songfest.om');
        checkPublicSuffix('www.songfest.om', 'songfest.om');
        # US K12.
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
