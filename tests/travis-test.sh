#!/bin/bash

# Error exit; debug output
set -evx

if [[ $TEST_WHICH = 'plugin' ]]; then       # test plugin
    bundle exec rspec tests/plugin/spec/editorconfig_spec.rb

else                                        # test core
    cd tests/core
    mkdir build
    cd build
    cmake ..
    ctest . --output-on-failure
fi
