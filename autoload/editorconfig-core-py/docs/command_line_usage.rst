==================
Command Line Usage
==================

The EditorConfig Python Core can be used from the command line in the same way
as the EditorConfig C Core.

Discovering EditorConfig properties
-----------------------------------

Installing EditorConfig Python Core should add an ``editorconfig.py`` command
to your path.  This command can be used to locate and parse EditorConfig files
for a given full filepath.  For example::

    editorconfig.py /home/zoidberg/humans/anatomy.md

When used to retrieve EditorConfig file properties, ``editorconfig.py`` will
return discovered properties in *key=value* pairs, one on each line.
