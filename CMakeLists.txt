# TESTING TERMINAL (from .build/)
#cmake -DCMAKE_BUILD_TYPE=PROFILE ..
#make
#./company_test
#gcovr -r .. . --html --html-details -o example-html-details.html


cmake_minimum_required(VERSION 3.16)

project(test)

include(DownloadProject.cmake)
download_project(PROJ                googletest
                 GIT_REPOSITORY      https://github.com/google/googletest.git
                 GIT_TAG             master
                 ${UPDATE_DISCONNECTED_IF_AVAILABLE}
)

# Prevent GoogleTest from overriding our compiler/linker options
# when building with Visual Studio
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR})

# This flags are used if cmake is called with -DCMAKE_BUILD_TYPE=PROFILE
set(CMAKE_C_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_FLAGS_PROFILE --coverage)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(LIB_SOURCE_FILES company.c)
add_library(company STATIC ${LIB_SOURCE_FILES})

add_executable(main main.c)
target_link_libraries(main company)

option(BUILD_TESTS "Build all tests." OFF) # Makes boolean 'test' available.

if (BUILD_TESTS)
    enable_testing()

    include(GoogleTest)
    add_executable(company_test company_test.cpp)

    target_link_libraries(company_test gtest company)
    gtest_add_tests(TARGET company_test)

endif()