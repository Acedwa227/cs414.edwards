
/*
File: main.cpp
Author: Adam Edwards
Date: 10/18/2026
Purpose: Demonstrates the VariantBST by inserting integers
         from a file or default list and printing the traversals.
AI Help: Claude assisted with planning and drafting the program.
*/

#include "variant_bst.hpp"

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// Prints the values for each traversal
void print_values(const std::string& label, const std::vector<int>& values) {
    std::cout << label;
    for (int value : values) {
        std::cout << " " << value;
    }
    std::cout << "\n";
}

int main(int argc, char* argv[]) {
    std::vector<int> numbers;

    // Read integers from a file if provided
    if (argc > 1) {
        std::ifstream input(argv[1]);
        if (!input) {
            std::cout << "could not open file " << argv[1] << "\n";
            return 1;
        }
        int number;
        while (input >> number) {
            numbers.push_back(number);
        }
    }
    else {
        // Default values from Module 05 Part C
        numbers = { 5, 2, 8, 1, 3, 7, 9 };
    }

    // Build the binary search tree
    VariantBST tree;
    for (int number : numbers) {
        tree.insert(number);
    }

    // Display the results
    print_values("Inserted: ", numbers);
    print_values("Inorder:  ", tree.inorder());
    print_values("Preorder: ", tree.preorder());
    print_values("Postorder:", tree.postorder());

    return 0;
}
