"""
Modules exported by ``editorconfig`` package:

- handler: used by plugins for locating and parsing EditorConfig files
- exceptions: provides special exceptions used by other modules
"""

from versiontools import join_version

VERSION = (0, 9, 0, "alpha")

__all__ = ['handler', 'exceptions', 'main']

__version__ = join_version(VERSION)
