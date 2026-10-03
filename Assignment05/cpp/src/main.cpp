/* File: main.cpp
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Command loop for the C++ key-value store. Reads commands,
   calls the Store operations, and prints results. All console I/O is
   kept in this file.

   AI Help: Claude helped plan and draft the command loop and the
   parsing of each command line. 
*/

#include "store.hpp"

#include <iostream>
#include <optional>
#include <sstream>
#include <string>

int main() {
    Store store;
    std::string line;

    std::cout << "> ";
    while (std::getline(std::cin, line)) {
        std::istringstream words(line);
        std::string command;
        std::string argument;
        words >> command >> argument;

        if (command == "QUIT") {
            break;
        }
        else if (command == "SET") {
            /* the value is the rest of the line, so it can contain spaces */
            std::string value;
            std::getline(words >> std::ws, value);
            if (argument.empty() || value.empty()) {
                std::cout << "usage: SET key value\n";
            }
            else {
                store.set(argument, value);
            }
        }
        else if (command == "GET") {
            std::optional<std::string> value = store.get(argument);
            if (value) {
                std::cout << *value << "\n";
            }
            else {
                std::cout << "key not found\n";
            }
        }
        else if (command == "DELETE") {
            if (!store.remove(argument)) {
                std::cout << "key not found\n";
            }
        }
        else if (command == "LIST") {
            for (const auto& entry : store.list()) {
                std::cout << entry.first << " = " << entry.second << "\n";
            }
        }
        else if (command == "SAVE") {
            if (!store.save(argument)) {
                std::cout << "could not open file\n";
            }
        }
        else if (command == "LOAD") {
            if (!store.load(argument)) {
                std::cout << "could not open file\n";
            }
        }
        else if (!command.empty()) {
            std::cout << "unknown command\n";
        }

        std::cout << "> ";
    }

    return 0;
}