# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/19/2013, updated 08/21/2013
#
""" Dissecting the structure of a domain name.

    Call signatures examples:
    >>> from netu import publicsuffix  # or 'import publicsuffix'
    >>> ds = publicsuffix.DomainStruct ('mail.google.co.uk')
    >>> ds.eSLD
    'google'
    >>> ds.isFQDN
    True
    >>> ds.eTkLD
    ['co.uk', 'google.co.uk', 'mail.google.co.uk']
"""
from __future__ import absolute_import

import sys
if not (2, 6) <= sys.version_info < (3, ):
    raise ImportError("CPython 2.6.x or 2.7.x is required (%d.%d detected)."
                      % sys.version_info[:2])

from .publicsuffix import *
from .domstruct import *

del sys, absolute_import

# The first three numbers are sync'd with Tomaz' distribution.
__version__ = '1.0.4.2-a3'

