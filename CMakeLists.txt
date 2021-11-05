cmake_minimum_required(VERSION 3.16)

set(CMAKE_CXX_STANDARD 11)

project(hw2)

# This flags are used if cmake is called with -DCMAKE_BUILD_TYPE=PROFILE
set(CMAKE_C_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#set cpp compile flags
set(CPP_FLAGS "-Wall -Wpedantic -Werror -Wno-variadic-macros -Wno-long-long -Wno-shadow")
set(C_FLAGS "-std=gnu11 -Wall -Wpedantic -Werror -Wno-variadic-macros -Wno-long-long -Wno-shadow")
set(CMAKE_CXX_FLAGS ${CPP_FLAGS})
set(CMAKE_C_FLAGS ${C_FLAGS})

set(LIB_SOURCE_FILES tools.c)
add_library(company STATIC ${LIB_SOURCE_FILES})

# Build main
option(BUILD_MAIN ON)
if (BUILD_MAIN)
    add_executable(main main.c)
    target_link_libraries(main company)
endif()