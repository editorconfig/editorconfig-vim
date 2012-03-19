import os

from .ini import EditorConfigParser


def get_filenames(path, filename):
    """Yield full filepath for filename in each directory in and above path"""
    while True:
        yield os.path.join(path, filename)
        newpath = os.path.dirname(path)
        if path == newpath:
            break
        path = newpath


class EditorConfigHandler(object):
    """Allows locating and parsing of EditorConfig files for a given filename"""
    def __init__(self, filepath, conf_filename='.editorconfig'):
        """Create EditorConfigHandler for matching given filepath"""
        self.filepath = filepath
        self.conf_filename = conf_filename
        self.options = None

    def preprocess_values(self):
        opts = self.options

        # Lowercase option value for certain options
        for name in ["end_of_line", "indent_style", "indent_size"]:
            if name in opts:
                opts[name] = opts[name].lower()

        # Set indent_size to "tab" if indent_size is unspecified and
        # indent_style is set to "tab".
        if (opts.get("indent_style") == "tab" and
            not opts.has_key("indent_size")):
            opts["indent_size"] = "tab"

        # Set tab_width to indent_size if indent_size is specified and tab_width
        # is unspecified
        if (opts.has_key("indent_size") and not opts.has_key("tab_width") and
            opts["indent_size"] != "tab"):
            opts["tab_width"] = opts["indent_size"]

    def get_configurations(self):
        """Find EditorConfig files and return all options matching filepath"""
        path, filename = os.path.split(self.filepath)
        conf_files = get_filenames(path, self.conf_filename)
        for filename in conf_files:
            parser = EditorConfigParser(self.filepath)
            parser.read(filename)
            old_options = self.options
            self.options = parser.options
            if old_options:
                self.options.update(old_options)
            if parser.root_file:
                break
        self.preprocess_values()
        return self.options
