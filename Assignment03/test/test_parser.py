# File: test_parser.py
# Author: Adam Edwards (with help from ChatGPT)
# Date: 9/13/2026
# Purpose:
# Unit tests for the Assignment 03 recursive descent parser.

import unittest

from parser import CommandNode, Parser
from tokenizer import tokenize


class TestParser(unittest.TestCase):

    def parse(self, command):
        tokens = tokenize(command)
        parser = Parser(tokens)
        return parser.parse()

    # Valid command tests

    def test_ls(self):
        self.assertEqual(
            self.parse("ls docs"),
            CommandNode("ls", "docs"),
        )

    def test_ls_no_folder(self):
        self.assertEqual(
            self.parse("ls"),
            CommandNode("ls"),
        )

    def test_cd(self):
        self.assertEqual(
            self.parse(r"cd docs\cs414"),
            CommandNode("cd", r"docs\cs414"),
        )

    def test_cd_no_path(self):
        self.assertEqual(
            self.parse("cd"),
            CommandNode("cd"),
        )

    def test_cat(self):
        self.assertEqual(
            self.parse("cat TESTFILE.txt"),
            CommandNode("cat", "TESTFILE.txt"),
        )

    def test_print(self):
        self.assertEqual(
            self.parse("print ReportAA.txt"),
            CommandNode("print", "ReportAA.txt"),
        )

    def test_exec(self):
        self.assertEqual(
            self.parse("exec RUNAFILE.EXE"),
            CommandNode("exec", "RUNAFILE.EXE"),
        )

    # Invalid command tests

    def test_filename_too_short(self):
        with self.assertRaises(SyntaxError):
            self.parse("cat TEST.txt")

    def test_extension_wrong_length(self):
        with self.assertRaises(SyntaxError):
            self.parse("cat TESTFILE.text")

    def test_folder_too_long(self):
        with self.assertRaises(SyntaxError):
            self.parse("ls documents")

    def test_missing_filename(self):
        with self.assertRaises(SyntaxError):
            self.parse("cat")

    def test_extra_input(self):
        with self.assertRaises(SyntaxError):
            self.parse("cat TESTFILE.txt extra")


if __name__ == "__main__":
    unittest.main()