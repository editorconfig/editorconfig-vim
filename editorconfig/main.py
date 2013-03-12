"""EditorConfig command line interface

Licensed under PSF License (see LICENSE.txt file).

"""

import getopt
import sys

from editorconfig import __version__, VERSION
from editorconfig.versiontools import split_version
from editorconfig.handler import EditorConfigHandler
from editorconfig.exceptions import ParsingError, PathError, VersionError


def version():
    print("Version %s" % __version__)


def usage(command, error=False):
    if error:
        out = sys.stderr
    else:
        out = sys.stdout
    print("%s [OPTIONS] FILENAME" % command, file=out)
    print('-f                 '
            'Specify conf filename other than ".editorconfig".', file=out)
    print("-b                 ",
            "Specify version (used by devs to test compatibility).", file=out)
    print("-h OR --help       Print this help message.", file=out)
    print("-v OR --version    Display version information.", file=out)


def main():
    command_name = sys.argv[0]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhb:f:", ["version", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        usage(command_name, error=True)
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
        usage(command_name, error=True)
        sys.exit(2)
    filenames = args
    multiple_files = len(args) > 1

    for filename in filenames:
        handler = EditorConfigHandler(filename, conf_filename, version_tuple)
        try:
            options = handler.get_configurations()
        except (ParsingError, PathError, VersionError) as e:
            print(str(e), file=sys.stderr)
            sys.exit(2)
        if multiple_files:
            print("[%s]" % filename)
        for key, value in options.items():
            print("%s=%s" % (key, value))
