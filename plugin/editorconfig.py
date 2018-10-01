from __future__ import print_function

try:
    # `ec_` prefix is used in order to keep clean Python namespace
    ec_data = {}

    try:
        import vim
        import sys

        ec_data['win32unix'] = int(vim.eval("has('win32unix')")) != 0
    except:
        vim.command('let l:ret = 2')
        raise

    # Converts the path to windows when we are in mingw or cygwin
    def maybe_to_win(filepath):
        if ec_data['win32unix']:
            if filepath[0] == '/':
                # hacky way of making a unix path out of a linux path
                filepath = filepath[1] + ':' + filepath[2:]

        return filepath


    try:
        ec_data['verbose'] = int(vim.eval('g:EditorConfig_verbose')) != 0

        pycoredir = maybe_to_win(vim.eval('a:editorconfig_core_py_dir'))

        if ec_data['verbose']:
            print("EditorConfig.Python: Python core dir: " + pycoredir)

        sys.path.insert(0, pycoredir)

        import editorconfig
        import editorconfig.exceptions as editorconfig_except
    except:
        vim.command('let l:ret = 3')
        raise
    finally:
        del sys.path[0]

    def ec_UseConfigFiles():
        ec_data['filename'] = maybe_to_win(vim.eval("expand('%:p')"))
        ec_data['conf_file'] = ".editorconfig"
        if ec_data['verbose']:
            print('EditorConfig.Python: ' + str(ec_data))

        try:
            ec_data['options'] = editorconfig.get_properties(ec_data['filename'])
        except editorconfig_except.EditorConfigError as e:
            if ec_data['verbose']:
                print('EditorConfig.Python: ' + str(e), file=sys.stderr)
            vim.command('let l:ret = 1')
            return

        for key, value in ec_data['options'].items():
            cmd = "let l:config['" + key.replace("'", "''") + "'] = " +\
                "'" + value.replace("'", "''") + "'"
            if ec_data['verbose']:
                print("EditorConfig.Python: Found setting: " + cmd)
            vim.command(cmd)

except:
    pass
