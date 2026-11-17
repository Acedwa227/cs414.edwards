/*
File: file_handle.hpp
Author: Adam Edwards
Date: 11/15/2026
Purpose: Declares FileHandle for managing files using RAII.
Template: Assignment 08 handout (Part A2).
AI Help: Claude (Anthropic) helped with the comments and class design.
*/

#ifndef FILE_HANDLE_HPP
#define FILE_HANDLE_HPP

#include <cstdio>
#include <string>

class FileHandle {
public:
    // Opens a file for reading.
    explicit FileHandle(const std::string& path);

    // Closes the file when the object is destroyed.
    ~FileHandle() noexcept;

    // Prevent copying or moving the file handle.
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    FileHandle(FileHandle&&) = delete;
    FileHandle& operator=(FileHandle&&) = delete;

    // Returns the file pointer without transferring ownership.
    FILE* get() const noexcept;

private:
    FILE* file_ = nullptr;
    std::string path_;
};

#endif
