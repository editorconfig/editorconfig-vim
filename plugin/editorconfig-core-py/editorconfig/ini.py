"""EditorConfig file parser

Based on code from ConfigParser.py file distributed with Python 2.6.

Licensed under PSF License (see LICENSE.txt file).

Changes to original ConfigParser:

- Special characters can be used in section names
- Octothorpe can be used for comments (not just at beginning of line)
- Only track INI options in sections that match target filename
- Stop parsing files with when ``root = true`` is found

"""

import re
from codecs import open
import posixpath
from os import sep
from os.path import normcase, dirname

from editorconfig.exceptions import ParsingError
from editorconfig.fnmatch import fnmatch
from editorconfig.odict import OrderedDict
from editorconfig.compat import u


__all__ = ["ParsingError", "EditorConfigParser"]


class EditorConfigParser(object):

    """Parser for EditorConfig-style configuration files

    Based on RawConfigParser from ConfigParser.py in Python 2.6.
    """

    # Regular expressions for parsing section headers and options.
    # Allow ``]`` and escaped ``;`` and ``#`` characters in section headers
    SECTCRE = re.compile(
        r'\s*\['                              # [
        r'(?P<header>([^#;]|\\#|\\;)+)'       # very permissive!
        r'\]'                                 # ]
        )
    # Regular expression for parsing option name/values.
    # Allow any amount of whitespaces, followed by separator
    # (either ``:`` or ``=``), followed by any amount of whitespace and then
    # any characters to eol
    OPTCRE = re.compile(
        r'\s*(?P<option>[^:=\s][^:=]*)'
        r'\s*(?P<vi>[:=])\s*'
        r'(?P<value>.*)$'
        )

    def __init__(self, filename):
        self.filename = filename
        self.options = OrderedDict()
        self.root_file = False

    def matches_filename(self, config_filename, glob):
        """Return True if section glob matches filename"""
        config_dirname = normcase(dirname(config_filename)).replace(sep, '/')
        glob = glob.replace("\\#", "#")
        glob = glob.replace("\\;", ";")
        if '/' in glob:
            if glob.find('/') == 0:
                glob = glob[1:]
            glob = posixpath.join(config_dirname, glob)
        else:
            glob = posixpath.join('**/', glob)
        return fnmatch(self.filename, glob)

    def read(self, filename):
        """Read and parse single EditorConfig file"""
        try:
            fp = open(filename, encoding='utf-8')
        except IOError:
            return
        self._read(fp, filename)
        fp.close()

    def _read(self, fp, fpname):
        """Parse a sectioned setup file.

        The sections in setup file contains a title line at the top,
        indicated by a name in square brackets (`[]'), plus key/value
        options lines, indicated by `name: value' format lines.
        Continuations are represented by an embedded newline then
        leading whitespace.  Blank lines, lines beginning with a '#',
        and just about everything else are ignored.
        """
        in_section = False
        matching_section = False
        optname = None
        lineno = 0
        e = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            if lineno == 0 and line.startswith(u('\ufeff')):
                line = line[1:]  # Strip UTF-8 BOM
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    in_section = True
                    matching_section = self.matches_filename(fpname, sectname)
                    # So sections can't start with a continuation line
                    optname = None
                # an option line?
                else:
                    mo = self.OPTCRE.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if ';' in optval or '#' in optval:
                            # ';' and '#' are comment delimiters only if
                            # preceeded by a spacing character
                            m = re.search('(.*?) [;#]', optval)
                            if m:
                                optval = m.group(1)
                        optval = optval.strip()
                        # allow empty values
                        if optval == '""':
                            optval = ''
                        optname = self.optionxform(optname.rstrip())
                        if not in_section and optname == 'root':
                            self.root_file = (optval.lower() == 'true')
                        if matching_section:
                            self.options[optname] = optval
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = ParsingError(fpname)
                        e.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if e:
            raise e

    def optionxform(self, optionstr):
        return optionstr.lower()
