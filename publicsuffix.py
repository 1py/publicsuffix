#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Updated 06/28/2013
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Copyright (c) 2011 Tomaz Solc <tomaz.solc@tablix.org>
# Copyright (c) 2009 David Wilson
## Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# The Public Suffix List included in this distribution has been downloaded
# from http://publicsuffix.org/ and is covered by a separate license. Please
# see the license block at the top of the file itself.

""" Public Suffix List module for Python.
"""

__all__ = [
    'get_public_suffix',
]

import codecs
import os.path


#-----------------------------------------------------------------------------
# Parses and parses the public suffix list, and build the search tree
#-----------------------------------------------------------------------------

# Search tree
Root = [0]

# Cache the lookup results at the module level (for current process)
Domain_to_t2ld_cache = {}


def _find_node (parent, parts):

    if not parts:
        return parent

    if len(parent) == 1:
        parent.append({})

    assert len(parent) == 2
    negate, children = parent

    child = parts.pop()

    child_node = children.get(child, None)

    if not child_node:
        children[child] = child_node = [0]

    return _find_node(child_node, parts)


def _add_rule (root, rule):

    if rule.startswith('!'):
        negate = 1
        rule = rule[1:]
    else:
        negate = 0

    parts = rule.split('.')
    _find_node(root, parts)[0] = negate


PATH_DATA = os.path.join(os.path.dirname(__file__), '@data')

# The file format is described at http://publicsuffix.org/list/
TLD_FNAME = os.path.join(PATH_DATA, 'effective_tld_names.txt')

with codecs.open(TLD_FNAME, 'r', 'utf8') as fr:

    for line in fr:
        line = line.strip()
        if line.startswith('//') or not line:
            continue

        _add_rule (Root, line.split()[0].lstrip('.'))  # Root is changed


def _simplify (node):

    if len(node) == 1:
        return node[0]

    return node[0], dict((k, _simplify(v)) for k, v in node[1].items())


Root = _simplify (Root)


#-----------------------------------------------------------------------------
# Lookup functions
#-----------------------------------------------------------------------------

def _lookup_node (matches, depth, parent, parts):

    if parent in (0, 1):
        negate = parent
        children = None
    else:
        negate, children = parent

    matches[-depth] = negate
    if depth < len(parts) and children:
        for name in ('*', parts[-depth]):
            child = children.get(name, None)
            if child is not None:
                _lookup_node (matches, depth+1, child, parts)


def get_public_suffix (domain):
    """ get_public_suffix("www.example.com") -> "example.com"

    Calling this function with a DNS name will return the
    public suffix for that name.

    Note that if the input does not contain a valid TLD,
    e.g. "xxx.residential.fw" in which "fw" is not a valid TLD,
    the returned public suffix will be "fw", and TLD will be empty

    Note that for internationalized domains the list at
    http://publicsuffix.org uses decoded names, so it is
    up to the caller to decode any Punycode-encoded names.

    """
    global Root, Domain_to_t2ld_cache

    try:
        return Domain_to_t2ld_cache [domain]

    except KeyError:

        parts = domain.lower().lstrip('.').split('.')
        hits = [None] * len(parts)

        _lookup_node (hits, 1, Root, parts)

        for i, what in enumerate(hits):
            if what is not None and what == 0:
                t2ld = '.'.join(parts[i:])
                Domain_to_t2ld_cache [domain] = t2ld
                return t2ld

