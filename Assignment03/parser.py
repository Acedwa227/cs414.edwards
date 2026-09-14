# File: parser.py
# Author: Adam Edwards (with help from ChatGPT)
# Date: 9/13/2026
# Purpose:
# Parse tokenized simple-shell commands and build an AST.
#
# EBNF Grammar:
# command = ls_command | cd_comand | cat_command | print_command | exec_command;
#  ls_command = "ls", [folder];
#  cd_command = "cd", [path];
#  cat_command = "cat", filename;
#  print_command = "print", filename;
#  exec_command = "exec", filename; 
#  filename = name, ".", extension;
#  name = letter, letter, letter, letter, letter, letter, letter, letter;
#  extension = letter, letter, letter;
#  letter = upper_case | lower_case;
#  upper_case = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z";
# lower_case = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z";
#  folder = folder_char, [folder_char], [folder_char], [folder_char], [folder_char], [folder_char], [folder_char], [folder_char];
#  folder_char = letter | digit;
#  digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
#  path = folder, {separator, folder};
#  separator = "\"

from dataclasses import dataclass
from typing import List, Optional

from tokenizer import Token, TokenType


@dataclass
class CommandNode:
    command: str
    argument: Optional[str] = None


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def expect(self, expected_type: TokenType, value: str = None) -> Token:
        tok = self.peek()

        if tok[0] != expected_type or (
            value is not None and tok[1] != value
        ):
            raise SyntaxError(
                f"Expected {expected_type} {value}, got {tok}"
            )

        self.advance()
        return tok

    def parse(self) -> CommandNode:
        command = self.parse_command()
        self.expect(TokenType.EOF)
        return command

    def parse_command(self) -> CommandNode:
        tok = self.peek()

        if tok[0] != TokenType.KEYWORD:
            raise SyntaxError(f"Expected command, got {tok}")

        if tok[1] == "ls":
            return self.parse_ls_command()

        if tok[1] == "cd":
            return self.parse_cd_command()

        if tok[1] == "cat":
            return self.parse_cat_command()

        if tok[1] == "print":
            return self.parse_print_command()

        if tok[1] == "exec":
            return self.parse_exec_command()

        raise SyntaxError(f"Unknown command: {tok[1]}")

    def parse_ls_command(self) -> CommandNode:
        self.expect(TokenType.KEYWORD, "ls")

        if self.peek()[0] == TokenType.EOF:
            return CommandNode("ls")

        folder = self.parse_folder()
        return CommandNode("ls", folder)

    def parse_cd_command(self) -> CommandNode:
        self.expect(TokenType.KEYWORD, "cd")

        if self.peek()[0] == TokenType.EOF:
            return CommandNode("cd")

        path = self.parse_path()
        return CommandNode("cd", path)

    def parse_cat_command(self) -> CommandNode:
        self.expect(TokenType.KEYWORD, "cat")
        filename = self.parse_filename()
        return CommandNode("cat", filename)

    def parse_print_command(self) -> CommandNode:
        self.expect(TokenType.KEYWORD, "print")
        filename = self.parse_filename()
        return CommandNode("print", filename)

    def parse_exec_command(self) -> CommandNode:
        self.expect(TokenType.KEYWORD, "exec")
        filename = self.parse_filename()
        return CommandNode("exec", filename)

    def parse_filename(self) -> str:
        name = self.parse_name()
        self.expect(TokenType.DOT)
        extension = self.parse_extension()

        return f"{name}.{extension}"

    def parse_name(self) -> str:
        word = self.parse_word()

        if len(word) != 8 or not word.isalpha():
            raise SyntaxError(
                "Filename name must contain exactly 8 letters"
            )

        return word

    def parse_extension(self) -> str:
        word = self.parse_word()

        if len(word) != 3 or not word.isalpha():
            raise SyntaxError(
                "Filename extension must contain exactly 3 letters"
            )

        return word

    def parse_folder(self) -> str:
        folder = self.parse_word()

        if len(folder) > 8 or not folder.isalnum():
            raise SyntaxError(
                "Folder name must contain 1 to 8 letters or digits"
            )

        return folder

    def parse_path(self) -> str:
        folders = [self.parse_folder()]

        while self.peek()[0] == TokenType.SEPARATOR:
            self.expect(TokenType.SEPARATOR)
            folders.append(self.parse_folder())

        return "\\".join(folders)

    def parse_word(self) -> str:
        tok = self.peek()

        if tok[0] not in {TokenType.WORD, TokenType.KEYWORD}:
            raise SyntaxError(f"Expected word, got {tok}")

        self.advance()
        return tok[1]