===============
Writing Plugins
===============

The EditorConfig Python Core can be easily used by text editor plugins written in Python or plugins that can call an external Python interpreter.  The EditorConfig Python Core supports Python versions 2.2 to 2.7.  Check out the `Vim`_ and `Gedit`_ plugins for example usages of the EditorConfig Python Core.

.. _`Vim`: https://github.com/editorconfig/editorconfig-vim
.. _`Gedit`: https://github.com/editorconfig/editorconfig-gedit


Use as a library
----------------

For instructions on using the EditorConfig Python Core as a Python library see :doc:`usage`.


Using with an external Python interpreter
-----------------------------------------

The EditorConfig Python Core can be used with an external Python interpreter by executing the ``main.py`` file.  The ``main.py`` file can be executed like so::

    python editorconfig-core-py/main.py /home/zoidberg/humans/anatomy.md

For more information on command line usage of the EditorConfig Python Core see :doc:`command_line_usage`.


Bundling EditorConfig Python Core with Plugin
---------------------------------------------

A text editor or IDE plugin will either need to bundle the EditorConfig Python
Core with the plugin installation package or the will need to assist the user
in installing the EditorConfig Python Core.  Below are instructions for
bundling the EditorConfig Python Core with plugins.

Bundling as a Submodule in Git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Git submodules allow one repository to be included inside another.  A submodule
stores a remote repositry and commit to use for fetching the embedded
repository.  Submodules take up very little space in the repository since they
do not actually include the code of the embedded repository directly.

To add EditorConfig Python Core as a submodule in the ``editorconfig-core-py``
directory of your repository::

    git submodule add git://github.com/editorconfig/editorconfig-core-py.git editorconfig-core-py

Then every time the code is checked out the submodule directory should be
initialized and updated::

    git submodule update --init

Bundling as a Subtree in Git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Git subtrees are convenient because, unlike submodules, they do not require any
extra work to be performed when cloning the git repository.  Git subtrees
include one git codebase as a subdirectory of another.

Example of using a subtree for the ``editorconfig`` directory from the
EditorConfig Python Core repository::

    git remote add -f editorconfig-core-py git://github.com/editorconfig/editorconfig-core-py.git
    git merge -s ours --no-commit editorconfig-core-py/master
    git read-tree --prefix=editorconfig -u editorconfig-core-py/master:editorconfig
    git commit

For more information on subtrees consult the `subtree merge guide`_ on Github
and `Chapter 6.7`_ in the book Pro Git.

.. _`subtree merge guide`: http://help.github.com/subtree-merge/
.. _`Chapter 6.7`: http://git-scm.com/book/ch6-7.html
