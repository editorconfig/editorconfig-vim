===================
Handling Exceptions
===================

All exceptions raised by EditorConfig will subclass ``EditorConfigError``.  To
handle certain exceptions specially, catch them first.  More exception classes
may be added in the future so it is advisable to always handle general
``EditorConfigError`` exceptions in case a future version raises an exception
that your code does not handle specifically.

Exceptions module reference
---------------------------

Exceptions can be found in the ``editorconfig.exceptions`` module.  These are
the current exception types:

.. autoexception:: editorconfig.exceptions.EditorConfigError
.. autoexception:: editorconfig.exceptions.ParsingError
.. autoexception:: editorconfig.exceptions.PathError
.. autoexception:: editorconfig.exceptions.VersionError

Exception handling example
--------------------------

An example of custom exception handling::

    import logging
    from editorconfig import get_properties
    from editorconfig import exceptions

    filename = "/home/zoidberg/myfile.txt"

    try:
        options = get_properties(filename)
    except exceptions.ParsingError:
        logging.warning("Error parsing an .editorconfig file", exc_info=True)
    except exceptions.PathError:
        logging.error("Invalid filename specified", exc_info=True)
    except exceptions.EditorConfigError:
        logging.error("An unknown EditorConfig error occurred", exc_info=True)

    for key, value in options.iteritems():
        print "%s=%s" % (key, value)
