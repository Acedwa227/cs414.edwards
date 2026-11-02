# File: CMakeLists.txt
# Author: Adam Edwards
# Date: 2026-11-01
# Purpose: Builds the two C++ diamond-inheritance programs for Assignment 07 (oo-comparison).
# Template: Based on the CMake sketch in Module 02 Part H (cmake_minimum_required, project, CMAKE_CXX_STANDARD, add_executable).
# AI Help: Claude (Anthropic) helped drafted this build file.

cmake_minimum_required(VERSION 3.16)
project(OOComparison CXX)

# The assignment requires C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# One executable per program
add_executable(nonvirtual_diamond nonvirtual_diamond.cpp)
add_executable(virtual_diamond virtual_diamond.cpp)