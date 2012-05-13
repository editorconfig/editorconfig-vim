"""
Modules exported by ``editorconfig`` package:

- handler: used by plugins for locating and parsing EditorConfig files
- exceptions: provides special exceptions used by other modules
"""

from versiontools import join_version

VERSION = (0, 9, 0, "final")

__all__ = ['get_properties', 'EditorConfigError', 'handler', 'exceptions']

__version__ = join_version(VERSION)


def get_properties(filename):
    handler = EditorConfigHandler(filename)
    return handler.get_configurations()


from handler import EditorConfigHandler
from exceptions import *
