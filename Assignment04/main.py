# File: main.py
# Author: Adam Edwards
# Date: 9/21/2026
# Purpose: Run the Assignment 04 simple shell parser.
#
# Template: Adapted from Dr. Lewis's Module02PartF example usage.
# AI Help: ChatGPT helped add the interactive input loop, error handling,
# and formatted AST output. Claude helped add the symbol table for
# shell variables and the symbol table printout.

from tokenizer import tokenize
from parser import Parser


def print_symbol_table(symbol_table):
    print("Symbol table:")

    if not symbol_table:
        print("  (empty)")

    for name, value in symbol_table.items():
        print(f"  {name} = {value}")


def main():
    print("Simple Shell Parser")
    print("Type exit to quit.")

    symbol_table = {}

    while True:
        command = input("> ")

        if command.lower() == "exit":
            break

        if not command.strip():
            continue

        try:
            tokens = tokenize(command)
            parser = Parser(tokens, symbol_table)
            ast = parser.parse()

            print(ast.pretty())
            print_symbol_table(symbol_table)

        except (RuntimeError, SyntaxError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()