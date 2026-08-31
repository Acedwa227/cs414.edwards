# File: question4.md
# Author: Adam Edwards (with help from ChatGPT)
# Date: 8/31/2026
# Purpose:
# Extend the arithmetic expression grammar to support unary
# plus and minus operators.

Expr   -> Expr + Term
       | Expr - Term
       | Term

Term   -> Term * Factor
       | Term / Factor
       | Factor

Factor -> + Factor
       | - Factor
       | ( Expr )
       | number
       | identifier