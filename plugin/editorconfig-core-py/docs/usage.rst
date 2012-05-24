=====
Usage
=====

First you will need to install the EditorConfig Python Core package.

To install from PyPI using pip::

    pip install editorconfig

Discovering EditorConfig properties
-----------------------------------

The ``get_properties`` function can be used to discover EditorConfig properties
for a given file.  Example::

    import logging
    from editorconfig import get_properties, EditorConfigError

    filename = "/home/zoidberg/humans/anatomy.md"

    try:
        options = get_properties(filename)
    except EditorConfigError:
        logger.warning("Error getting EditorConfig properties", exc_info=True)
    else:
        for key, value in options.items():
            print "%s=%s" % (key, value)


The ``get_properties`` method returns a dictionary representing EditorConfig
properties found for the given file.  If an error occurs while parsing a file
an exception will be raised.  All raised exceptions will inherit from the
``EditorConfigError`` class.
