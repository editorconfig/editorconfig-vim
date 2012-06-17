package org.editorconfig.core;


/**
 * Exception throwed by EditorConfig.getProperties() if an invalid file path is
 * specified
 */
public class PathException extends EditorConfigException {

    PathException(String msg) {
        super(msg);        
    }
}
