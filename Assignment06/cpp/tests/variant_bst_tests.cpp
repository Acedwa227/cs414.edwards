
/*
File: variant_bst_tests.cpp
Author: Adam Edwards
Date: 10/18/2026
Purpose: Tests BST traversals with empty trees, single values,
         sample trees, duplicates, sorted input, and negative numbers.
Template: Based on the Google Test setup from previous assignments.
AI Help: Claude assisted with the original test cases and expected results.
         ChatGPT assisted with converting the tests to Google Test.
*/

#include "variant_bst.hpp"
#include <gtest/gtest.h>
#include <vector>

// Builds a tree from a list of integers
VariantBST build(const std::vector<int>& numbers) {
    VariantBST tree;
    for (int number : numbers) {
        tree.insert(number);
    }
    return tree;
}

// Test an empty tree
TEST(VariantBSTTest, EmptyTree) {
    VariantBST tree;
    EXPECT_TRUE(tree.inorder().empty());
    EXPECT_TRUE(tree.preorder().empty());
    EXPECT_TRUE(tree.postorder().empty());
}

// Test a tree with one value
TEST(VariantBSTTest, SingleValue) {
    VariantBST tree = build({ 42 });
    std::vector<int> expected = { 42 };

    EXPECT_EQ(tree.inorder(), expected);
    EXPECT_EQ(tree.preorder(), expected);
    EXPECT_EQ(tree.postorder(), expected);
}

// Test the sample tree from Module 05
TEST(VariantBSTTest, SampleTree) {
    VariantBST tree = build({ 5, 2, 8, 1, 3, 7, 9 });

    EXPECT_EQ(tree.inorder(), (std::vector<int>{ 1, 2, 3, 5, 7, 8, 9 }));
    EXPECT_EQ(tree.preorder(), (std::vector<int>{ 5, 2, 1, 3, 8, 7, 9 }));
    EXPECT_EQ(tree.postorder(), (std::vector<int>{ 1, 3, 2, 7, 9, 8, 5 }));
}

// Test that duplicate values are ignored
TEST(VariantBSTTest, DuplicatesIgnored) {
    VariantBST tree = build({ 5, 2, 5, 8, 2, 8 });

    EXPECT_EQ(tree.inorder(), (std::vector<int>{ 2, 5, 8 }));
    EXPECT_EQ(tree.preorder(), (std::vector<int>{ 5, 2, 8 }));
    EXPECT_EQ(tree.postorder(), (std::vector<int>{ 2, 8, 5 }));
}

// Test sorted input that creates a right-leaning tree
TEST(VariantBSTTest, SortedInput) {
    VariantBST tree = build({ 1, 2, 3, 4, 5 });

    EXPECT_EQ(tree.inorder(), (std::vector<int>{ 1, 2, 3, 4, 5 }));
    EXPECT_EQ(tree.preorder(), (std::vector<int>{ 1, 2, 3, 4, 5 }));
    EXPECT_EQ(tree.postorder(), (std::vector<int>{ 5, 4, 3, 2, 1 }));
}

// Test a tree containing negative numbers
TEST(VariantBSTTest, NegativeNumbers) {
    VariantBST tree = build({ 0, -5, 10, -2 });

    EXPECT_EQ(tree.inorder(), (std::vector<int>{ -5, -2, 0, 10 }));
    EXPECT_EQ(tree.preorder(), (std::vector<int>{ 0, -5, -2, 10 }));
    EXPECT_EQ(tree.postorder(), (std::vector<int>{ -2, -5, 10, 0 }));
}
