#!/bin/bash
# travis-test.sh: Script for running editorconfig-vim tests under Travis CI.
# Copyright (c) 2019 Chris White.  All rights reserved.
# Licensed Apache, version 2.0 or any later version, at your option.

# Error exit; debug output
set -evx

if [[ $TEST_WHICH = 'plugin' ]]; then       # test plugin
    # Use the standalone Vimscript EditorConfig core to test the plugin's
    # external_command mode
    export EDITORCONFIG_VIM_EXTERNAL_CORE=tests/core/editorconfig

    bundle exec rspec tests/plugin/spec/editorconfig_spec.rb

else                                        # test core
    cd tests/core
    mkdir build
    cd build
    cmake ..
    ctest . --output-on-failure -VV -C Debug
    # -C Debug: for Visual Studio builds, you have to specify
    # a configuration.
fi
