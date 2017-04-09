"""EditorConfig Python2/Python3 compatibility utilities"""
import sys

__all__ = ['force_unicode', 'u']


if sys.version_info[0] == 2:
    text_type = unicode
else:
    text_type = str


def force_unicode(string):
    if not isinstance(string, text_type):
        string = text_type(string, encoding='utf-8')
    return string


if sys.version_info[0] == 2:
    import codecs
    u = lambda s: codecs.unicode_escape_decode(s)[0]
else:
    u = lambda s: s
