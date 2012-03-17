VERSION = (0, 9, 0, "alpha")

def get_version():
    version = "%s.%s.%s" % VERSION[:3]
    if VERSION[3] != "final":
        version += ".%s" % VERSION[3]
    return version

__version__ = get_version()
