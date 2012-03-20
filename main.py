#!/usr/bin/env python

import getopt, sys

from editorconfig import __version__, VERSION
from editorconfig.versiontools import split_version
from editorconfig.handler import EditorConfigHandler


def version():
    print "Version %s" % __version__


def usage(command):
    print "%s [OPTIONS] FILENAME" % command
    print '-f                 Specify conf filename other than ".editorconfig".'
    print "-b                 Specify version (used by devs to test compatibility)."
    print "-h OR --help       Print this help message."
    print "--version          Display version information."


def main():
    command_name = sys.argv[0]
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "vhb:f:", ["version", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage(command_name)
        sys.exit(2)
    if len(args) > 1:
        usage(command_name)
        sys.exit(2)

    version_tuple = VERSION
    conf_filename = '.editorconfig'

    for option, arg in opts:
        if option in ('-h', '--help'):
            usage(command_name)
            sys.exit()
        if option in ('-v', '--version'):
            version()
            sys.exit()
        if option == '-f':
            conf_filename = arg
        if option == '-b':
            version_tuple = split_version(arg)
            if version_tuple is None:
                sys.exit("Invalid version number: %s" % arg)

    if len(args) < 1:
        usage(command_name)
        sys.exit(2)
    filename = args[0]

    handler = EditorConfigHandler(filename, conf_filename, version_tuple)
    options = handler.get_configurations()
    for key, value in options.items():
        print "%s=%s" % (key, value)


if __name__ == "__main__":
    main()
