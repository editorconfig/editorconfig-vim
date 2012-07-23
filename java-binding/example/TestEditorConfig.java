import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.util.List;
import org.editorconfig.core.*;

public class TestEditorConfig {
    public static void main(String[] args) throws EditorConfigException {
        EditorConfig ec = new EditorConfig();
        List<EditorConfig.OutPair> l = null;
        try {
            l = ec.getProperties(System.getProperty("user.dir") + "/a.py");
        } catch(EditorConfigException e) {
            System.out.println(e);
            System.exit(1);
        }
        
        for(int i = 0; i < l.size(); ++i) {
            System.out.println(l.get(i).getKey() + "=" + l.get(i).getVal());
        }
    }
}
