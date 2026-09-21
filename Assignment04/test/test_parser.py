# File: test_parser.py
# Author: Adam Edwards (with help from ChatGPT and Claude)
# Date: 9/21/2026
# Purpose:
# Unit tests for the Assignment 04 parser.
# AI Help: ChatGPT helped with the Assignment 03 tests. Claude helped
# plan and draft the tests for variables, set/echo, expressions, and the
# symbol table.

import unittest

from parser import ASTNode, Parser
from tokenizer import tokenize


class TestParser(unittest.TestCase):

    def parse(self, command, symbol_table=None):
        tokens = tokenize(command)
        parser = Parser(tokens, symbol_table)
        return parser.parse()

    def test_ls(self):
        self.assertEqual(
            self.parse("ls docs"),
            ASTNode(
                "ls",
                [ASTNode("docs")]
            ),
        )

    def test_ls_no_folder(self):
        self.assertEqual(
            self.parse("ls"),
            ASTNode("ls"),
        )

    def test_cd(self):
        self.assertEqual(
            self.parse(r"cd docs\cs414"),
            ASTNode(
                "cd",
                [
                    ASTNode(
                        "path",
                        [
                            ASTNode("docs"),
                            ASTNode("cs414"),
                        ],
                    )
                ],
            ),
        )

    def test_cd_no_path(self):
        self.assertEqual(
            self.parse("cd"),
            ASTNode("cd"),
        )

    def test_cat(self):
        self.assertEqual(
            self.parse("cat TESTFILE.txt"),
            ASTNode(
                "cat",
                [
                    ASTNode(
                        "Filename",
                        [
                            ASTNode("TESTFILE"),
                            ASTNode("txt"),
                        ],
                    )
                ],
            ),
        )

    def test_print(self):
        self.assertEqual(
            self.parse("print ReportAA.txt"),
            ASTNode(
                "print",
                [
                    ASTNode(
                        "Filename",
                        [
                            ASTNode("ReportAA"),
                            ASTNode("txt"),
                        ],
                    )
                ],
            ),
        )

    def test_exec(self):
        self.assertEqual(
            self.parse("exec RUNAFILE.EXE"),
            ASTNode(
                "exec",
                [
                    ASTNode(
                        "Filename",
                        [
                            ASTNode("RUNAFILE"),
                            ASTNode("EXE"),
                        ],
                    )
                ],
            ),
        )

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

    def test_digit_in_filename(self):
        with self.assertRaises(SyntaxError):
            self.parse("cat TEST1234.txt")

    def test_trailing_separator(self):
        with self.assertRaises(SyntaxError):
            self.parse("cd docs\\")

    # ---- Assignment 04: set and echo ----

    def test_set_terminal(self):
        self.assertEqual(
            self.parse("set $x = hello", {}),
            ASTNode(
                "set",
                [
                    ASTNode("$x"),
                    ASTNode("hello"),
                ],
            ),
        )

    def test_set_expression(self):
        self.assertEqual(
            self.parse("set $x = 1 + 2 * 3", {}),
            ASTNode(
                "set",
                [
                    ASTNode("$x"),
                    ASTNode(
                        "+",
                        [
                            ASTNode("1"),
                            ASTNode(
                                "*",
                                [
                                    ASTNode("2"),
                                    ASTNode("3"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        )

    def test_set_parentheses(self):
        self.assertEqual(
            self.parse("set $x = (1 + 2) * 3", {}),
            ASTNode(
                "set",
                [
                    ASTNode("$x"),
                    ASTNode(
                        "*",
                        [
                            ASTNode(
                                "+",
                                [
                                    ASTNode("1"),
                                    ASTNode("2"),
                                ],
                            ),
                            ASTNode("3"),
                        ],
                    ),
                ],
            ),
        )

    def test_subtraction_is_left_associative(self):
        self.assertEqual(
            self.parse("set $x = 1 - 2 - 3", {}),
            ASTNode(
                "set",
                [
                    ASTNode("$x"),
                    ASTNode(
                        "-",
                        [
                            ASTNode(
                                "-",
                                [
                                    ASTNode("1"),
                                    ASTNode("2"),
                                ],
                            ),
                            ASTNode("3"),
                        ],
                    ),
                ],
            ),
        )

    def test_division_is_left_associative(self):
        self.assertEqual(
            self.parse("set $x = 8 / 4 / 2", {}),
            ASTNode(
                "set",
                [
                    ASTNode("$x"),
                    ASTNode(
                        "/",
                        [
                            ASTNode(
                                "/",
                                [
                                    ASTNode("8"),
                                    ASTNode("4"),
                                ],
                            ),
                            ASTNode("2"),
                        ],
                    ),
                ],
            ),
        )

    def test_echo(self):
        self.assertEqual(
            self.parse("echo $x", {"$x": "5"}),
            ASTNode(
                "echo",
                [ASTNode("$x")]
            ),
        )

    def test_variable_in_expression(self):
        table = {"$a": "1"}

        self.assertEqual(
            self.parse("set $b = $a + 2", table),
            ASTNode(
                "set",
                [
                    ASTNode("$b"),
                    ASTNode(
                        "+",
                        [
                            ASTNode("$a"),
                            ASTNode("2"),
                        ],
                    ),
                ],
            ),
        )

    # ---- Assignment 04: variables in the other commands ----

    def test_variable_in_ls(self):
        self.assertEqual(
            self.parse("ls $d", {"$d": "docs"}),
            ASTNode(
                "ls",
                [ASTNode("$d")]
            ),
        )

    def test_variable_in_cd(self):
        self.assertEqual(
            self.parse(r"cd docs\$d", {"$d": "cs414"}),
            ASTNode(
                "cd",
                [
                    ASTNode(
                        "path",
                        [
                            ASTNode("docs"),
                            ASTNode("$d"),
                        ],
                    )
                ],
            ),
        )

    def test_variable_in_cat(self):
        self.assertEqual(
            self.parse("cat $f", {"$f": "TESTFILE"}),
            ASTNode(
                "cat",
                [ASTNode("$f")]
            ),
        )

    def test_variable_in_print(self):
        self.assertEqual(
            self.parse("print $f", {"$f": "TESTFILE"}),
            ASTNode(
                "print",
                [ASTNode("$f")]
            ),
        )

    def test_variable_in_exec(self):
        self.assertEqual(
            self.parse("exec $f", {"$f": "RUNAFILE"}),
            ASTNode(
                "exec",
                [ASTNode("$f")]
            ),
        )

    def test_undefined_variable_in_cat(self):
        with self.assertRaises(SyntaxError):
            self.parse("cat $f", {})

    # ---- Assignment 04: syntax errors ----

    def test_echo_undefined_variable(self):
        with self.assertRaises(SyntaxError):
            self.parse("echo $y", {})

    def test_set_uses_undefined_variable(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = $y + 1", {})

    def test_set_refers_to_itself_before_defined(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = $x + 1", {})

    def test_set_missing_equals(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x 5", {})

    def test_set_variable_without_dollar(self):
        with self.assertRaises(SyntaxError):
            self.parse("set x = 5", {})

    def test_set_missing_expression(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x =", {})

    def test_set_missing_everything(self):
        with self.assertRaises(SyntaxError):
            self.parse("set", {})

    def test_echo_missing_variable(self):
        with self.assertRaises(SyntaxError):
            self.parse("echo", {})

    def test_echo_without_dollar(self):
        with self.assertRaises(SyntaxError):
            self.parse("echo x", {})

    def test_unbalanced_open_paren(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = (1 + 2", {})

    def test_unbalanced_close_paren(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = 1 + 2)", {})

    def test_empty_parentheses(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = ()", {})

    def test_trailing_operator(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = 1 +", {})

    def test_leading_operator(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = * 2", {})

    def test_two_operators_in_a_row(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = 1 + + 2", {})

    def test_set_extra_input(self):
        with self.assertRaises(SyntaxError):
            self.parse("set $x = 1 2", {})

    # ---- Assignment 04: symbol table ----

    def test_set_adds_to_symbol_table(self):
        table = {}
        self.parse("set $x = 1 + 2 * 3", table)

        self.assertEqual(table, {"$x": "1 + 2 * 3"})

    def test_set_terminal_adds_to_symbol_table(self):
        table = {}
        self.parse("set $name = hello", table)

        self.assertEqual(table, {"$name": "hello"})

    def test_reassignment_updates_value(self):
        table = {}
        self.parse("set $x = 1", table)
        self.parse("set $x = 2 + 3", table)

        self.assertEqual(table, {"$x": "2 + 3"})

    def test_two_variables_in_symbol_table(self):
        table = {}
        self.parse("set $a = 1", table)
        self.parse("set $b = 2", table)

        self.assertEqual(table, {"$a": "1", "$b": "2"})

    def test_variable_defined_then_used(self):
        table = {}
        self.parse("set $a = 1", table)
        self.parse("set $b = $a + 1", table)

        self.assertEqual(table, {"$a": "1", "$b": "$a + 1"})

    def test_echo_does_not_change_symbol_table(self):
        table = {"$x": "5"}
        self.parse("echo $x", table)

        self.assertEqual(table, {"$x": "5"})

    def test_other_commands_do_not_change_symbol_table(self):
        table = {"$f": "TESTFILE"}
        self.parse("cat $f", table)
        self.parse("ls", table)

        self.assertEqual(table, {"$f": "TESTFILE"})

    def test_failed_set_does_not_add_variable(self):
        table = {}

        with self.assertRaises(SyntaxError):
            self.parse("set $x = (1 + 2", table)

        self.assertEqual(table, {})

    def test_failed_set_does_not_change_existing_variable(self):
        table = {"$x": "1"}

        with self.assertRaises(SyntaxError):
            self.parse("set $x = 2 +", table)

        self.assertEqual(table, {"$x": "1"})

    def test_set_with_extra_input_does_not_change_table(self):
        table = {}

        with self.assertRaises(SyntaxError):
            self.parse("set $x = 1 2", table)

        self.assertEqual(table, {})

    def test_parsers_without_table_do_not_share_variables(self):
        self.parse("set $x = 5")

        with self.assertRaises(SyntaxError):
            self.parse("echo $x")


if __name__ == "__main__":
    unittest.main()