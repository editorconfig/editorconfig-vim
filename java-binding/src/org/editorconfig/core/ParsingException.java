package org.editorconfig.core;

/**
 * Exception throwed by EditorConfig.getProperties() if an EditorConfig file
 * could not be parsed
 */
public class ParsingException extends EditorConfigException {

    ParsingException(String msg) {
        super(msg);
    }
}
