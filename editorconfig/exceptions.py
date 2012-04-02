from ConfigParser import ParsingError as _ParsingError


class ParsingError(_ParsingError):
    """Error raised if an EditorConfig file could not be parsed"""


class PathError(ValueError):
    """Error raised if invalid filepath is specified"""


class VersionError(ValueError):
    """Error raised if invalid version number is specified"""
