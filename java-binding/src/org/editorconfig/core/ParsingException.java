package org.editorconfig.core;


// throwed when an EditorConfig file is failed to be parsed
public class ParsingException extends EditorConfigException {

    ParsingException(String msg) {
        super(msg);
    }
}
