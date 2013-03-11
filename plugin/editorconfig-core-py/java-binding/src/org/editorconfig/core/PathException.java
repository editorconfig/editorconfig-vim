package org.editorconfig.core;


/**
 * Exception throwed by {@link EditorConfig#getProperties(String)} if an
 * invalid file path is specified
 */
public class PathException extends EditorConfigException {

    PathException(String msg) {
        super(msg);        
    }
}
