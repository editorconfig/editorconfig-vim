package org.editorconfig.core;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.util.List;
import java.util.LinkedList;

/**
 * EditorConfig handler
 */
public class EditorConfig {

    private ScriptEngine jythonEngine;

    /**
     * String-String pair to store the parsing result.
     */
    public class OutPair {
        private String key;
        private String val;

        /*
         * Constructor
         */
        OutPair(String key, String val) {
            this.key = key;
            this.val = val;
        }

        /**
         * Return the key of the current pair.
         */
        public String getKey() {
            return this.key;
        }

        /**
         * Return the value of the current pair.
         */
        public String getVal() {
            return this.val;
        }
    }

    /**
     * EditorConfig constructor.
     *
     * @throws javax.script.ScriptException If a Jython exception happens.
     * 
     */
    public EditorConfig()
            throws ScriptException {
        ScriptEngineManager manager = new ScriptEngineManager();

        jythonEngine = manager.getEngineByName("python");

        jythonEngine.eval("from editorconfig import get_properties");
        jythonEngine.eval("from editorconfig import exceptions");
    }
    
    /**
     * Parse editorconfig files corresponding to the file path given by
     * filename, and return the parsing result.
     *
     * @param filename The full path to be parsed. The path is usually the path
     * of the file which is currently edited by the editor.
     *
     * @return The parsing result stored in a list of {@link
     * EditorConfig.OutPair}.
     *
     * @throws org.editorconfig.core.ParsingException If an
     * {@code .editorconfig} file could not be parsed
     *
     * @throws org.editorconfig.core.PathException If an invalid file path is
     * specified as {@code filename}
     *
     * @throws org.editorconfig.core.EditorConfigException If an EditorConfig
     * exception occurs. Usually one of {@link ParsingException} or {@link
     * PathException}.
     *
     * @throws javax.script.ScriptException If a Jython exception happens.
     *
     */
    public List<OutPair> getProperties(String filename)
            throws EditorConfigException, ScriptException {

        jythonEngine.eval("try:\n" +
                "\toptions = get_properties('" + filename + "')\n" +
                "except exceptions.ParsingError:\n" +
                "\te = 'ParsingError'\n" +
                "except exceptions.PathError:\n" +
                "\te = 'PathError'\n" +
                "except exceptions.VersionError:\n" +
                "\te = 'VersionError'\n" +
                "except exceptions.EditorConfigError:\n" +
                "\te = 'EditorConfigError'\n" +
                "else:\n" +
                "\te = 'None'");

        String except = jythonEngine.get("e").toString();
        if(except.equals("ParsingError"))
            throw new ParsingException("Failed to parse .editorconfig file.");
        else if(except.equals("PathError"))
            throw new PathException("Invalid file name specified. Must be absolute path.");
        else if(except.equals("VersionError"))
            throw new VersionException("Invalid Version Specified.");

        jythonEngine.eval("option_count = len(options)");
        jythonEngine.eval("option_items = options.items()");
 
        LinkedList<OutPair> retList = new LinkedList<OutPair>();
        int count = Integer.parseInt(jythonEngine.get("option_count").toString());
        for(int i = 0; i < count; ++i) {
            jythonEngine.eval("option_key = option_items[" + i + "][0]");
            jythonEngine.eval("option_item = option_items[" + i + "][1]");
            OutPair op = new OutPair(
                    jythonEngine.get("option_key").toString(),
                    jythonEngine.get("option_item").toString());

            retList.add(op);
        }

        return retList;
    }
}
