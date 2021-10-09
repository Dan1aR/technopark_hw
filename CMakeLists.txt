cmake_minimum_required(VERSION 3.16)

project(test)

# TESTING TERMINAL (from .build/)
#cmake -DCMAKE_BUILD_TYPE=PROFILE ..
#make
#./company_test
#gcovr -r .. . --html --html-details -o example-html-details.html

# This flags are used if cmake is called with -DCMAKE_BUILD_TYPE=PROFILE
set(CMAKE_C_FLAGS_PROFILE --coverage)
set(CMAKE_CXX_FLAGS_PROFILE --coverage)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(LIB_SOURCE_FILES company.c)
add_library(company STATIC ${LIB_SOURCE_FILES})

add_executable(main main.c)
target_link_libraries(main company)

enable_testing()
find_package(GTest REQUIRED)

include_directories(${GTEST_INCLUDE_DIRS})
add_executable(company_test company_test.cpp)
target_link_libraries(company_test ${GTEST_LIBRARIES} company)