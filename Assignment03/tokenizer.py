# File: tokenizer.py
# Author: Adam Edwards (with help from ChatGPT)
# Date: 9/13/2026
# Purpose:
# Tokenize commands for the simple shell defined in Assignment 03.
#
# AI Assistance:
# ChatGPT was used to help adapt the tokenizer structure from
# the Module02F class example to the Assignment 03 shell grammar.

import re
from enum import Enum, auto
from typing import List, Tuple


class TokenType(Enum):
    KEYWORD = auto()
    WORD = auto()
    DOT = auto()
    SEPARATOR = auto()
    EOF = auto()


Token = Tuple[TokenType, str]


KEYWORDS = {"ls", "cd", "cat", "print", "exec"}


token_specification = [
    ("DOT",       r"\."),
    ("SEPARATOR", r"\\"),
    ("WORD",      r"[A-Za-z0-9]+"),
    ("SKIP",      r"[ \t\n]+"),
    ("MISMATCH",  r"."),
]


master_regex = "|".join(
    f"(?P<{name}>{regex})"
    for name, regex in token_specification
)


def tokenize(code: str) -> List[Token]:
    tokens = []

    for mo in re.finditer(master_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == "WORD":
            if value in KEYWORDS:
                tokens.append((TokenType.KEYWORD, value))
            else:
                tokens.append((TokenType.WORD, value))

        elif kind == "DOT":
            tokens.append((TokenType.DOT, value))

        elif kind == "SEPARATOR":
            tokens.append((TokenType.SEPARATOR, value))

        elif kind == "SKIP":
            continue

        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character: {value}")

    tokens.append((TokenType.EOF, "EOF"))

    return tokens