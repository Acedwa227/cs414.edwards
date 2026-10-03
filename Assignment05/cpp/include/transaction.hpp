/* File: transaction.hpp
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Declare the Transaction class, which rolls the store back
   unless commit() is called.

   Template: Interface taken from the example in the Assignment 05 handout.
   AI Help: Claude helped explain the handout's interface and set up
   this header. 
*/

#pragma once

#include "store.hpp"

class Transaction {
public:
    explicit Transaction(Store& store);

    void commit();

    ~Transaction();

private:
    Store& store_;
    Store backup_;
    bool committed_{ false };
};