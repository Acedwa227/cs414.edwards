# File: question3.md
# Author: Adam Edwards (with help from ChatGPT)
# Date: 8/31/2026
# Purpose:
# Build parse trees for arithmetic expressions using the provided
# context-free grammar.

Expr   -> Expr + Term
       | Expr - Term
       | Term

Term   -> Term * Factor
       | Term / Factor
       | Factor

Factor -> ( Expr )
       | number
       | identifier


(a+(b*c)/2)

Expr
└── Term
    └── Factor
        ├── (
        ├── Expr
        │   ├── Expr
        │   │   └── Term
        │   │       └── Factor
        │   │           └── identifier
        │   │               └── a
        │   ├── +
        │   └── Term
        │       ├── Term
        │       │   └── Factor
        │       │       ├── (
        │       │       ├── Expr
        │       │       │   └── Term
        │       │       │       ├── Term
        │       │       │       │   └── Factor
        │       │       │       │       └── identifier
        │       │       │       │           └── b
        │       │       │       ├── *
        │       │       │       └── Factor
        │       │       │           └── identifier
        │       │       │               └── c
        │       │       └── )
        │       ├── /
        │       └── Factor
        │           └── number
        │               └── 2
        └── )

a*(3+b)*4

Expr
└── Term
    ├── Term
    │   ├── Term
    │   │   └── Factor
    │   │       └── identifier
    │   │           └── a
    │   ├── *
    │   └── Factor
    │       ├── (
    │       ├── Expr
    │       │   ├── Expr
    │       │   │   └── Term
    │       │   │       └── Factor
    │       │   │           └── number
    │       │   │               └── 3
    │       │   ├── +
    │       │   └── Term
    │       │       └── Factor
    │       │           └── identifier
    │       │               └── b
    │       └── )
    ├── *
    └── Factor
        └── number
            └── 4

42\*c+3\*(a+b)

Expr
├── Expr
│   └── Term
│       ├── Term
│       │   └── Factor
│       │       └── number
│       │           └── 42
│       ├── *
│       └── Factor
│           └── identifier
│               └── c
├── +
└── Term
    ├── Term
    │   └── Factor
    │       └── number
    │           └── 3
    ├── *
    └── Factor
        ├── (
        ├── Expr
        │   ├── Expr
        │   │   └── Term
        │   │       └── Factor
        │   │           └── identifier
        │   │               └── a
        │   ├── +
        │   └── Term
        │       └── Factor
        │           └── identifier
        │               └── b
        └── )