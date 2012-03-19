import re


_version_re = re.compile(r'^(\d+)\.(\d+)\.(\d+)(\..*)?$', re.VERBOSE)


def join_version(version_tuple):
    version = "%s.%s.%s" % version_tuple[:3]
    if version_tuple[3] != "final":
        version += ".%s" % version_tuple[3]
    return version


def split_version(version):
    match = _version_re.search(version)
    if not match:
        return None
    else:
        split_version = list(match.groups())
        if split_version[3] is None:
            split_version[3] = "final"
        split_version = map(int, split_version[:3]) + split_version[3:]
        return tuple(split_version)
