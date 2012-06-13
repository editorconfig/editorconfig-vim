package org.editorconfig.core;


/**
 * The base class of all EditorConfig exceptions.
 */
abstract public class EditorConfigException extends Exception {
    EditorConfigException(String msg) {
        super(msg);
    }
}
