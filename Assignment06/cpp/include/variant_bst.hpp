/*
File: variant_bst.hpp
Author: Adam Edwards
Date: 10/18/2026
Purpose: Defines a binary search tree using std::variant to
         represent Empty and Node, similar to OCaml.
Template: Based on the AST example in Assignment 06.
AI Help: Claude assisted with the type structure and class interface.
*/

#pragma once

#include <memory>
#include <variant>
#include <vector>

// Tree is declared first so Node can hold pointers to it. 
struct Tree;

// Represents an empty tree
struct Empty {};

// Represents a node with a value and two subtrees
struct Node {
    int value;
    std::unique_ptr<Tree> left;
    std::unique_ptr<Tree> right;
};

// Wraps the variant to allow recursive tree references
struct Tree {
    std::variant<Empty, Node> node;
};

class VariantBST {
public:
    // Insert a value, ignoring duplicates
    void insert(int value);

    // Each traversal returns the values in the order they were visited. 
    std::vector<int> inorder() const;
    std::vector<int> preorder() const;
    std::vector<int> postorder() const;

private:
    // Root of the tree, initially Empty
    Tree root;
};