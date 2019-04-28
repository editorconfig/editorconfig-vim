@echo off
:: editorconfig.bat: First-level invoker for editorconfig-core-vimscript.
:: Just passes the full command line to editorconfig1.vbs, since VBScript
:: applies very simple quoting rules when it parses a command line.
:: Copyright (c) 2018 Chris White.  CC-BY-SA 3.0+.
set here=%~dp0

cscript //Nologo "%here%editorconfig1.vbs" %*
:: %* has the whole command line
