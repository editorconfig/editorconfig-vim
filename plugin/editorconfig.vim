" Copyright (c) 2011-2012 EditorConfig Team
" All rights reserved.
" 
" Redistribution and use in source and binary forms, with or without
" modification, are permitted provided that the following conditions are met:
" 
" 1. Redistributions of source code must retain the above copyright notice,
"    this list of conditions and the following disclaimer.
" 2. Redistributions in binary form must reproduce the above copyright notice,
"    this list of conditions and the following disclaimer in the documentation
"    and/or other materials provided with the distribution.
" 
" THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
" IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
" ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
" LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
" CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
" SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
" INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
" CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
" ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
" POSSIBILITY OF SUCH DAMAGE.
"

if v:version < 700
    finish
endif

" check whether this script is already loaded
if exists("g:loaded_EditorConfig")
    finish
endif
let g:loaded_EditorConfig = 1

if !exists('g:EditorConfig_exec_path')
    let g:EditorConfig_exec_path = ''
endif

if !exists('g:EditorConfig_python_files')
    let g:EditorConfig_python_files_dir = 'plugin/editorconfig-core-py'
endif

let s:saved_cpo = &cpo
set cpo&vim

augroup editorconfig
autocmd! editorconfig
autocmd editorconfig BufNewFile,BufReadPost * call s:UseConfigFiles()
autocmd editorconfig BufNewFile,BufRead .editorconfig set filetype=dosini

command! EditorConfigReload call s:UseConfigFiles() " Reload EditorConfig files

" Find python interp. If found, return python command; if not found, return ''
function! s:FindPythonInterp()
    if has('unix')
        let l:searching_list = [
                    \ 'python',
                    \ 'python27',
                    \ 'python26',
                    \ 'python25',
                    \ 'python24',
                    \ '/usr/local/bin/python',
                    \ '/usr/local/bin/python27',
                    \ '/usr/local/bin/python26',
                    \ '/usr/local/bin/python25',
                    \ '/usr/local/bin/python24',
                    \ '/usr/bin/python',
                    \ '/usr/bin/python27',
                    \ '/usr/bin/python26',
                    \ '/usr/bin/python25',
                    \ '/usr/bin/python24']
    elseif has('win32')
        let l:searching_list = [
                    \ 'python',
                    \ 'python27',
                    \ 'python26',
                    \ 'python25',
                    \ 'python24',
                    \ 'C:\Python27\python.exe',
                    \ 'C:\Python26\python.exe',
                    \ 'C:\Python25\python.exe',
                    \ 'C:\Python24\python.exe']
    endif

    for possible_python_interp in l:searching_list
        if executable(possible_python_interp)
            return possible_python_interp
        endif
    endfor

    return ''
endfunction

" Find EditorConfig Core python files
function! s:FindPythonFiles()
    return substitute(
                \ findfile(g:EditorConfig_python_files_dir . '/main.py',
                \ ','.&runtimepath), '/main.py$', '', '')
endfunction

let s:editorconfig_core_mode = ''

" If python is built-in with vim and python scripts are found, python core
" would be used
while 1

    " If user has specified a mode, just break
    if exists('g:editorconfig_core_mode') && !empty(g:editorconfig_core_mode)
        let s:editorconfig_core_mode = g:editorconfig_core_mode
        break
    endif

    " Find python files. If not found, we use C mode
    let s:editorconfig_core_py_dir = s:FindPythonFiles()
    if empty(s:editorconfig_core_py_dir) " python files are not found
        let s:editorconfig_core_mode = 'c'
        break
    endif

    " Check whether built-in python could be found. If not, we need to look
    " for external python interp. If the external interp is not found, use C
    " mode.
    if !has('python')

        if !exists('g:editorconfig_python_interp') ||
                    \ empty('g:editorconfig_python_interp')
            let g:editorconfig_python_interp = s:FindPythonInterp()
        endif

        if empty(g:editorconfig_python_interp) " Use C
            let s:editorconfig_core_mode = 'c'
        else
            let s:editorconfig_core_mode = 'python_external'
        endif

        break
    endif

    python << EEOOFF

try:
    import vim
    import sys
except:
    vim.command('let s:editorconfig_core_mode = "c"')

EEOOFF

    if !empty(s:editorconfig_core_mode)
        break
    endif

    python << EEOOFF

sys.path.insert(0, vim.eval('s:editorconfig_core_py_dir'))

try:
    from editorconfig.handler import EditorConfigHandler
    from editorconfig.exceptions import (ParsingError, PathError,
            VersionError)
except:
    vim.command('let s:editorconfig_core_mode = "c"')

del sys.path[0] 

EEOOFF

    if !empty(s:editorconfig_core_mode)
        break
    endif

    let s:editorconfig_core_mode = 'python_builtin'
    break
endwhile

function! s:UseConfigFiles()
    if s:editorconfig_core_mode == 'c'
        call s:UseConfigFiles_C()
    elseif s:editorconfig_core_mode == 'python_builtin'
        call s:UseConfigFiles_Python_Builtin()
    elseif s:editorconfig_core_mode == 'python_external'
        call s:UseConfigFiles_Python_External()
    else
        echohl Error |
                    \ echo "Unknown EditorConfig Core: " .
                    \ s:editorconfig_core_mode |
                    \ echohl None
    endif
endfunction

" Use built-in python to run the python EditorConfig core
function! s:UseConfigFiles_Python_Builtin()

    let l:config = {}
    let l:ret = 0

    python << EEOOFF

