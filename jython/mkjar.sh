#!/bin/sh

jython_url='http://downloads.sourceforge.net/project/jython/jython/2.2.1/jython_installer-2.2.1.jar?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fjython%2Ffiles%2Fjython%2F2.2.1%2F&ts=1338203268&use_mirror=iweb'
tmp_dir=`pwd`/tmp
output_dir=`pwd`/jar
editorconfig_py_dir=`pwd`/..

mkdir -p "$tmp_dir"

cd "$tmp_dir"

# Download Jython if it is not downloaded yet
if [ ! -f jython_installer.jar ]; then
  wget $jython_url -O jython_installer.jar

  if [ $? != 0 ]; then
    exit 1
  fi
fi

# install the standalone package, and move it to current dir
java -jar jython_installer.jar -s -v -d ./install -t standalone

if [ $? != 0 ]; then
  exit 1
fi

mv install/jython.jar jython_editorconfig.jar

# package EditorConfig python files
rm ./Lib
ln -s "$editorconfig_py_dir" ./Lib
echo 'from editorconfig.main import main

try:
    main()
except SystemExit:
    pass
' >__run__.py
chmod +x __run__.py

zip -r jython_editorconfig.jar __run__.py Lib/README.rst Lib/editorconfig/*.py
chmod +x jython_editorconfig.jar

# Copy jython_editorconfig.jar to dest dir and create the editorconfig shell
# script
cd -
mkdir -p "$output_dir"
cd "$output_dir"
cp $tmp_dir/jython_editorconfig.jar .
echo '#!/bin/sh

script_dir=$(cd "$(dirname "$0")"; pwd)
java -cp "$script_dir/jython_editorconfig.jar" org.python.util.jython -jar "$script_dir/jython_editorconfig.jar" $*' >editorconfig
chmod +x editorconfig
