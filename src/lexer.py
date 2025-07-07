from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .typo_engine import TypoEngine


class TokenType(Enum):
    # literals
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"

    # keywords
    DEF = "DEF"
    RETURN = "RETURN"

    # builtins
    PRINT = "PRINT"

    # operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"

    # punctation
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    COLON = "COLON"  # :
    COMMA = "COMMA"  # ,
    NEWLINE = "NEWLINE"  # \n

    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.typo_engine = TypoEngine()

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < len(self.code):
            token = self._next_token()
            if token:
                tokens.append(token)
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def _next_token(self) -> Optional[Token]:
        self._skip_whitespace()

        if self.pos >= len(self.code):
            return None

        current_char = self.code[self.pos]

        if current_char.isdigit():
            return self._read_number()

        if current_char == '"':
            return self._read_string()

        if current_char.isalpha() or current_char == "_":
            return self._read_identifier()

        single_char_tokens = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.MULTIPLY,
            "/": TokenType.DIVIDE,
            "=": TokenType.ASSIGN,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            ":": TokenType.COLON,
            ",": TokenType.COMMA,
            "\n": TokenType.NEWLINE,
        }

        if current_char in single_char_tokens:
            token_type = single_char_tokens[current_char]
            token = Token(token_type, current_char, self.line, self.column)
            self._advance()

            if current_char == "\n":
                self.line = self.line + 1
                self.column = 1

            return token

        # unknown character, skip it
        self._advance()
        return None

    def _skip_whitespace(self):
        while self.pos < len(self.code) and self.code[self.pos] in " \t\r":
            if self.code[self.pos] == "\t":
                self.column = self.column + 4
            else:
                self.column = self.column + 1

            self.pos = self.pos + 1

    def _advance(self):
        self.pos = self.pos + 1
        self.column = self.column + 1

    def _read_number(self) -> Token:
        start_pos = self.pos
        start_column = self.column

        while self.pos < len(self.code) and (self.code[self.pos].isdigit() or self.code[self.pos] == "."):
            self._advance()

        value = self.code[start_pos : self.pos]
        return Token(TokenType.NUMBER, value, self.line, start_column)

    def _read_string(self) -> Token:
        start_column = self.column
        self._advance()  # skip opening quote

        value = ""
        while self.pos < len(self.code) and self.code[self.pos] != '"':
            value = value + self.code[self.pos]
            self._advance()

        if self.pos < len(self.code):
            self._advance()  # skip closing quote

        return Token(TokenType.STRING, value, self.line, start_column)

    def _read_identifier(self) -> Token:
        start_pos = self.pos
        start_column = self.column

        while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == "_"):
            self._advance()

        value = self.code[start_pos : self.pos]

        correct_word = self.typo_engine.find_original_word(value)

        if correct_word == "def":
            return Token(TokenType.DEF, value, self.line, start_column)
        elif correct_word == "return":
            return Token(TokenType.RETURN, value, self.line, start_column)
        elif correct_word == "print":
            return Token(TokenType.PRINT, value, self.line, start_column)
        else:
            return Token(TokenType.IDENTIFIER, value, self.line, start_column)
