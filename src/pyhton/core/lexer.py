from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from pyhton.language.typo_engine import TypoEngine


class TokenType(Enum):
    # literals
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"

    # keywords
    DEF = "DEF"
    ENDFUNC = "ENDFUNC"
    RETURN = "RETURN"

    # builtins
    PRINT = "PRINT"
    RANGE = "RANGE"

    # operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"

    EQUALS = "EQUALS"  # ==
    NOT_EQUALS = "NOT_EQUALS"  # !=
    LESS_THAN = "LESS_THAN"  # <
    GREATER_THAN = "GREATER_THAN"  # >
    LESS_EQUAL = "LESS_EQUAL"  # <=
    GREATER_EQUAL = "GREATER_EQUAL"  # >=

    # conditionals
    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"
    ENDIF = "ENDIF"

    # logical operators
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    # loops
    FOR = "FOR"
    IN = "IN"
    ENDFOR = "ENDFOR"
    WHILE = "WHILE"
    ENDWHILE = "ENDWHILE"

    # punctation
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    COLON = "COLON"  # :
    COMMA = "COMMA"  # ,
    NEWLINE = "NEWLINE"  # \n

    EOF = "EOF"


# the Token class represents a single token in the source code
@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    original_word: Optional[str] = None


# the lexer tokenizes the source code into a list of tokens
class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.typo_engine = TypoEngine()

    # main method to tokenize the source code
    def tokenize(self) -> List[Token]:
        tokens = []  # initialize an empty list to hold tokens

        while self.pos < len(self.code):  # repeat until the end of the code
            token = self._next_token()  # get the next token
            if token:
                tokens.append(token)  # if a token is found, append it to the list
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))  # add an EOF token to mark the end of the input

        return tokens  # return the list of tokens

    # private method to get the next token from the source code
    def _next_token(self) -> Optional[Token]:
        self._skip_whitespace()  # skip whitespace characters

        if self.pos >= len(self.code):  # if the end of the code is reached, return None
            return None

        current_char = self.code[self.pos]  # get the current character

        # handle comments
        if current_char == "#":
            self._skip_comment()
            return None

        # COMMENT THESE
        if current_char == "=" and self.pos + 1 < len(self.code) and self.code[self.pos + 1] == "=":
            token = Token(TokenType.EQUALS, "==", self.line, self.column)
            self._advance()
            self._advance()
            return token

        if current_char == "!" and self.pos + 1 < len(self.code) and self.code[self.pos + 1] == "=":
            token = Token(TokenType.NOT_EQUALS, "!=", self.line, self.column)
            self._advance()
            self._advance()
            return token

        if current_char == "<":
            if self.pos + 1 < len(self.code) and self.code[self.pos + 1] == "=":
                token = Token(TokenType.LESS_EQUAL, "<=", self.line, self.column)
                self._advance()
                self._advance()
                return token
            else:
                token = Token(TokenType.LESS_THAN, "<", self.line, self.column)
                self._advance()
                return token
        if current_char == ">":
            if self.pos + 1 < len(self.code) and self.code[self.pos + 1] == "=":
                token = Token(TokenType.GREATER_EQUAL, ">=", self.line, self.column)
                self._advance()
                self._advance()
                return token
            else:
                token = Token(TokenType.GREATER_THAN, ">", self.line, self.column)
                self._advance()
                return token

        # handle numbers
        if current_char.isdigit():
            return self._read_number()

        # handle strings
        if current_char == '"':
            return self._read_string()

        # handle identifiers and keywords
        if current_char.isalpha() or current_char == "_":
            return self._read_identifier()

        # handle single-character tokens
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
            token_type = single_char_tokens[current_char]  # get the token type for the current character
            token = Token(token_type, current_char, self.line, self.column)  # create a new token
            self._advance()  # advance to the next character

            # if the token is a newline, increment the line number and reset the column
            if current_char == "\n":
                self.line = self.line + 1
                self.column = 1

            return token

        # unknown character, skip it
        self._advance()
        return None

    # private method to skip whitespace characters
    def _skip_whitespace(self):
        # repeat until the end of the code or a non-whitespace character is found
        while self.pos < len(self.code) and self.code[self.pos] in " \t\r":
            if self.code[self.pos] == "\t":  # if the character is a tab, increment the column by 4 (a tab is 4 spaces)
                self.column = self.column + 4
            else:
                self.column = self.column + 1  # otherwise, increment the column by 1

            self.pos = self.pos + 1  # advance to the next character

    # private method to skip comments
    def _skip_comment(self):
        # repeat until the end of the code or a newline character is found
        while self.pos < len(self.code) and self.code[self.pos] != "\n":
            self._advance()  # advance to the next character

    # private method to advance the position and column
    def _advance(self):
        self.pos = self.pos + 1
        self.column = self.column + 1

    # private method to read a number token
    def _read_number(self) -> Token:
        start_pos = self.pos
        start_column = self.column

        # repeat until the end of the code or a non-digit character is found
        while self.pos < len(self.code) and (self.code[self.pos].isdigit() or self.code[self.pos] == "."):
            self._advance()

        value = self.code[start_pos : self.pos]  # get the substring from start_pos to current position
        return Token(TokenType.NUMBER, value, self.line, start_column)  # create a new token with the number value

    # private method to read a string token
    def _read_string(self) -> Token:
        start_column = self.column
        self._advance()  # skip opening quote

        value = ""

        # repeat until the end of the code or a closing quote is found
        while self.pos < len(self.code) and self.code[self.pos] != '"':
            value = value + self.code[self.pos]  # append the current character to the value
            self._advance()  # advance to the next character

        if self.pos < len(self.code):
            self._advance()  # skip closing quote

        return Token(TokenType.STRING, value, self.line, start_column)  # create a new token with the string value

    # private method to read an identifier or keyword token
    def _read_identifier(self) -> Token:
        start_pos = self.pos
        start_column = self.column

        # repeat until the end of the code or a non-alphanumeric character is found
        while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == "_"):
            self._advance()

        value = self.code[start_pos : self.pos]  # get the substring from start_pos to current position

        # raise an exception if the identifier is a correct word
        if self.typo_engine.is_correct_word(value):
            raise Exception(f"'{value}' is spelled correctly. It must be a typo.")

        correct_word = self.typo_engine.find_original_word(value)  # find the original word if it is a typo

        # if the correct word is one of the keywords, return the corresponding token type
        if correct_word == "def":
            return Token(TokenType.DEF, value, self.line, start_column)
        elif correct_word == "endfunc":
            return Token(TokenType.ENDFUNC, value, self.line, start_column)
        elif correct_word == "return":
            return Token(TokenType.RETURN, value, self.line, start_column)
        elif correct_word == "print":
            return Token(TokenType.PRINT, value, self.line, start_column)
        elif correct_word == "range":
            return Token(TokenType.RANGE, value, self.line, start_column)
        elif correct_word == "if":
            return Token(TokenType.IF, value, self.line, start_column)
        elif correct_word == "elif":
            return Token(TokenType.ELIF, value, self.line, start_column)
        elif correct_word == "else":
            return Token(TokenType.ELSE, value, self.line, start_column)
        elif correct_word == "endif":
            return Token(TokenType.ENDIF, value, self.line, start_column)
        elif correct_word == "for":
            return Token(TokenType.FOR, value, self.line, start_column)
        elif correct_word == "in":
            return Token(TokenType.IN, value, self.line, start_column)
        elif correct_word == "endfor":
            return Token(TokenType.ENDFOR, value, self.line, start_column)
        elif correct_word == "while":
            return Token(TokenType.WHILE, value, self.line, start_column)
        elif correct_word == "endwhile":
            return Token(TokenType.ENDWHILE, value, self.line, start_column)
        elif correct_word == "and":
            return Token(TokenType.AND, value, self.line, start_column)
        elif correct_word == "or":
            return Token(TokenType.OR, value, self.line, start_column)
        elif correct_word == "not":
            return Token(TokenType.NOT, value, self.line, start_column)
        elif correct_word == "True":
            return Token(TokenType.BOOLEAN, value, self.line, start_column, correct_word)
        elif correct_word == "False":
            return Token(TokenType.BOOLEAN, value, self.line, start_column, correct_word)
        else:
            return Token(
                TokenType.IDENTIFIER, value, self.line, start_column
            )  # return an identifier token if it is not a keyword
