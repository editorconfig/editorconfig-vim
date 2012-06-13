#!/bin/sh

CLASSPATH='../build/editorconfig.jar:.'
javac -cp $CLASSPATH TestEditorConfig.java
java -cp $CLASSPATH TestEditorConfig
