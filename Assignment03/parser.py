# File: parser.py
# Author: Adam Edwards
# Date: 9/13/2026
# Purpose: Parse Assignment 03 shell tokens and build an AST.
#
# Template: Adapted from Dr. Lewis's Module02PartF recursive-descent
# parser example.
# AI Help: ChatGPT helped adapt the parser, validation, and AST
# construction to the Assignment 03 grammar.

# EBNF Grammar:
#
# command = ls_command | cd_command | cat_command | print_command | exec_command;
#
# ls_command = "ls", [folder];
# cd_command = "cd", [path];
# cat_command = "cat", filename;
# print_command = "print", filename;
# exec_command = "exec", filename;
#
# filename = name, ".", extension;
#
# name = letter, letter, letter, letter, letter, letter, letter, letter;
#
# extension = letter, letter, letter;
#
# letter = upper_case | lower_case;
#
# upper_case = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I"
#            | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R"
#            | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z";
#
# lower_case = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i"
#            | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r"
#            | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z";
#
# folder = folder_char, [folder_char], [folder_char], [folder_char],
#          [folder_char], [folder_char], [folder_char], [folder_char];
#
# folder_char = letter | digit;
#
# digit = "0" | "1" | "2" | "3" | "4"
#       | "5" | "6" | "7" | "8" | "9";
#
# path = folder, {separator, folder};
#
# separator = "\";

import re
from dataclasses import dataclass, field
from typing import List, Optional

from tokenizer import Token, TokenType


@dataclass
class ASTNode:
    label: str
    children: List["ASTNode"] = field(default_factory=list)

    def pretty(self, indent: int = 0) -> str:
        lines = ["  " * indent + self.label]

        for child in self.children:
            lines.append(child.pretty(indent + 1))

        return "\n".join(lines)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def expect(
        self,
        expected_type: TokenType,
        value: Optional[str] = None
    ) -> Token:
        tok = self.peek()

        if tok[0] != expected_type or (
            value is not None and tok[1] != value
        ):
            raise SyntaxError(
                f"Expected {expected_type.name}"
                + (f" '{value}'" if value is not None else "")
                + f", got {tok}"
            )

        self.advance()
        return tok

    def parse(self) -> ASTNode:
        ast = self.parse_command()
        self.expect(TokenType.EOF)
        return ast

    def parse_command(self) -> ASTNode:
        match self.peek():
            case (TokenType.KEYWORD, "ls"):
                return self.parse_ls_command()

            case (TokenType.KEYWORD, "cd"):
                return self.parse_cd_command()

            case (TokenType.KEYWORD, "cat"):
                return self.parse_cat_command()

            case (TokenType.KEYWORD, "print"):
                return self.parse_print_command()

            case (TokenType.KEYWORD, "exec"):
                return self.parse_exec_command()

            case _:
                raise SyntaxError(
                    f"Expected command, got {self.peek()}"
                )

    def parse_ls_command(self) -> ASTNode:
        self.expect(TokenType.KEYWORD, "ls")

        if self.peek()[0] == TokenType.EOF:
            return ASTNode("ls")

        folder = self.parse_folder()

        return ASTNode(
            "ls",
            [ASTNode(folder)]
        )

    def parse_cd_command(self) -> ASTNode:
        self.expect(TokenType.KEYWORD, "cd")

        if self.peek()[0] == TokenType.EOF:
            return ASTNode("cd")

        path = self.parse_path()

        return ASTNode(
            "cd",
            [path]
        )

    def parse_cat_command(self) -> ASTNode:
        self.expect(TokenType.KEYWORD, "cat")
        filename = self.parse_filename()

        return ASTNode(
            "cat",
            [filename]
        )

    def parse_print_command(self) -> ASTNode:
        self.expect(TokenType.KEYWORD, "print")
        filename = self.parse_filename()

        return ASTNode(
            "print",
            [filename]
        )

    def parse_exec_command(self) -> ASTNode:
        self.expect(TokenType.KEYWORD, "exec")
        filename = self.parse_filename()

        return ASTNode(
            "exec",
            [filename]
        )

    def parse_filename(self) -> ASTNode:
        name = self.parse_word()

        if re.fullmatch(r"[A-Za-z]{8}", name) is None:
            raise SyntaxError(
                "Filename name must contain exactly 8 letters"
            )

        self.expect(TokenType.DOT)

        extension = self.parse_word()

        if re.fullmatch(r"[A-Za-z]{3}", extension) is None:
            raise SyntaxError(
                "Filename extension must contain exactly 3 letters"
            )

        return ASTNode(
            "Filename",
            [
                ASTNode(name),
                ASTNode(extension),
            ],
        )

    def parse_folder(self) -> str:
        folder = self.parse_word()

        if re.fullmatch(r"[A-Za-z0-9]{1,8}", folder) is None:
            raise SyntaxError(
                "Folder name must contain 1 to 8 letters or digits"
            )

        return folder

    def parse_path(self) -> ASTNode:
        folders = [
            ASTNode(self.parse_folder())
        ]

        while self.peek()[0] == TokenType.SEPARATOR:
            self.expect(TokenType.SEPARATOR)
            folders.append(
                ASTNode(self.parse_folder())
            )

        return ASTNode(
            "path",
            folders
        )

    def parse_word(self) -> str:
        tok = self.peek()

        if tok[0] not in {
            TokenType.WORD,
            TokenType.KEYWORD,
        }:
            raise SyntaxError(
                f"Expected word, got {tok}"
            )

        self.advance()
        return tok[1]