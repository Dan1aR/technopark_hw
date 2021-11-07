cmake_minimum_required(VERSION 3.16)

set(CMAKE_CXX_STANDARD 11)

project(hw2 C CXX)

# This flags are used if cmake is called with -DCMAKE_BUILD_TYPE=PROFILE
set(CMAKE_C_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#set cpp compile flags
set(CMAKE_CXX_FLAGS "-Wall -Wpedantic -Werror -Wno-variadic-macros -Wno-long-long -Wno-shadow")
set(CMAKE_C_FLAGS "-std=gnu11 -Wall -Wpedantic -Werror -Wno-variadic-macros -Wno-long-long -Wno-shadow")

# add_compile_options(-fsanitize=address -fsanitize=undefined)
# add_link_options(-fsanitize=address -fsanitize=undefined)

include_directories(include)

set(FIND_CONSISTENT_LIB  ${PROJECT_SOURCE_DIR}/include/libdtools.h lib_consistent/libdataproc_consistent.c lib_consistent/tools.c generator/generator.c)
add_library(find_consistent_lib STATIC ${FIND_CONSISTENT_LIB})
target_include_directories(find_consistent_lib PUBLIC ${PROJECT_SOURCE_DIR}/include)

set(FIND_PARALLEL_LIB  ${PROJECT_SOURCE_DIR}/include/libdtools.h lib_parallel/libdataproc_parallel.c lib_parallel/tools.c generator/generator.c)
add_library(find_parallel_lib SHARED ${FIND_PARALLEL_LIB})
target_include_directories(find_parallel_lib PUBLIC ${PROJECT_SOURCE_DIR}/include)


# Build main
option(BUILD_MAIN ON)
if (BUILD_MAIN)
    add_executable(${PROJECT_NAME} src/main.c)
    target_link_libraries(${PROJECT_NAME} PRIVATE find_consistent_lib)
    target_link_libraries(${PROJECT_NAME} PRIVATE find_parallel_lib -ldl)
endif()