filename = vim.eval("expand('%:p')")
conf_file = ".editorconfig"
handler = EditorConfigHandler(filename, conf_file)

try:
    handler.get_configurations()
except (PathError, ParsingError, VersionError) as e:
    print >> sys.stderr, str(e)
    vim.command('let l:ret = 1')

EEOOFF
    if l:ret != 0
        return l:ret
    endif

    python << EEOOFF
for key, value in handler.options.items():
    vim.command('let l:config[' + repr(key) + '] = ' + repr(value))

EEOOFF

    call s:ApplyConfig(l:config)

    return 0
endfunction

" Use external python interp to run the the python EditorConfig Core
function! s:UseConfigFiles_Python_External()

    " Find Python Files
    if !exists('s:editorconfig_core_py_dir') ||
                \ empty('s:editorconfig_core_py_dir')
        let s:editorconfig_core_py_dir = s:FindPythonFiles()
    endif

    if empty(s:editorconfig_core_py_dir)
        return 1
    endif

    " Find python interp 
    if !exists('g:editorconfig_python_interp') ||
                \ empty('g:editorconfig_python_interp')
        let g:editorconfig_python_interp = s:FindPythonInterp()
    endif

    if empty(g:editorconfig_python_interp)
        return 2
    endif

    let l:cmd = g:editorconfig_python_interp . ' ' .
                \ s:editorconfig_core_py_dir . '/main.py'

    call s:SpawnExternalParser(l:cmd)

    return 0
endfunction

" Use external EditorConfig core (The C core, or external python interp)
function! s:UseConfigFiles_C()

    let l:cmd = ''

    if has('unix')
        let l:searching_list = [
                    \ g:EditorConfig_exec_path,
                    \ 'editorconfig',
                    \ '/usr/local/bin/editorconfig',
                    \ '/usr/bin/editorconfig',
                    \ '/opt/bin/editorconfig',
                    \ '/opt/editorconfig/bin/editorconfig']
    elseif has('win32')
        let l:searching_list = [
                    \ g:EditorConfig_exec_path,
                    \ 'editorconfig',
                    \ 'C:\editorconfig\bin\editorconfig',
                    \ 'D:\editorconfig\bin\editorconfig',
                    \ 'E:\editorconfig\bin\editorconfig',
                    \ 'F:\editorconfig\bin\editorconfig',
                    \ 'C:\Program Files\editorconfig\bin\editorconfig',
                    \ 'D:\Program Files\editorconfig\bin\editorconfig',
                    \ 'E:\Program Files\editorconfig\bin\editorconfig',
                    \ 'F:\Program Files\editorconfig\bin\editorconfig']
    endif

    " search for editorconfig core
    for possible_cmd in l:searching_list
        if executable(possible_cmd)
            let l:cmd = possible_cmd
            " let g:EditorConfig_exec_path as the command thus we could save
            " time to find the EditorConfig core next time
            let g:EditorConfig_exec_path = l:cmd
            break
        endif
    endfor

    call s:SpawnExternalParser(l:cmd)
endfunction

function! s:SpawnExternalParser(cmd) " Spawn external EditorConfig

    let l:cmd = a:cmd

    " if editorconfig is present, we use this as our parser
    if !empty(l:cmd)
        let l:config = {}

        let l:cmd = l:cmd . ' ' . shellescape(expand('%:p'))
        let l:parsing_result = split(system(l:cmd), '\n')

        " if editorconfig core's exit code is not zero, give out an error
        " message
        if v:shell_error != 0
            echohl ErrorMsg
            echo 'Failed to execute "' . l:cmd . '"'
            echohl None
            return
        endif

        for one_line in l:parsing_result
            let l:eq_pos = stridx(one_line, '=')

            if l:eq_pos == -1 " = is not found. Skip this line
                continue
            endif

            let l:eq_left = strpart(one_line, 0, l:eq_pos)
            if l:eq_pos + 1 < strlen(one_line)
                let l:eq_right = strpart(one_line, l:eq_pos + 1)
            else
                let l:eq_right = ''
            endif

            let l:config[l:eq_left] = l:eq_right
        endfor

        call s:ApplyConfig(l:config)
    endif
endfunction

" Set the indentation style according to the config values
function! s:ApplyConfig(config)
    if has_key(a:config, "indent_style")
        if a:config["indent_style"] == "tab"
            setl noexpandtab
        elseif a:config["indent_style"] == "space"
            setl expandtab
        endif
    endif
    if has_key(a:config, "tab_width")
        let &l:tabstop = str2nr(a:config["tab_width"])
    endif
    if has_key(a:config, "indent_size")

        " if indent_size is 'tab', set shiftwidth to tabstop;
        " if indent_size is a positive integer, set shiftwidth to the integer
        " value
        if a:config["indent_size"] == "tab"
            let &l:shiftwidth = &l:tabstop
            let &l:softtabstop = &l:shiftwidth
        else
            let l:indent_size = str2nr(a:config["indent_size"])
            if l:indent_size > 0
                let &l:shiftwidth = l:indent_size
                let &l:softtabstop = &l:shiftwidth
            endif
        endif

    endif

    if has_key(a:config, "end_of_line")
        if a:config["end_of_line"] == "lf"
            setl fileformat=unix
        elseif a:config["end_of_line"] == "crlf"
            setl fileformat=dos
        elseif a:config["end_of_line"] == "cr"
            setl fileformat=mac
        endif
    endif
endfunction

let &cpo = s:saved_cpo
unlet! s:saved_cpo

