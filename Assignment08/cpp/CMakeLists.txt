# File: CMakeLists.txt
# Author: Adam Edwards
# Date: 11/15/2026
# Purpose: Builds the Assignment 08 C++ program (FileHandle RAII demo).
# AI Help: Claude (Anthropic) helped write this build file.

cmake_minimum_required(VERSION 3.16)
project(Assignment08 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(assignment08 main.cpp file_handle.cpp file_handle.hpp)

# The assignment requires std::fopen. MSVC warns that fopen is "unsafe"
# (C4996) and suggests fopen_s, so turn that warning off on MSVC only.
if(MSVC)
    target_compile_definitions(assignment08 PRIVATE _CRT_SECURE_NO_WARNINGS)
    target_compile_options(assignment08 PRIVATE /W4)
else()
    target_compile_options(assignment08 PRIVATE -Wall -Wextra)
endif()