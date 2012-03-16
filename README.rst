========================
EditorConfig Python Core
========================

EditorConfig Python Core provides the same functionality as the
`EditorConfig C Core <https://github.com/editorconfig/editorconfig-core>`_. 
EditorConfig Python core can be used as a command line program or as an
importable library.

Installation
============

With setuptools:

    sudo python setup.py install

Getting Help
============
For help with the EditorConfig core code, please write to our `mailing list <http://groups.google.com/group/editorconfig>`_.

If you are writing a plugin a language that can import Python libraries, you may want to import and use the EditorConfig Python Core directly.

Using as a Library
==================

Example use of EditorConfig Python Core as a library:

    filename = "/home/zoidberg/myfile.txt"
    conf_file = ".editorconfig"
    handler = EditorConfigHandler(filename, conf_filename)
    options = handler.get_configurations()
    for key, value in options.items():
        print "%s=%s" % (key, value)

License
=======

Unless otherwise stated, all files are distributed under the PSF license.  The odict library (editorconfig/odict.py) is distributed under the New BSD license.  See LICENSE.txt file for details on PSF license.
