# File: test_tokenizer.py
# Author: Adam Edwards (with help from ChatGPT)
# Date: 9/13/2026
# Purpose:
# Unit tests for the Assignment 03 tokenizer.

import unittest

from tokenizer import TokenType, tokenize


class TestTokenizer(unittest.TestCase):

    def test_ls(self):
        self.assertEqual(
            tokenize("ls docs"),
            [
                (TokenType.KEYWORD, "ls"),
                (TokenType.WORD, "docs"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_cd(self):
        self.assertEqual(
            tokenize(r"cd docs\cs414"),
            [
                (TokenType.KEYWORD, "cd"),
                (TokenType.WORD, "docs"),
                (TokenType.SEPARATOR, "\\"),
                (TokenType.WORD, "cs414"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_cat(self):
        self.assertEqual(
            tokenize("cat TESTFILE.txt"),
            [
                (TokenType.KEYWORD, "cat"),
                (TokenType.WORD, "TESTFILE"),
                (TokenType.DOT, "."),
                (TokenType.WORD, "txt"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_print(self):
        self.assertEqual(
            tokenize("print ReportAA.txt"),
            [
                (TokenType.KEYWORD, "print"),
                (TokenType.WORD, "ReportAA"),
                (TokenType.DOT, "."),
                (TokenType.WORD, "txt"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_exec(self):
        self.assertEqual(
            tokenize("exec RUNAFILE.EXE"),
            [
                (TokenType.KEYWORD, "exec"),
                (TokenType.WORD, "RUNAFILE"),
                (TokenType.DOT, "."),
                (TokenType.WORD, "EXE"),
                (TokenType.EOF, "EOF"),
            ],
        )


if __name__ == "__main__":
    unittest.main()