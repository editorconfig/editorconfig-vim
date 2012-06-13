/*
 * Copyright 2006 Sun Microsystems, Inc. All rights reserved. 
 * Use is subject to license terms.
 *
 * Redistribution and use in source and binary forms, with or without modification, are 
 * permitted provided that the following conditions are met: Redistributions of source code 
 * must retain the above copyright notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of 
 * conditions and the following disclaimer in the documentation and/or other materials 
 * provided with the distribution. Neither the name of the Sun Microsystems nor the names of 
 * is contributors may be used to endorse or promote products derived from this software 
 * without specific prior written permission. 

 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
 * AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER 
 * OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

/*
 * JythonScriptEngine.java
 * @author A. Sundararajan
 */

package com.sun.script.jython;

import javax.script.*;
import java.lang.reflect.*;
import java.io.*;
import org.python.core.*;


public class JythonScriptEngine extends AbstractScriptEngine 
        implements Compilable, Invocable { 

    // my factory, may be null
    private ScriptEngineFactory factory;
    // my scope -- associated with the default context
    private PyObject myScope;

    public static final String JYTHON_COMPILE_MODE = "com.sun.script.jython.comp.mode";

    private static ThreadLocal<PySystemState> systemState;
    static {
        PySystemState.initialize();
        systemState = new ThreadLocal<PySystemState>();
    }

    public JythonScriptEngine() {
        myScope = newScope(context);
    }

    // my implementation for CompiledScript
    private class JythonCompiledScript extends CompiledScript {
        // my compiled code
        private PyCode code;

        JythonCompiledScript (PyCode code) {
            this.code = code;
        }

        public ScriptEngine getEngine() {
            return JythonScriptEngine.this;
        }

        public Object eval(ScriptContext ctx) throws ScriptException {
            return evalCode(code, ctx);
        }
    }

    // Compilable methods
    public CompiledScript compile(String script) 
                                  throws ScriptException {  
        PyCode code = compileScript(script, context);
        return new JythonCompiledScript(code);
    }

    public CompiledScript compile (Reader reader) 
                                  throws ScriptException {  
        return compile(readFully(reader));
    }

    // Invocable methods
    public Object invokeFunction(String name, Object... args) 
                         throws ScriptException, NoSuchMethodException {       
        return invokeImpl(null, name, args);
    }

    public Object invokeMethod(Object obj, String name, Object... args) 
                         throws ScriptException, NoSuchMethodException {       
        if (obj == null) {
            throw new IllegalArgumentException("script object is null");
        }
        return invokeImpl(obj, name, args);
    }

    private Object invokeImpl(Object obj, String name, Object... args) 
                         throws ScriptException, NoSuchMethodException {       
        if (name == null) {
            throw new NullPointerException("method name is null");
        }
        setSystemState();
         
        PyObject thiz;
        if (obj instanceof PyObject) {
            thiz = (PyObject) obj;
        } else if (obj == null) {
            thiz = myScope;
        } else {
            thiz = java2py(obj);
        }

        PyObject func = thiz.__findattr__(name);
        if (func == null || !func.isCallable()) { 
            if (thiz == myScope) {
                // lookup in built-in functions. This way
                // user can call invoke built-in functions.
                PyObject builtins = systemState.get().builtins;
                func = builtins.__finditem__(name);
            }
        }

        if (func == null || !func.isCallable()) { 
            throw new NoSuchMethodException(name);
        }
        PyObject res = func.__call__(wrapArguments(args));
        return py2java(res);        
    }
    

    public <T> T getInterface(Object obj, Class<T> clazz) {
        if (obj == null) {
            throw new IllegalArgumentException("script object is null");
        }
        return makeInterface(obj, clazz);
    }

    public <T> T getInterface(Class<T> clazz) {
        return makeInterface(null, clazz);
    }

    private <T> T makeInterface(Object obj, Class<T> clazz) {
        if (clazz == null || !clazz.isInterface()) {
            throw new IllegalArgumentException("interface Class expected");
        }
        final Object thiz = obj;
        return (T) Proxy.newProxyInstance(
              clazz.getClassLoader(),
              new Class[] { clazz },
              new InvocationHandler() {
                  public Object invoke(Object proxy, Method m, Object[] args)
                                       throws Throwable {
                      Object res = invokeImpl(
                                       thiz, m.getName(), args);                      
                      return py2java(java2py(res), m.getReturnType());
                  }
              });
    }


    // ScriptEngine methods
    public Object eval(String str, ScriptContext ctx) 
                       throws ScriptException {	
        PyCode code = compileScript(str, ctx);
        return evalCode(code, ctx);
    }

    public Object eval(Reader reader, ScriptContext ctx)
                       throws ScriptException { 
        return eval(readFully(reader), ctx);
    }

    public ScriptEngineFactory getFactory() {
	synchronized (this) {
	    if (factory == null) {
	    	factory = new JythonScriptEngineFactory();
	    }
        }
	return factory;
    }

    public Bindings createBindings() {
        return new SimpleBindings();
    }

    public void setContext(ScriptContext ctx) {
        super.setContext(ctx);
        // update myScope to keep it in-sync
        myScope = newScope(context);
    }

    // package-private methods
    void setFactory(ScriptEngineFactory factory) {
        this.factory = factory;
    }

    static PyObject java2py(Object javaObj) {
        return Py.java2py(javaObj);
    }

    static Object py2java(PyObject pyObj, Class type) {        
        return (pyObj == null)? null : pyObj.__tojava__(type);
    }

    static Object py2java(PyObject pyObj) {
        return py2java(pyObj, Object.class);
    }

    static PyObject[] wrapArguments(Object[] args) {
        if (args == null) {
            return new PyObject[0];
        }

        PyObject[] res = new PyObject[args.length];
        for (int i = 0; i < args.length; i++) {
            res[i] = java2py(args[i]);
        }
        return res;
    }

    // internals only below this point
    private PyObject getJythonScope(ScriptContext ctx) {
        if (ctx == context) {
            return myScope;
        } else {
            return newScope(ctx);
        }
    }

    private PyObject newScope(ScriptContext ctx) {
        return new JythonScope(this, ctx); 
    }

    private void setSystemState() {
        /*
         * From my reading of Jython source, it appears that
         * PySystemState is set on per-thread basis. So, I 
         * maintain it in a thread local and set it. Besides,
         * this also helps in setting correct class loader
         * -- which is thread context class loader.
         */
        if (systemState.get() == null) {
            // we entering into this thread for the first time.
           
            PySystemState newState = new PySystemState();            
            ClassLoader cl = Thread.currentThread().getContextClassLoader();
            newState.setClassLoader(cl);
            systemState.set(newState);
            Py.setSystemState(newState);
        }
    }

    private PyCode compileScript(String script, ScriptContext ctx) 
                                 throws ScriptException {
        try {
            setSystemState();
            String fileName = (String) ctx.getAttribute(ScriptEngine.FILENAME);
            if (fileName == null) {
                fileName = "<unknown>";
            }

            /*
             * Jython parser seems to have 3 input modes (called compile "kind")
             * These are "single", "eval" and "exec". I don't clearly understand
             * the difference. But, with "eval" and "exec" certain features are
             * not working. For eg. with "eval" assignments are not working. 
             * I've used "exec". But, that is customizable by special attribute.
             */
            String mode = (String) ctx.getAttribute(JYTHON_COMPILE_MODE);
            if (mode == null) {
                mode = "exec";
            }
            return __builtin__.compile(script, fileName, mode);
        } catch (Exception exp) {
            throw new ScriptException(exp);
        }
    }

    private Object evalCode(PyCode code, ScriptContext ctx) 
                            throws ScriptException {
        try {
            setSystemState();
            PyObject scope = getJythonScope(ctx);
            PyObject res = Py.runCode(code, scope, scope);
            return res.__tojava__(Object.class);
        } catch (Exception exp) {
            throw new ScriptException(exp);
        }
    }

    private String readFully(Reader reader) throws ScriptException { 
        char[] arr = new char[8*1024]; // 8K at a time
        StringBuilder buf = new StringBuilder();
        int numChars;
        try {
            while ((numChars = reader.read(arr, 0, arr.length)) > 0) {
                buf.append(arr, 0, numChars);
            }
        } catch (IOException exp) {
            throw new ScriptException(exp);
        }
        return buf.toString();
    }
}
