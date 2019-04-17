" autoload/editorconfig_core.vim: top-level functions for
" editorconfig-core-vimscript.
" Copyright (c) 2018 Chris White.  All rights reserved.

let s:saved_cpo = &cpo
set cpo&vim

" Variables {{{1

" Note: we create this variable in every script that accesses it.  Normally, I
" would put this in plugin/editorconfig.vim.  However, in some of my tests,
" the command-line testing environment did not load plugin/* in the normal
" way.  Therefore, I do the check everywhere so I don't have to special-case
" the command line.

if !exists('g:editorconfig_core_vimscript_debug')
    let g:editorconfig_core_vimscript_debug = 0
endif
" }}}1

" The version we are, i.e., the latest version we support
function! editorconfig_core#version()
    return [0,12,2]
endfunction

" === CLI =============================================================== {{{1

" For use from the command line.  Output settings for in_name to
" the buffer named out_name.  If an optional argument is provided, it is the
" name of the config file to use (default '.editorconfig').
" TODO support multiple files
"
" filename (if any)
" @param names  {Dictionary}    The names of the files to use for this run
"   - output    [required]  Where the editorconfig settings should be written
"   - target    [required]  A string or list of strings to process.  Each
"                           must be a full path.
"   - dump      [optional]  If present, write debug info to this file
" @param job    {Dictionary}    What to do - same format as the input of
"                               editorconfig_core#handler#get_configurations(),
"                               except without the target member.

function! editorconfig_core#currbuf_cli(names, job) " out_name, in_name, ...
    let l:output = []

    " Preprocess the job
    let l:job = deepcopy(a:job)

    if has_key(l:job, 'version')    " string to list
        let l:ver = split(editorconfig_core#util#strip(l:job.version), '\v\.')
        for l:idx in range(len(l:ver))
            let l:ver[l:idx] = str2nr(l:ver[l:idx])
        endfor

        let l:job.version = l:ver
    endif

    " TODO provide version output from here instead of the shell script
"    if string(a:names) ==? 'version'
"        return
"    endif
"
    if type(a:names) != type({}) || type(a:job) != type({})
        throw 'Need two Dictionary arguments'
    endif

    if has_key(a:names, 'dump')
        execute 'redir! > ' . fnameescape(a:names.dump)
        echom 'Names: ' . string(a:names)
        echom 'Job: ' . string(l:job)
        let g:editorconfig_core_vimscript_debug = 1
    endif

    if type(a:names['target']) == type([])
        let l:targets = a:names.target
    else
        let l:targets = [a:names.target]
    endif

    for l:target in l:targets

        " Pre-process quoting weirdness so we are more flexible in the face
        " of CMake+CTest+BAT+Powershell quoting.

        " Permit wrapping in double-quotes
        let l:target = substitute(l:target, '\v^"(.*)"$', '\1', '')

        " Permit empty ('') entries in l:targets
        if strlen(l:target)<1
            continue
        endif

        if has_key(a:names, 'dump')
            echom 'Trying: ' . string(l:target)
        endif

        let l:job.target = l:target
        let l:options = editorconfig_core#handler#get_configurations(l:job)

        if has_key(a:names, 'dump')
            echom 'editorconfig_core#currbuf_cli result: ' . string(l:options)
        endif

        if len(l:targets) > 1
            let l:output += [ '[' . l:target . ']' ]
        endif

        for [ l:key, l:value ] in items(l:options)
            let l:output += [ l:key . '=' . l:value ]
        endfor

    endfor "foreach target

    " Write the output file
    call writefile(l:output, a:names.output)
endfunction "editorconfig_core#currbuf_cli

" }}}1

let &cpo = s:saved_cpo
unlet! s:saved_cpo

" vi: set fdm=marker fo-=ro:
