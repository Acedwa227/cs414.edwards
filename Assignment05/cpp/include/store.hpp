/* File: store.hpp
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Declare the Store class, which owns the key-value map and
   provides set, get, remove, list, save, and load.

   Template: Operation names come from the Assignment 05 handout.
   AI Help: Claude helped plan and draft the class interface, including
   returning std::optional from get and a copy of the pairs from list. 
*/

#pragma once

#include <map>
#include <optional>
#include <string>
#include <utility>
#include <vector>

class Store {
public:
    
    void set(const std::string& key, const std::string& value);
        
    std::optional<std::string> get(const std::string& key) const;

    bool remove(const std::string& key);

    std::vector<std::pair<std::string, std::string>> list() const;

    bool save(const std::string& filename) const;
    bool load(const std::string& filename);

private:
    std::map<std::string, std::string> data_;
};