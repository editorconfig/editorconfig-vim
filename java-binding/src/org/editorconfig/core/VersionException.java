package org.editorconfig.core;

/**
 * Exception throwed by {@link EditorConfig#getProperties(String)} if an
 * invalid version number is specified
 */
public class VersionException extends EditorConfigException {
    
    VersionException(String msg) {
        super(msg);
    }
}
