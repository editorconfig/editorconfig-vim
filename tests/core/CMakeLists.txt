# This file is used for testing only

# To perform the test, from the root of the project tree, run
#   mkdir build
#   cd build
#   cmake ..
#   ctest .

cmake_minimum_required(VERSION 3.5)
#set(CMAKE_LEGACY_CYGWIN_WIN32 0)

# Do not check any compiler
project(editorconfig-core-vimscript NONE)

enable_testing()
if(NOT WIN32)
    set(EDITORCONFIG_CMD "${CMAKE_SOURCE_DIR}/editorconfig")
else()
    set(EDITORCONFIG_CMD "${CMAKE_SOURCE_DIR}/editorconfig.bat")
endif()

add_subdirectory(tests)

configure_file(CTestCustom.cmake ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
