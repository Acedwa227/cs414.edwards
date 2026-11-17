/*
File: main.cpp
Author: Adam Edwards
Date: 11/15/2026
Purpose: Counts lines containing a search string using FileHandle (RAII).
         Runs tests T1-T7 from Assignment 08.
Usage: .\cpp\build\Debug\assignment08.exe data
Template: Assignment 08 handout (Parts A1 and A3).
AI Help: Claude (Anthropic) helped with the line reader, tests,
         and comments.
*/

#include "file_handle.hpp"

#include <cstdio>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>

// Reads a complete line, including lines larger than the buffer.
bool read_line(FILE* file, std::string& line)
{
    char buffer[4096];
    line.clear();
    bool read_something = false;

    while (std::fgets(buffer, sizeof buffer, file)) {
        read_something = true;
        line += buffer;
        if (!line.empty() && line.back() == '\n') {
            line.pop_back();
            return true;
        }
    }

    return read_something;
}

int count_matches_cpp(const std::string& path,
    const std::string& needle,
    bool fail_after_first_line = false)
{
    // Reject an empty search string.
    if (needle.empty()) {
        throw std::invalid_argument("search string must not be empty");
    }

    // FileHandle closes the file automatically.
    FileHandle file(path);

    std::string line;
    int count = 0;
    while (read_line(file.get(), line)) {
        if (line.find(needle) != std::string::npos) {
            ++count;
        }

        // Simulate an exception after the first line.
        if (fail_after_first_line) {
            throw std::runtime_error("simulated failure");
        }
    }
    return count;
}

// Runs a test and displays the result.
void run_test(const std::string& name,
    const std::string& path,
    const std::string& needle,
    bool fail_after_first_line,
    const std::string& expected)
{
    std::cout << "\n" << name << ": path=" << path
        << " needle=\"" << needle << "\""
        << " fail=" << (fail_after_first_line ? "true" : "false")
        << "\n  expected: " << expected << "\n";
    try {
        int result = count_matches_cpp(path, needle, fail_after_first_line);
        std::cout << "  result:   returned " << result << "\n";
    }
    catch (const std::exception& e) {
        std::cout << "  result:   exception: " << e.what() << "\n";
    }
}

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cerr << "usage: assignment08 <data folder>\n";
        return 1;
    }
    std::string data = argv[1];

    run_test("T1", data + "/sample.txt", "red", false,
        "return 2; close file");
    run_test("T2", data + "/sample.txt", "orange", false,
        "return 0; close file");
    run_test("T3", data + "/empty.txt", "red", false,
        "return 0; close file");
    run_test("T4", data + "/missing.txt", "red", false,
        "opening failure; nothing to release");
    run_test("T5", data + "/sample.txt", "red", true,
        "exception; close file");
    run_test("T6", data + "/sample.txt", "", false,
        "rejected before opening file");
    run_test("T7", data + "/long_line.txt", "red", false,
        "return 1; close file");

    return 0;
}
