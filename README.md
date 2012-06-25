# EditorConfig Vim Plugin

This is an [EditorConfig][] plugin for Vim. This plugin could be found on both
[GitHub][] and [Vim online][].

## Installation

There are two ways for installation:

- If your Vim is compiled with `+python` feature (this is usually true on most
  Linux distributions), the most simple way to install this plugin is to
  download the archive and extract it into your Vim runtime directory (`~/.vim`
  on UNIX/Linux and `$VIM_INSTALLATION_FOLDER\vimfiles` on windows).

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
[GitHub]: https://github.com/editorconfig/editorconfig-vim
[properties]: http://editorconfig.org/#supported-properties
[Vim online]: http://www.vim.org/scripts/script.php?script_id=3934
