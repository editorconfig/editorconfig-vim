from __future__ import print_function

try:
    try:
        import vim
        import sys
    except:
        vim.command('let l:ret = 2')
        raise

    try:
        sys.path.insert(0, vim.eval('a:editorconfig_core_py_dir'))

        import editorconfig
        import editorconfig.exceptions as editorconfig_except
    except:
        vim.command('let l:ret = 3')
        raise
    finally:
        del sys.path[0]

    # `ec_` prefix is used in order to keep clean Python namespace
    ec_data = {}

    def ec_UseConfigFiles():
        ec_data['filename'] = vim.eval("expand('%:p')")
        ec_data['conf_file'] = ".editorconfig"

        try:
            ec_data['options'] = editorconfig.get_properties(ec_data['filename'])
        except editorconfig_except.EditorConfigError as e:
            if int(vim.eval('g:EditorConfig_verbose')) != 0:
                print(str(e), file=sys.stderr)
            vim.command('let l:ret = 1')
            return

        for key, value in ec_data['options'].items():
            vim.command("let l:config['" + key.replace("'", "''") + "'] = " +
                "'" + value.replace("'", "''") + "'")

except:
    pass
