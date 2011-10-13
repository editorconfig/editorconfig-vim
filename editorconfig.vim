augroup editconfig
autocmd! editconfig
autocmd editconfig BufNewFile,BufReadPost * call s:UseConfigFiles()

let s:this_file = expand("%")
let s:this_dir = expand("%:p:h")

" Find all config files in this directory and parent directories.  Apply any
" matching patterns in each config file found (starting with furthest file).
function! s:UseConfigFiles()
    let config_files = reverse(findfile('.editorconfig', ".;", -1))

    for file in config_files
        if filereadable(file)
            let parsed_ini = IniParser#Read(file)
            for file_pattern in keys(parsed_ini)
                if s:FilePatternMatches(file_pattern)
                    call s:ApplyConfig(parsed_ini[file_pattern])
                endif
            endfor
        endif
    endfor
endfunction

" Return 1 if pattern describes current file and 0 otherwise
function! s:FilePatternMatches(pattern)
    let matched_files = split(glob(a:pattern, s:this_dir))
    for found_file in matched_files
        if found_file == s:this_file
            return 1
        endif
    endfor
    return 0
endfunction

" Set the indentation style according to the config values
function! s:ApplyConfig(config)
    if has_key(a:config, "indent_style")
        if a:config["indent_style"] == "tab"
            set noexpandtab
        elseif a:config["indent_style"] == "space"
            let tab_width = a:config["tab_width"] + 0
            set expandtab
            let &shiftwidth = tab_width
            let &softtabstop = tab_width
        endif
    endif
endfunction
