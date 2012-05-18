# This file is used for testing only

# To perform the test, run `cmake .` at the root of the project tree followed
# by ctest .

cmake_minimum_required(VERSION 2.6)

# Do not check any compiler
project(editorconfig-core-py NONE)

find_package(PythonInterp)

if(NOT PYTHONINTERP_FOUND)
    message(FETAL_ERROR
        "Python interpreter is not found. If you have python installed, please run:
        cmake -DPYTHON_EXECUTABLE=/path/to/python .")
endif()

enable_testing()
set(EDITORCONFIG_CMD ${PYTHON_EXECUTABLE} ${PROJECT_SOURCE_DIR}/main.py)
add_subdirectory(tests)
