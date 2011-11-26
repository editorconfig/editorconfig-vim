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

augroup editorconfig
autocmd! editorconfig
autocmd editorconfig BufNewFile,BufReadPost * call s:UseConfigFiles()
autocmd editorconfig BufNewFile,BufRead .editorconfig set filetype=dosini

function! s:UseConfigFiles()

    let l:cmd = ''
    " search for editorconfig core
    for possible_cmd in [
                \ 'editorconfig',
                \ '/usr/local/bin/editorconfig',
                \ '/usr/bin/editorconfig',
                \ '/opt/bin/editorconfig',
                \ '/opt/editorconfig/bin/editorconfig']
        if executable(possible_cmd)
            let l:cmd = possible_cmd
            break
        endif
    endfor

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
        let &l:shiftwidth = str2nr(a:config["indent_size"])
        let &l:softtabstop = &l:shiftwidth
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

