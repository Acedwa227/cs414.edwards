
cmake_minimum_required(VERSION 3.16)

project(variant_bst)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Headers
include_directories(${CMAKE_SOURCE_DIR}/include)

# --- Main program ---
add_executable(variant_bst
    src/main.cpp
    src/variant_bst.cpp
)

# --- Google Test ---
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.13.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# --- Test program ---
add_executable(variant_bst_tests
    tests/variant_bst_tests.cpp
    src/variant_bst.cpp
)

target_link_libraries(variant_bst_tests PRIVATE GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(variant_bst_tests)
