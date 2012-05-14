# EditorConfig Vim Plugin

This is an [EditorConfig][] plugin for Vim.

## Installation

There are two ways for installation:

- If your Vim is compiled with `+python` feature (this is usually true on most
  Linux distributions), the most simple way to install this plugin is to
  download the archive and extract it into your Vim runtime directory (`~/.vim`
  on UNIX/Linux and `$VIM_INSTALLATION_FOLDER\vimfiles` on windows).

  **Note**: If you obtain this plugin from GitHub by Git, you should update the
  submodule after you clone the repository, or the python files would be missing
  and the plugin won't work if you want to use the EditorConfig Core written in
  Python:

    git submodule update --init

- If your Vim is not compiled with `+python` feature, please first download the
  [EditorConfig core][] and follow the instructions in the README and INSTALL
  files to install it. Once EditorConfig core is installed, copy the
  `editorconfig.vim` file to your `~/.vim/plugin` directory to install the
  editorconfig plugin.


## Supported properties

The EditorConfig Vim plugin supports the following EditorConfig [properties][]:

* indent_style
* indent_size
* tab_width
* end_of_line
* root (only used by EditorConfig core)

[EditorConfig]: http://editorconfig.org
[EditorConfig core]: https://github.com/editorconfig/editorconfig-core
[properties]: http://editorconfig.org/#supported-properties
