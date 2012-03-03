"""EditorConfig file parser

Based on code from ConfigParser.py file distributed with Python 2.6.

Licensed under PSF License (see PYTHON_LICENSE.txt file).
"""

import re
from ConfigParser import SafeConfigParser, DEFAULTSECT

from odict import OrderedDict

__all__ = ["EditorConfigParser"]


class EditorConfigParser(SafeConfigParser):
    """Parser for EditorConfig-style configuration files"""

    # Allow ] and escaped ; and # characters in section headers
    SECTCRE = re.compile(
        r'\['
        r'(?P<header>([^#;]|\\#|\\;)+)'
        r'\]'
        )

    # Use empty section name for initial section
    def __init__(self, *args, **kwargs):
        SafeConfigParser.__init__(self, *args, **kwargs)
        if '' not in self._sections:
            self._sections[''] = self._dict()

    def _read(self, fp, fpname):
        """Parse a sectioned EditorConfig file."""
        cursect = self._sections['']              # Current section
        optname = None
        lineno = 0
        e = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue
            if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
                # no leading whitespace
                continue
            # continuation line?
            if line[0].isspace() and cursect is not None and optname:
                value = line.strip()
                if value:
                    cursect[optname] = "%s\n%s" % (cursect[optname], value)
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                    elif sectname == DEFAULTSECT:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        cursect['__name__'] = sectname
                        self._sections[sectname] = cursect
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
                        cursect[optname] = optval
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

