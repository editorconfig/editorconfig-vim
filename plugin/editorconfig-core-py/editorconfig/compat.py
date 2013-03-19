"""EditorConfig Python2/Python3/Jython compatibility utilities"""
import sys
import types

__all__ = ['slice', 'u']


if sys.version_info[0] == 2:
    slice = types.SliceType
else:
    slice = slice


if sys.version_info[0] == 2:
    import codecs
    u = lambda s: codecs.unicode_escape_decode(s)[0]
else:
    u = lambda s: s
