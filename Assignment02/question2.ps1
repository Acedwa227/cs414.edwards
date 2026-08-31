#
# File:   question2.ps1
# Author: Adam Edwards (with help from ChatGPT)
# Date:   8/31/2026
# Purpose:
# Test regular expressions for C++ identifiers, U.S. phone numbers,
# floating-point numbers, and binary palindromes.
#

# 1. C++ Identifiers

$pattern = '^[A-Za-z_][A-Za-z0-9_]*$'

$tests = @(
    'myVariable'
    '_count2'
    '2badName'
)

foreach ($test in $tests) {
    "$test -> $($test -match $pattern)"
}

# 2. Valid U.S. Phone Numbers

$pattern = '^(\([0-9]{3}\) [0-9]{3}-[0-9]{4}|[0-9]{3}-[0-9]{3}-[0-9]{4})$'

$tests = @(
    '(256) 555-1234'
    '256-555-1234'
    '256-55-1234'
)

foreach ($test in $tests) {
    "$test -> $($test -match $pattern)"
}

# 3. Floating-Point Numbers

$pattern = '^[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?$'

$tests = @(
    '3.14'
    '-1.0E-6'
    '+42'
    '12.3.4'
)

foreach ($test in $tests) {
    "$test -> $($test -match $pattern)"
}

# 4. Binary Palindromes of Length 3 or 4

$pattern = '^([01])([01])\2\1$|^([01])[01]\3$'

$tests = @(
    '101'
    '0110'
    '0101'
    '111'
)

foreach ($test in $tests) {
    "$test -> $($test -match $pattern)"
}