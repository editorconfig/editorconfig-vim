" Copyright (c) 2011-2015 EditorConfig Team
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

let s:saved_cpo = &cpo
set cpo&vim

" variables {{{1
if !exists('g:EditorConfig_exec_path')
    let g:EditorConfig_exec_path = ''
endif

if !exists('g:EditorConfig_python_files_dir')
    let g:EditorConfig_python_files_dir = 'plugin/editorconfig-core-py'
endif

if !exists('g:EditorConfig_verbose')
    let g:EditorConfig_verbose = 0
endif

if !exists('g:EditorConfig_preserve_formatoptions')
    let g:EditorConfig_preserve_formatoptions = 0
endif

if !exists('g:EditorConfig_max_line_indicator')
    let g:EditorConfig_max_line_indicator = 'line'
endif

if !exists('g:EditorConfig_exclude_patterns')
    let g:EditorConfig_exclude_patterns = []
endif

if exists('g:EditorConfig_core_mode') && !empty(g:EditorConfig_core_mode)
    let s:editorconfig_core_mode = g:EditorConfig_core_mode
else
    let s:editorconfig_core_mode = ''
endif


function! s:FindPythonInterp() " {{{1
" Find python interp. If found, return python command; if not found, return ''

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

function! s:FindPythonFiles() " {{{1
" Find EditorConfig Core python files

    " On Windows, we still use slash rather than backslash
    let l:old_shellslash = &shellslash
    set shellslash

    let l:python_core_files_dir = fnamemodify(
                \ findfile(g:EditorConfig_python_files_dir . '/main.py',
                \ ','.&runtimepath), ':p:h')

    if empty(l:python_core_files_dir)
        let l:python_core_files_dir = ''
    else

    " expand python core file path to full path, and remove the appending '/'
    let l:python_core_files_dir = substitute(
                \ fnamemodify(l:python_core_files_dir, ':p'), '/$', '', '')
    endif

    let &shellslash = l:old_shellslash

    return l:python_core_files_dir
endfunction

" Mode initialization functions {{{1
function! s:InitializeExternalCommand() " {{{2
" Initialize external_command mode

    let s:EditorConfig_exec_path = ''

    " User has specified an EditorConfig command. Use that one.
    if exists('g:EditorConfig_exec_path') &&
                \ !empty(g:EditorConfig_exec_path)
        if executable(g:EditorConfig_exec_path)
            let s:EditorConfig_exec_path = g:EditorConfig_exec_path
            return 0
        else
            return 1
        endif
    endif

    " User does not specify an EditorConfig command. Let's search for it.
    if has('unix')
        let l:searching_list = [
                    \ 'editorconfig',
                    \ '/usr/local/bin/editorconfig',
                    \ '/usr/bin/editorconfig',
                    \ '/opt/bin/editorconfig',
                    \ '/opt/editorconfig/bin/editorconfig',
                    \ 'editorconfig.py',
                    \ '/usr/local/bin/editorconfig.py',
                    \ '/usr/bin/editorconfig.py',
                    \ '/opt/bin/editorconfig.py',
                    \ '/opt/editorconfig/bin/editorconfig.py']
    elseif has('win32')
        let l:searching_list = [
                    \ 'editorconfig',
                    \ 'C:\editorconfig\bin\editorconfig',
                    \ 'D:\editorconfig\bin\editorconfig',
                    \ 'E:\editorconfig\bin\editorconfig',
                    \ 'F:\editorconfig\bin\editorconfig',
                    \ 'C:\Program Files\editorconfig\bin\editorconfig',
                    \ 'D:\Program Files\editorconfig\bin\editorconfig',
                    \ 'E:\Program Files\editorconfig\bin\editorconfig',
                    \ 'F:\Program Files\editorconfig\bin\editorconfig',
                    \ 'C:\Program Files (x86)\editorconfig\bin\editorconfig',
                    \ 'D:\Program Files (x86)\editorconfig\bin\editorconfig',
                    \ 'E:\Program Files (x86)\editorconfig\bin\editorconfig',
                    \ 'F:\Program Files (x86)\editorconfig\bin\editorconfig',
                    \ 'editorconfig.py']
    endif

    " search for editorconfig core executable
    for possible_cmd in l:searching_list
        if executable(possible_cmd)
            let s:EditorConfig_exec_path = possible_cmd
            break
        endif
    endfor

    if empty(s:EditorConfig_exec_path)
        return 2
    endif

    return 0
endfunction

function! s:InitializePythonExternal() " {{{2
" Initialize external python. Before calling this function, please make sure
" s:FindPythonFiles is called and the return value is set to
" s:editorconfig_core_py_dir

    if !exists('s:editorconfig_core_py_dir') ||
                \ empty(s:editorconfig_core_py_dir)
        return 2
    endif

    " Find python interp
    if !exists('g:editorconfig_python_interp') ||
                \ empty('g:editorconfig_python_interp')
        let s:editorconfig_python_interp = s:FindPythonInterp()
    endif

    if empty(s:editorconfig_python_interp) ||
                \ !executable(s:editorconfig_python_interp)
        return 1
    endif

    return 0
