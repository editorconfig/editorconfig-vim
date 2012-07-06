package org.editorconfig.core;


/**
 * Exception throwed by EditorConfig() if an exception from the internal Python
 * interpreter (Jython) is thrown
 */
public class PythonException extends EditorConfigException {

    PythonException(String msg) {
        super(msg);        
    }
}
