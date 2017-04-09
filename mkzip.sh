#!/bin/sh

zip -r editorconfig-vim-$*.zip plugin/editorconfig.vim autoload/editorconfig.py autoload/editorconfig-core-py/* doc/editorconfig.txt autoload/*.vim
