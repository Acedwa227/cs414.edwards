/* File: store.cpp
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Implement the Store operations. save and load use
   std::ofstream and std::ifstream so the files close automatically (RAII).

   AI Help: Claude helped plan and draft these functions, including the
   "key value" file format and having load replace the store's contents. 
*/

#include "store.hpp"

#include <fstream>

void Store::set(const std::string& key, const std::string& value) {
    data_[key] = value;
}

std::optional<std::string> Store::get(const std::string& key) const {
    auto it = data_.find(key);
    if (it == data_.end()) {
        return std::nullopt;
    }
    return it->second;
}

bool Store::remove(const std::string& key) {
    return data_.erase(key) > 0;
}

std::vector<std::pair<std::string, std::string>> Store::list() const {
    std::vector<std::pair<std::string, std::string>> pairs;
    for (const auto& entry : data_) {
        pairs.push_back({ entry.first, entry.second });
    }
    return pairs;
}

bool Store::save(const std::string& filename) const {
    std::ofstream file(filename);
    if (!file) {
        return false;
    }
    for (const auto& entry : data_) {
        file << entry.first << " " << entry.second << "\n";
    }
    /* no close() call: the ofstream closes the file when it goes out of scope */
    return true;
}

bool Store::load(const std::string& filename) {
    std::ifstream file(filename);
    if (!file) {
        return false;
    }
    std::map<std::string, std::string> loaded;
    std::string line;
    while (std::getline(file, line)) {
        std::size_t space = line.find(' ');
        if (space == std::string::npos) {
            continue;
        }
        loaded[line.substr(0, space)] = line.substr(space + 1);
    }
    data_ = loaded;
    return true;
}