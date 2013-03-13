"""EditorConfig Python2/3 compatibility tools"""
import sys

__all__ = ['u']


if sys.version_info[0] == 2:
    import codecs
    u = lambda s: codecs.unicode_escape_decode(s)[0]
else:
    u = lambda s: s
