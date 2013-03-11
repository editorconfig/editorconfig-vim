@echo off

SETLOCAL

set LOCAL_CLASSPATH="../build/editorconfig.jar;.;%CLASSPATH%"
javac -cp %LOCAL_CLASSPATH% TestEditorConfig.java
java -cp %LOCAL_CLASSPATH% TestEditorConfig

ENDLOCAL
