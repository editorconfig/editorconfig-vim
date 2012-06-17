#!/bin/sh

CLASSPATH="../build/editorconfig.jar:.:$CLASSPATH"
javac -cp $CLASSPATH TestEditorConfig.java
java -cp $CLASSPATH TestEditorConfig
