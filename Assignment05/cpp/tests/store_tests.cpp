/* File: store_tests.cpp
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Tests for the C++ store: set, get, remove, an aborted and a
   committed transaction, and save followed by load.

   Template: Transaction scenario (x = 10, set x 20, set y 30, abort)
   comes from the Assignment 05 handout.
   AI Help: Claude helped plan and draft the check function and the
   test cases. 
*/

#include "store.hpp"
#include "transaction.hpp"

#include <iostream>
#include <string>

int failures = 0;

void check(bool condition, const std::string& name) {
    if (condition) {
        std::cout << "PASS: " << name << "\n";
    }
    else {
        std::cout << "FAIL: " << name << "\n";
        failures = failures + 1;
    }
}

void test_set_and_get() {
    Store store;
    store.set("name", "Ada");
    check(store.get("name") == "Ada", "set then get returns the value");

    store.set("name", "Grace");
    check(store.get("name") == "Grace", "set on an existing key replaces the value");

    check(!store.get("missing").has_value(), "get on a missing key returns nothing");
}

void test_remove() {
    Store store;
    store.set("name", "Ada");
    check(store.remove("name"), "remove on an existing key returns true");
    check(!store.get("name").has_value(), "removed key is gone");
    check(!store.remove("name"), "remove on a missing key returns false");
}

void test_transaction_abort() {
    Store store;
    store.set("x", "10");
    {
        Transaction tx{ store };
        store.set("x", "20");
        store.set("y", "30");
        /* no commit, so leaving this block rolls the store back */
    }
    check(store.get("x") == "10", "aborted transaction restores x to 10");
    check(!store.get("y").has_value(), "aborted transaction removes y");
}

void test_transaction_commit() {
    Store store;
    store.set("x", "10");
    {
        Transaction tx{ store };
        store.set("x", "20");
        store.set("y", "30");
        tx.commit();
    }
    check(store.get("x") == "20", "committed transaction keeps x as 20");
    check(store.get("y") == "30", "committed transaction keeps y as 30");
}

void test_save_and_load() {
    Store original;
    original.set("name", "Ada");
    original.set("language", "C++");
    check(original.save("test_data.txt"), "save writes the file");

    Store loaded;
    check(loaded.load("test_data.txt"), "load reads the file");
    check(loaded.list() == original.list(), "save then load rebuilds the same data");
}

int main() {
    test_set_and_get();
    test_remove();
    test_transaction_abort();
    test_transaction_commit();
    test_save_and_load();

    if (failures == 0) {
        std::cout << "All tests passed\n";
        return 0;
    }
    std::cout << failures << " test(s) failed\n";
    return 1;
}