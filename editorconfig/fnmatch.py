"""Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)

Based on code from fnmatch.py file distributed with Python 2.6.

Licensed under PSF License (see LICENSE.txt file).

Changes to original fnmatch module:
- translate function supports ``*`` and ``**`` similarly to fnmatch C library
"""

import os
import re

__all__ = ["fnmatch", "fnmatchcase", "translate"]

_cache = {}

_brace1 = re.compile(r'(?:^|[^\\])\{')
_brace2 = re.compile(r'(?:^|[^\\])\}')


def fnmatch(name, pat):
    """Test whether FILENAME matches PATTERN.

    Patterns are Unix shell style:

    - ``*``             matches everything except path separator
    - ``**``            matches everything
    - ``?``             matches any single character
    - ``[seq]``         matches any character in seq
    - ``[!seq]``        matches any char not in seq
    - ``{s1,s2,s3}``    matches any of the strings given (separated by commas)

    An initial period in FILENAME is not special.
    Both FILENAME and PATTERN are first case-normalized
    if the operating system requires it.
    If you don't want this, use fnmatchcase(FILENAME, PATTERN).
    """

    name = os.path.normpath(name).replace(os.sep, "/")
    return fnmatchcase(name, pat)


def fnmatchcase(name, pat):
    """Test whether FILENAME matches PATTERN, including case.

    This is a version of fnmatch() which doesn't case-normalize
    its arguments.
    """

    if not pat in _cache:
        res = translate(pat)
        _cache[pat] = re.compile(res)
    return _cache[pat].match(name) is not None


def translate(pat, nested=False):
    """Translate a shell PATTERN to a regular expression.

    There is no way to quote meta-characters.
    """

    i, n = 0, len(pat)
    brace_level = 0
    res = ''
    escaped = False
    matching_braces = len(_brace1.findall(pat)) == len(_brace2.findall(pat))
    while i < n:
        c = pat[i]
        i = i + 1
        if c == '*':
            j = i
            if j < n and pat[j] == '*':
                res = res + '.*'
            else:
                res = res + '[^/]*'
        elif c == '?':
            res = res + '.'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j + 1
            if j < n and pat[j] == ']':
                j = j + 1
            while j < n and (pat[j] != ']' or escaped):
                escaped = pat[j] == '\\' and not escaped
                j = j + 1
            if j >= n:
                res += res + '\\['
            else:
                stuff = pat[i:j]
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        elif c == '{':
            j = i
            has_comma = False
            while j < n and (pat[j] != '}' or escaped):
                if pat[j] == ',' and not escaped:
                    has_comma = True
                    break
                escaped = pat[j] == '\\' and not escaped
                j = j + 1
            if not has_comma and j < n:
                res = '%s\\{%s\\}' % (res, translate(pat[i:j], nested=True))
                i = j + 1
            elif matching_braces:
                res = res + '(?:'
                brace_level += 1
            else:
                res = res + '\\{'
        elif c == ',':
            if brace_level > 0 and not escaped:
                res = res + '|'
            else:
                res = res + '\\,'
        elif c == '}':
            if brace_level > 0 and not escaped:
                res = res + ')'
                brace_level -= 1
            else:
                res = res + '\\}'
        elif c != '\\':
            res = res + re.escape(c)
        if c == '\\':
            if escaped:
                res = res + re.escape(c)
            escaped = not escaped
        else:
            escaped = False
    if nested:
        return res
    else:
        return res + '\Z(?ms)'
