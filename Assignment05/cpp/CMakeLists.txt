# File: CMakeLists.txt
# Author: Adam Edwards
# Date: 10/2/2026
# Purpose: Build the C++ key-value store program (kvstore) and its
# test program (store_tests) using C++20.
#
# Template: Follows the add_executable style of the CMake examples in
# Dr. Lewis's Module02PartH.
# AI Help: Claude helped plan and draft this build file.

cmake_minimum_required(VERSION 3.16)
project(kvstore CXX)

# The handout asks for C++20 or later.
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# The interactive program.
add_executable(kvstore
  src/main.cpp
  src/store.cpp
  src/transaction.cpp
)
target_include_directories(kvstore PRIVATE include)

# The test program reuses the same store code with its own main().
add_executable(store_tests
  tests/store_tests.cpp
  src/store.cpp
  src/transaction.cpp
)
target_include_directories(store_tests PRIVATE include)