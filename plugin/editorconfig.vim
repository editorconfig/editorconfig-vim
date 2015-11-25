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
if !exists('g:EditorConfig_preserve_formatoptions')
    let g:EditorConfig_preserve_formatoptions = 0
endif

if !exists('g:EditorConfig_max_line_indicator')
    let g:EditorConfig_max_line_indicator = 'line'
endif

if !exists('g:EditorConfig_exclude_patterns')
    let g:EditorConfig_exclude_patterns = []
endif

" command, autoload {{{1
command! EditorConfigReload call s:UseConfigFiles() " Reload EditorConfig files
augroup editorconfig
    autocmd!
    autocmd BufNewFile,BufReadPost,BufFilePost * call s:UseConfigFiles()
    autocmd BufNewFile,BufRead .editorconfig set filetype=dosini
augroup END

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

    let configfile = findfile('.editorconfig', escape(expand('.'), '*[]?{}, ') . ';')
	if empty(configfile)
		return
	endif

	let inrange = 0
	let lines = readfile(fnamemodify(configfile, ':p'))
	let config = {}
	for l in range(len(lines))
		let line = lines[l]
		let mx = '^\[\([^\]]\+\)\]'
		if line =~ mx
			let pattern = matchlist(line, mx)[1]
			let pattern = substitute(pattern, '\.', '\\.', 'g')
			let pattern = substitute(pattern, '*', '.*', 'g')
			let pattern = '^' . pattern . '$'

			if expand('%:p') !~ pattern
				let inrange = 1
			else
				let inrange = 0
			endif
		elseif inrange == 1
			let token = matchlist(line, '^\s*\([a-zA-Z][a-zA-Z0-9_]*\)\s*=\s*\%(\([^ \t\''"]\+\)\|''\([^\'']*\)''\|"\(\%([^\"\\]\|\\.\)*\)"\)')
			if len(token) > 3 && !empty(token[1]) && !empty(token[2])
				let config[token[1]] = token[2]
			endif
		endif
	endfor
	call s:ApplyConfig(config)
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
