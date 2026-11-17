/*
File: file_handle.cpp
Author: Adam Edwards
Date: 11/15/2026
Purpose: Implements FileHandle to open and close files using RAII.
Template: Assignment 08 handout (Part A2).
AI Help: Claude (Anthropic) helped with the implementation and comments.
*/

#include "file_handle.hpp"

#include <iostream>
#include <stdexcept>

FileHandle::FileHandle(const std::string& path)
    : file_(std::fopen(path.c_str(), "r")), path_(path)
{
    // Throw an exception if the file cannot be opened.
    if (file_ == nullptr) {
        throw std::runtime_error("cannot open file: " + path);
    }
    std::cerr << "[FileHandle] acquired " << path_ << "\n";
}

FileHandle::~FileHandle() noexcept
{
    // Close the file when the object is destroyed.
    if (file_ != nullptr) {
        std::fclose(file_);
        std::cerr << "[FileHandle] released " << path_ << "\n";
    }
}

FILE* FileHandle::get() const noexcept
{
    return file_;
}
