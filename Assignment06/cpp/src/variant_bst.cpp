
/*
File: variant_bst.cpp
Author: Adam Edwards
Date: 10/18/2026
Purpose: Implements BST insertion and traversals using std::visit
         to handle Empty and Node.
Template: Based on the std::visit example in Assignment 06.
AI Help: Claude assisted with the helper functions and insertion logic.
*/

#include "variant_bst.hpp"

// Combines lambdas for use with std::visit
template <class... Ts>
struct Overloaded : Ts... {
    using Ts::operator()...;
};

template <class... Ts>
Overloaded(Ts...) -> Overloaded<Ts...>;

// Inserts a value into the tree
static void insert_into(Tree& tree, int value) {
    bool found_empty = false;

    std::visit(Overloaded{
        [&found_empty](Empty&) {
            found_empty = true;
        },
        [value](Node& n) {
            if (value < n.value) {
                insert_into(*n.left, value);
            }
            else if (value > n.value) {
                insert_into(*n.right, value);
            }
            // Duplicate values are ignored
        }
        }, tree.node);

    // Create a new node if the tree is empty
    if (found_empty) {
        tree.node = Node{ value, std::make_unique<Tree>(), std::make_unique<Tree>() };
    }
}

// Inorder traversal: left, node, right
static void inorder_walk(const Tree& tree, std::vector<int>& visited) {
    std::visit(Overloaded{
        [](const Empty&) {},
        [&visited](const Node& n) {
            inorder_walk(*n.left, visited);
            visited.push_back(n.value);
            inorder_walk(*n.right, visited);
        }
        }, tree.node);
}

// Preorder traversal: node, left, right
static void preorder_walk(const Tree& tree, std::vector<int>& visited) {
    std::visit(Overloaded{
        [](const Empty&) {},
        [&visited](const Node& n) {
            visited.push_back(n.value);
            preorder_walk(*n.left, visited);
            preorder_walk(*n.right, visited);
        }
        }, tree.node);
}

// Postorder traversal: left, right, node
static void postorder_walk(const Tree& tree, std::vector<int>& visited) {
    std::visit(Overloaded{
        [](const Empty&) {},
        [&visited](const Node& n) {
            postorder_walk(*n.left, visited);
            postorder_walk(*n.right, visited);
            visited.push_back(n.value);
        }
        }, tree.node);
}

// Public BST functions
void VariantBST::insert(int value) {
    insert_into(root, value);
}

std::vector<int> VariantBST::inorder() const {
    std::vector<int> visited;
    inorder_walk(root, visited);
    return visited;
}

std::vector<int> VariantBST::preorder() const {
    std::vector<int> visited;
    preorder_walk(root, visited);
    return visited;
}

std::vector<int> VariantBST::postorder() const {
    std::vector<int> visited;
    postorder_walk(root, visited);
    return visited;
}