endfunction

function! s:InitializePythonBuiltin(editorconfig_core_py_dir) " {{{2
" Initialize builtin python. The parameter is the Python Core directory

    if exists('s:builtin_python_initialized') && s:builtin_python_initialized
        return 0
    endif

    let s:builtin_python_initialized = 1

    let l:ret = 0

    if !has('python')
        return 1
    endif

    python << EEOOFF

try:
    import vim
    import sys
except:
    vim.command('let l:ret = 2')

EEOOFF

    if l:ret != 0
        return l:ret
    endif

    python << EEOOFF

try:
    sys.path.insert(0, vim.eval('a:editorconfig_core_py_dir'))

    import editorconfig
    import editorconfig.exceptions as editorconfig_except

except:
    vim.command('let l:ret = 3')

del sys.path[0]

ec_data = {}  # used in order to keep clean Python namespace

EEOOFF

    if l:ret != 0
        return l:ret
    endif

    return 0
endfunction

" Do some initalization for the case that the user has specified core mode {{{1
if !empty(s:editorconfig_core_mode)

    if s:editorconfig_core_mode == 'external_command'
        if s:InitializeExternalCommand()
            echo 'EditorConfig: Failed to initialize external_command mode'
            finish
        endif
    else
        let s:editorconfig_core_py_dir = s:FindPythonFiles()

        if empty(s:editorconfig_core_py_dir)
            echo 'EditorConfig: '.
                        \ 'EditorConfig Python Core files could not be found.'
            finish
        endif

        if s:editorconfig_core_mode == 'python_builtin' &&
                    \ s:InitializePythonBuiltin(s:editorconfig_core_py_dir)
            echo 'EditorConfig: Failed to initialize vim built-in python.'
            finish
        elseif s:editorconfig_core_mode == 'python_external' &&
                    \ s:InitializePythonExternal()
            echo 'EditorConfig: Failed to find external Python interpreter.'
            finish
        endif
    endif
endif

" Determine the editorconfig_core_mode we should use {{{1
while 1
    " If user has specified a mode, just break
    if exists('s:editorconfig_core_mode') && !empty(s:editorconfig_core_mode)
        break
    endif

    " Find Python core files. If not found, we try external_command mode
    let s:editorconfig_core_py_dir = s:FindPythonFiles()
    if empty(s:editorconfig_core_py_dir) " python files are not found
        if !s:InitializeExternalCommand()
            let s:editorconfig_core_mode = 'external_command'
        endif
        break
    endif

    " Builtin python mode first
    if !s:InitializePythonBuiltin(s:editorconfig_core_py_dir)
        let s:editorconfig_core_mode = 'python_builtin'
        break
    endif

    " Then external_command mode
    if !s:InitializeExternalCommand()
        let s:editorconfig_core_mode = 'external_command'
        break
    endif

    " Finally external python mode
    if !s:InitializePythonExternal()
        let s:editorconfig_core_mode = 'python_external'
        break
    endif

    break
endwhile

" No EditorConfig Core is available
if empty(s:editorconfig_core_mode)
    echo "EditorConfig: ".
                \ "No EditorConfig Core is available. The plugin won't work."
    finish
endif

function! s:UseConfigFiles()

    " ignore buffers without a name
    if empty(expand('%:p'))
        return
    endif

    " Ignore specific patterns
    for pattern in g:EditorConfig_exclude_patterns
        if expand('%:p') =~ pattern
            return
        endif
    endfor

    if s:editorconfig_core_mode == 'external_command'
        call s:UseConfigFiles_ExternalCommand()
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

" command, autoload {{{1
command! EditorConfigReload call s:UseConfigFiles() " Reload EditorConfig files
augroup editorconfig
    autocmd!
    autocmd BufNewFile,BufReadPost,BufFilePost * call s:UseConfigFiles()
    autocmd BufNewFile,BufRead .editorconfig set filetype=dosini
augroup END

" UseConfigFiles function for different mode {{{1
function! s:UseConfigFiles_Python_Builtin() " {{{2
" Use built-in python to run the python EditorConfig core

    let l:config = {}
    let l:ret = 0

    " ignore buffers that do not have a file path associated
    if empty(expand('%:p'))
        return 0
    endif

    python << EEOOFF

ec_data['filename'] = vim.eval("expand('%:p')")
ec_data['conf_file'] = ".editorconfig"

try:
    ec_data['options'] = editorconfig.get_properties(ec_data['filename'])
except editorconfig_except.EditorConfigError as e:
    if int(vim.eval('g:EditorConfig_verbose')) != 0:
        print >> sys.stderr, str(e)
    vim.command('let l:ret = 1')

EEOOFF
    if l:ret != 0
        return l:ret
    endif

    python << EEOOFF
for key, value in ec_data['options'].items():
    vim.command("let l:config['" + key.replace("'", "''") + "'] = " +
        "'" + value.replace("'", "''") + "'")

EEOOFF

    call s:ApplyConfig(l:config)

    return 0
