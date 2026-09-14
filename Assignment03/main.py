# File: main.py
# Author: Adam Edwards (with help from ChatGPT)
# Date: 9/13/2026
# Purpose:
# Run the Assignment 03 simple shell parser interactively.

from tokenizer import tokenize
from parser import Parser


def main():
    print("Simple Shell Parser")
    print("Type exit to quit.")

    while True:
        command = input("> ")

        if command.lower() == "exit":
            break

        if not command.strip():
            continue

        try:
            tokens = tokenize(command)
            parser = Parser(tokens)
            ast = parser.parse()

            print(ast)

        except (RuntimeError, SyntaxError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()