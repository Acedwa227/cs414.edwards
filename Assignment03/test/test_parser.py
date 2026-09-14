import unittest

from parser import ASTNode, Parser
from tokenizer import tokenize


class TestParser(unittest.TestCase):

    def parse(self, command):
        tokens = tokenize(command)
        parser = Parser(tokens)
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


if __name__ == "__main__":
    unittest.main()