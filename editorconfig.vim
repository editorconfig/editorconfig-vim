augroup editorconfig
autocmd! editorconfig
autocmd editorconfig BufNewFile,BufReadPost * call s:UseConfigFiles()

" Find all config files in this directory and parent directories.  Apply any
" matching patterns in each config file found (starting with furthest file).
function! s:UseConfigFiles()
    let l:config_files = reverse(findfile('.editorconfig', ".;", -1))

    for file in l:config_files
        if filereadable(file)
            let l:parsed_ini = IniParser#Read(file)
            for file_pattern in keys(l:parsed_ini)
                if s:FilePatternMatches(file_pattern)
                    call s:ApplyConfig(l:parsed_ini[file_pattern])
                endif
            endfor
        endif
    endfor
endfunction

" Return 1 if pattern describes current file and 0 otherwise
function! s:FilePatternMatches(pattern)
    let l:this_file = expand("%")
    let l:this_dir = expand("%:p:h")
    let l:matched_files = split(glob(a:pattern, l:this_dir))
    for found_file in l:matched_files
        if found_file == l:this_file
            return 1
        endif
    endfor
    return 0
endfunction

" Set the indentation style according to the config values
function! s:ApplyConfig(config)
    if has_key(a:config, "indent_style")
        if a:config["indent_style"] == "tab"
            setl noexpandtab
        elseif a:config["indent_style"] == "space"
            let l:tab_width = a:config["tab_width"] + 0
            setl expandtab
            let &l:shiftwidth = l:tab_width
            let &l:softtabstop = l:tab_width
        endif
    endif
endfunction
