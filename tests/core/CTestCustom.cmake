# CTestCustom.cmake: Skip UTF-8 tests
# Part of editorconfig-vim

# Skip UTF8 tests on Windows for now per
# https://github.com/editorconfig/editorconfig-core-c/pull/31#issue-154810185
if(WIN32 AND (NOT "$ENV{RUN_UTF8}"))
    message(WARNING "Skipping UTF-8 tests on this platform")
    set(CTEST_CUSTOM_TESTS_IGNORE ${CTEST_CUSTOM_TESTS_IGNORE} g_utf_8_char)
    set(CTEST_CUSTOM_TESTS_IGNORE ${CTEST_CUSTOM_TESTS_IGNORE} utf_8_char)
endif()
