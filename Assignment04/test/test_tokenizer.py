# File: test_tokenizer.py
# Author: Adam Edwards (with help from ChatGPT and Claude)
# Date: 9/21/2026
# Purpose:
# Unit tests for the Assignment 04 tokenizer.
# AI Help: ChatGPT helped with the Assignment 03 tests. Claude helped
# plan and draft the tests for variables, set/echo, and expressions.

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

    def test_set_plain_value(self):
        self.assertEqual(
            tokenize("set $x = hello"),
            [
                (TokenType.KEYWORD, "set"),
                (TokenType.VARIABLE, "$x"),
                (TokenType.EQ, "="),
                (TokenType.WORD, "hello"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_set_expression(self):
        self.assertEqual(
            tokenize("set $x = 1 + 2 * 3"),
            [
                (TokenType.KEYWORD, "set"),
                (TokenType.VARIABLE, "$x"),
                (TokenType.EQ, "="),
                (TokenType.WORD, "1"),
                (TokenType.OPERATOR, "+"),
                (TokenType.WORD, "2"),
                (TokenType.OPERATOR, "*"),
                (TokenType.WORD, "3"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_set_parentheses(self):
        self.assertEqual(
            tokenize("set $x = (1 + 2) * 3"),
            [
                (TokenType.KEYWORD, "set"),
                (TokenType.VARIABLE, "$x"),
                (TokenType.EQ, "="),
                (TokenType.LPAREN, "("),
                (TokenType.WORD, "1"),
                (TokenType.OPERATOR, "+"),
                (TokenType.WORD, "2"),
                (TokenType.RPAREN, ")"),
                (TokenType.OPERATOR, "*"),
                (TokenType.WORD, "3"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_all_operators(self):
        self.assertEqual(
            tokenize("+ - * /"),
            [
                (TokenType.OPERATOR, "+"),
                (TokenType.OPERATOR, "-"),
                (TokenType.OPERATOR, "*"),
                (TokenType.OPERATOR, "/"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_set_without_spaces(self):
        self.assertEqual(
            tokenize("set $x=1+2"),
            [
                (TokenType.KEYWORD, "set"),
                (TokenType.VARIABLE, "$x"),
                (TokenType.EQ, "="),
                (TokenType.WORD, "1"),
                (TokenType.OPERATOR, "+"),
                (TokenType.WORD, "2"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_echo(self):
        self.assertEqual(
            tokenize("echo $x"),
            [
                (TokenType.KEYWORD, "echo"),
                (TokenType.VARIABLE, "$x"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_variable_with_digits(self):
        self.assertEqual(
            tokenize("echo $Var2"),
            [
                (TokenType.KEYWORD, "echo"),
                (TokenType.VARIABLE, "$Var2"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_variable_in_cat(self):
        self.assertEqual(
            tokenize("cat $file"),
            [
                (TokenType.KEYWORD, "cat"),
                (TokenType.VARIABLE, "$file"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_variable_in_path(self):
        self.assertEqual(
            tokenize(r"cd docs\$sub"),
            [
                (TokenType.KEYWORD, "cd"),
                (TokenType.WORD, "docs"),
                (TokenType.SEPARATOR, "\\"),
                (TokenType.VARIABLE, "$sub"),
                (TokenType.EOF, "EOF"),
            ],
        )

    def test_bare_dollar_sign(self):
        with self.assertRaises(RuntimeError):
            tokenize("echo $")

    def test_unexpected_character(self):
        with self.assertRaises(RuntimeError):
            tokenize("set $x = 5 #")

    def test_underscore_not_allowed_in_variable(self):
        with self.assertRaises(RuntimeError):
            tokenize("echo $my_var")


if __name__ == "__main__":
    unittest.main()