endfunction

function! s:UseConfigFiles_Python_External() " {{{2
" Use external python interp to run the python EditorConfig Core

    let l:cmd = s:editorconfig_python_interp . ' ' .
                \ s:editorconfig_core_py_dir . '/main.py'

    call s:SpawnExternalParser(l:cmd)

    return 0
endfunction

function! s:UseConfigFiles_ExternalCommand() " {{{2
" Use external EditorConfig core (The C core, or editorconfig.py)
    call s:SpawnExternalParser(s:EditorConfig_exec_path)
endfunction

function! s:SpawnExternalParser(cmd) " {{{2
" Spawn external EditorConfig. Used by s:UseConfigFiles_Python_External() and
" s:UseConfigFiles_ExternalCommand()

    let l:cmd = a:cmd

    " ignore buffers that do not have a file path associated
    if empty(expand("%:p"))
        return
    endif

    " if editorconfig is present, we use this as our parser
    if !empty(l:cmd)
        let l:config = {}

        " In Windows, 'shellslash' also changes the behavior of 'shellescape'.
        " It makes 'shellescape' behave like in UNIX environment. So ':setl
        " noshellslash' before evaluating 'shellescape' and restore the
        " settings afterwards when 'shell' does not contain 'sh' somewhere.
        if has('win32') && empty(matchstr(&shell, 'sh'))
            let l:old_shellslash = &l:shellslash
            setlocal noshellslash
        endif

        let l:cmd = l:cmd . ' ' . shellescape(expand('%:p'))

        " restore 'shellslash'
        if exists('l:old_shellslash')
            let &l:shellslash = l:old_shellslash
        endif

        let l:parsing_result = split(system(l:cmd), '\n')

        " if editorconfig core's exit code is not zero, give out an error
        " message
        if v:shell_error != 0
            echohl ErrorMsg
            echo 'Failed to execute "' . l:cmd . '". Exit code: ' .
                        \ v:shell_error
            echo ''
            echo 'Message:'
            echo l:parsing_result
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

function! s:ApplyConfig(config) " {{{1
    " Only process normal buffers (do not treat help files as '.txt' files)
    if !empty(&buftype)
        return
    endif

" Set the indentation style according to the config values

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

    if has_key(a:config, "end_of_line") && &l:modifiable
        if a:config["end_of_line"] == "lf"
            setl fileformat=unix
        elseif a:config["end_of_line"] == "crlf"
            setl fileformat=dos
        elseif a:config["end_of_line"] == "cr"
            setl fileformat=mac
        endif
    endif

    if has_key(a:config, "charset") && &l:modifiable
        if a:config["charset"] == "utf-8"
            setl fileencoding=utf-8
            setl nobomb
        elseif a:config["charset"] == "utf-8-bom"
            setl fileencoding=utf-8
            setl bomb
        elseif a:config["charset"] == "latin1"
            setl fileencoding=latin1
            setl nobomb
        elseif a:config["charset"] == "utf-16be"
            setl fileencoding=utf-16be
            setl bomb
        elseif a:config["charset"] == "utf-16le"
            setl fileencoding=utf-16le
            setl bomb
        endif
    endif

    augroup editorconfig_trim_trailing_whitespace
        autocmd! BufWritePre <buffer>
        if get(a:config, 'trim_trailing_whitespace', 'false') ==# 'true'
            autocmd BufWritePre <buffer> call s:TrimTrailingWhitespace()
        endif
    augroup END

    if has_key(a:config, "insert_final_newline")
        if exists('+fixendofline')
            if a:config["insert_final_newline"] == "false"
                setl nofixendofline
            else
                setl fixendofline
            endif
        elseif  exists(':SetNoEOL') == 2
            if a:config["insert_final_newline"] == "false"
                silent! SetNoEOL    " Use the PreserveNoEOL plugin to accomplish it
            endif
        endif
    endif

    " highlight the columns following max_line_length
    if has_key(a:config, 'max_line_length')
        let l:max_line_length = str2nr(a:config['max_line_length'])

        if l:max_line_length >= 0
            let &l:textwidth = l:max_line_length
            if g:EditorConfig_preserve_formatoptions == 0
                setlocal formatoptions+=tc
            endif
        endif

        if exists('+colorcolumn')
            if l:max_line_length > 0
                if g:EditorConfig_max_line_indicator == 'line'
                    let &l:colorcolumn = l:max_line_length + 1
                elseif g:EditorConfig_max_line_indicator == 'fill'
                    let &l:colorcolumn = join(
                                \ range(l:max_line_length+1,&l:columns),',')
                endif
            endif
        endif
    endif

    call editorconfig#ApplyHooks(a:config)
endfunction

" }}}

function! s:TrimTrailingWhitespace() " {{{{
    " don't lose user position when trimming trailing whitespace
    let s:view = winsaveview()
    try
        %s/\s\+$//e
    finally
        call winrestview(s:view)
    endtry
endfunction " }}}

let &cpo = s:saved_cpo
unlet! s:saved_cpo

" vim: fdm=marker fdc=3
