augroup editorconfig
autocmd! editorconfig
autocmd editorconfig BufNewFile,BufReadPost * call s:UseConfigFiles()

" wrapper for 'findfile()', a version that eliminates the affect of
" 'suffixesadd'
function! s:FindFile(name, ...)

    let l:old_suffixesadd = &l:suffixesadd
    let &l:suffixesadd = ''

    if a:0 == 1
        let l:ret = findfile(a:name, a:1)
    elseif a:0 == 2
        let l:ret = findfile(a:name, a:1, a:2)
    else
        let l:ret = findfile(a:name)
    endif

    let &l:suffixesadd = l:old_suffixesadd

    return l:ret
endfunction

" Find all config files in this directory and parent directories.  Apply any
" matching patterns in each config file found (starting with furthest file).
function! s:UseConfigFiles()
    let l:config_files = reverse(s:FindFile('.editorconfig', ".;", -1))

    for file in l:config_files
        if file !~ "/"
            let l:file = expand("%:p:h")."/".file
        endif
        if filereadable(file)
            let l:parsed_ini = IniParser#Read(file)
            for file_pattern in keys(l:parsed_ini)
                if s:FilePatternMatches(file_pattern, file)
                    call s:ApplyConfig(l:parsed_ini[file_pattern])
                endif
            endfor
        endif
    endfor
endfunction

" Return 1 if pattern describes current file and 0 otherwise
function! s:FilePatternMatches(pattern, config_file)
    let l:this_file = expand("%:p")

    if a:pattern =~ "/"
        " Use current directory as path prefix for pattern
        let l:path_prefix = strpart(a:config_file, 0, strridx(a:config_file, "/"))
    else
        " Use directory of .editorconfig file as path prefix for pattern
        let l:path_prefix = expand("%:p:h")
    endif

    let l:matched_files = split(globpath(l:path_prefix, a:pattern))
    for found_file in l:matched_files
        if simplify(found_file) == l:this_file
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
