package org.editorconfig.core;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.util.List;
import java.util.LinkedList;


public class EditorConfig {

    private ScriptEngine jythonEngine;

    public class OutPair {
        private String key;
        private String val;
        
        OutPair(String key, String val) {
            this.key = key;
            this.val = val;
        }
        
        public String getKey() {
            return this.key;
        }
        
        public String getVal() {
            return this.val;
        }
    }

    // Constructor
    EditorConfig()
            throws ScriptException {
        ScriptEngineManager manager = new ScriptEngineManager();

        jythonEngine = manager.getEngineByName("python");

        jythonEngine.eval("from editorconfig import get_properties");
        jythonEngine.eval("from editorconfig import exceptions");
    }
    
    /**
     * Get EditorConfig properties
     */
    public List<OutPair> getProperties(String filename)
            throws ScriptException {

        jythonEngine.eval("options = get_properties('" + filename + "')");
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
