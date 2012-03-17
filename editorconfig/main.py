#!/usr/bin/env python

import getopt, sys

from . import __version__
from editorconfig import EditorConfigHandler


def version():
    print "Version %s" % __version__


def usage(command):
    print "%s [OPTIONS] FILENAME" % command
    print '-f                 Specify conf filename other than ".editorconfig".'
    print "-h OR --help       Print this help message."
    print "--version          Display version information."


def main():
    command_name = sys.argv[0]
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "vhf:", ["version", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage(command_name)
        sys.exit(2)
    if len(args) > 1:
        usage(command_name)
        sys.exit(2)

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

    if len(args) < 1:
        usage(command_name)
        sys.exit(2)
    filename = args[0]

    handler = EditorConfigHandler(filename, conf_filename)
    options = handler.get_configurations()
    for key, value in options.items():
        print "%s=%s" % (key, value)


if __name__ == "__main__":
    main()
