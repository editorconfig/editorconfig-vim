"""EditorConfig exception classes

Licensed under PSF License (see LICENSE.txt file).

"""


class EditorConfigError(Exception):
    """Parent class of all exceptions raised by EditorConfig"""


try:
    from ConfigParser import ParsingError as _ParsingError
except:
    from configparser import ParsingError as _ParsingError


class ParsingError(_ParsingError, EditorConfigError):
    """Error raised if an EditorConfig file could not be parsed"""


class PathError(ValueError, EditorConfigError):
    """Error raised if invalid filepath is specified"""


class VersionError(ValueError, EditorConfigError):
    """Error raised if invalid version number is specified"""
