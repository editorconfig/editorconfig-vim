package org.editorconfig.core;

import java.util.LinkedList;
import java.util.List;
import org.python.core.Py;
import org.python.core.PyString;
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;

/**
 * EditorConfig handler
 */
public class EditorConfig {

    private PythonInterpreter pyInterp;

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
     * @throws PythonException If a Jython exception happens.
     * 
     * @see #EditorConfig(List)
     */
    public EditorConfig()
            throws PythonException {

        this(null);


    }

    /**
     * EditorConfig constructor.
     *
     * Same as {@link #EditorConfig()}, but with an additional parameter
     * {@code jarLocations}.
     *
     * @param jarLocations The possible locations of {@code editorconfig.jar}
     * file. This parameter is used in some cases, {@code editorconfig.jar}
     * cannot locate itself (e.g. java program launched in GNOME desktop
     * environment may have this kind of issue). However, some modules are
     * packed in {@code editorconfig.jar} file, so this file must be located
     * for this library to work correctly.
     *
     * @see #EditorConfig()
     */
    public EditorConfig(List<String> jarLocations)
            throws PythonException {
        pyInterp = new PythonInterpreter(null, new PySystemState());
        PySystemState pySysStat = Py.getSystemState();

        // Add all "jarLocations/Lib" to sys.path
        if(jarLocations != null)
            for(String jarPath : jarLocations)
                pySysStat.path.append(new PyString(jarPath + "/Lib"));

        pyInterp.exec("from editorconfig import get_properties");
        pyInterp.exec("from editorconfig import exceptions");
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
     * @throws org.editorconfig.core.PythonException If a Jython exception happens.
     *
     */
    public List<OutPair> getProperties(String filename)
            throws EditorConfigException {

        pyInterp.exec("try:\n" +
                "\toptions = get_properties(r\"\"\"" + filename + "\"\"\")\n" +
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

        String except = pyInterp.get("e").toString();
        if(except.equals("ParsingError"))
            throw new ParsingException("Failed to parse .editorconfig file.");
        else if(except.equals("PathError"))
            throw new PathException("Invalid file name specified. Must be absolute path.");
        else if(except.equals("VersionError"))
            throw new VersionException("Invalid Version Specified.");

        pyInterp.exec("option_count = len(options)");
        pyInterp.exec("option_items = options.items()");
 
        LinkedList<OutPair> retList = new LinkedList<OutPair>();
        int count = Integer.parseInt(pyInterp.get("option_count").toString());
        for(int i = 0; i < count; ++i) {
            pyInterp.exec("option_key = option_items[" + i + "][0]");
            pyInterp.exec("option_item = option_items[" + i + "][1]");
            OutPair op = new OutPair(
                    pyInterp.get("option_key").toString(),
                    pyInterp.get("option_item").toString());

            retList.add(op);
        }

        return retList;
    }
}
