package org.editorconfig.core;

/**
 * Exception throwed by EditorConfig.getProperties() if an invalid version
 * number is specified
 */
public class VersionException extends EditorConfigException {
    
    VersionException(String msg) {
        super(msg);
    }
}
