package org.editorconfig.core;


abstract public class EditorConfigException extends Exception {
    EditorConfigException(String msg) {
        super(msg);
    }
}
