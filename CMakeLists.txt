cmake_minimum_required(VERSION 3.16)

# Download Googletest
#include(Downloadproject.cmake)
#download_project(PROJ                googletest
#                 GIT_REPOSITORY      https://github.com/google/googletest.git
#                 GIT_TAG             master
#                 ${UPDATE_DISCONNECTED_IF_AVAILABLE}
#)

set(CMAKE_CXX_STANDARD 11)

include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        703bd9caab50b139428cea1aaff9974ebee5742e # release-1.10.0
)

# Prevent GoogleTest from overriding our compiler/linker options
#set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
#add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR})

project(hw1)

# This flags are used if cmake is called with -DCMAKE_BUILD_TYPE=PROFILE
set(CMAKE_C_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#set cpp compile flags
set(CPP_FLAGS "-Wall -Wpedantic -Werror -Wno-variadic-macros -Wno-long-long -Wno-shadow")
set(C_FLAGS "-std=gnu11 -Wall -Wpedantic -Werror -Wno-variadic-macros -Wno-long-long -Wno-shadow")
set(CMAKE_CXX_FLAGS ${CPP_FLAGS})
set(CMAKE_C_FLAGS ${C_FLAGS})

set(LIB_SOURCE_FILES company.c io.c)
add_library(company STATIC ${LIB_SOURCE_FILES})

# Build main
option(BUILD_MAIN ON)
if (BUILD_MAIN)
    add_executable(main main.c)
    target_link_libraries(main company)
endif()

# Build company_test
option(BUILD_TESTS ON)
if (BUILD_TESTS)
    enable_testing()

    include(GoogleTest)
    add_executable(company_test company_test.cpp)

    target_link_libraries(company_test gtest_main company)
    gtest_add_tests(TARGET company_test)
endif()
