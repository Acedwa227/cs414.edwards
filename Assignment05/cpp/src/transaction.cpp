/* File: transaction.cpp
   Author: Adam Edwards
   Date: 10/2/2026
   Purpose: Implement Transaction. The constructor saves a backup of the
   store and the destructor restores it if commit() was never called (RAII).

   AI Help: Claude helped plan and draft the constructor, commit, and
   destructor. 
*/

#include "transaction.hpp"

Transaction::Transaction(Store& store) : store_(store), backup_(store) {
}

void Transaction::commit() {
    committed_ = true;
}

Transaction::~Transaction() {
    /* never committed, so put the store back the way it was */
    if (!committed_) {
        store_ = backup_;
    }
}