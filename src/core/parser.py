from dataclasses import dataclass
from typing import List, Optional

from .lexer import Token, TokenType


# base node
@dataclass
class ASTNode:
    pass


# expresions (things that evaluate to values)
@dataclass
class NumberLiteral(ASTNode):
    value: float


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]


# statements (things that do actions)
@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]


@dataclass
class Return(ASTNode):
    value: Optional[ASTNode]


@dataclass
class PrintStatement(ASTNode):
    value: ASTNode


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


# the parser takes a list of tokens and produces an AST (Abstract Syntax Tree)
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    # parse the tokens into an AST
    def parse(self) -> Program:
        statements = []

        # loop through the tokens until the end is reached
        while not self._is_at_end():
            # skip newlines
            if self._current_token().type == TokenType.NEWLINE:
                self._advance()
                continue

            stmt = self._statement()  # parse a single statement

            if stmt:
                statements.append(stmt)  # if a statement is found, append it to the list

        return Program(statements)  # return the program with all statements

    # private method to determine if the end of the tokens list is reached
    def _is_at_end(self) -> bool:
        return self.pos >= len(self.tokens) or self._current_token().type == TokenType.EOF

    # private method to get the current token
    def _current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # return EOF token if the position is out of bounds

        return self.tokens[self.pos]  # return the current token

    # private method to advance to the next token
    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos = self.pos + 1  # if not at the end, move to the next token

        return self._previous()  # return the previous token (as there is no next token)

    # private method to get the previous token
    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    # private method to check if the current token matches a specific type
    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False

        return self._current_token().type == token_type

    # private method to check if the current token matches any of the given types, and skip it if it does
    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    # private method to parse a statement
    def _statement(self) -> Optional[ASTNode]:
        if self._match(TokenType.DEF):
            return self._function_def()
        elif self._match(TokenType.RETURN):
            return self._return_statement()
        elif self._match(TokenType.PRINT):
            return self._print_statement()
        else:
            return self._assignment_or_expression()

    # private method to parse a function definition
    def _function_def(self) -> FunctionDef:
        name = self._current_token().value  # extract the function name
        self._advance()  # skip the function name token
        self._advance()  # skip the (

        params = []

        # loop through, collecting parameters seperated by a , until a ) is found
        while not self._check(TokenType.RPAREN) and not self._is_at_end():
            params.append(self._current_token().value)
            self._advance()
            if self._match(TokenType.COMMA):
                continue

        self._advance()  # skip the closing )
        self._advance()  # skip the :

        while self._match(TokenType.NEWLINE):
            pass

        body = []

        # collect statements until the next function definition or end of file
        while not self._is_at_end() and not self._check(TokenType.DEF):
            # skip newlines
            if self._match(TokenType.NEWLINE):
                continue

            stmt = self._statement()
            if stmt:
                body.append(stmt)  # append the statement to the body

        return FunctionDef(
            name, params, body
        )  # return the function definition with its name, parameters, and body statements

    # private method to parse a return statement
    def _return_statement(self) -> Return:
        value = None

        # skip the return keyword
        if not self._check(TokenType.NEWLINE) and not self._is_at_end():
            value = self._expression()

        return Return(value)  # return a return statement with the value (if any)

    # private method to parse a print statement
    def _print_statement(self) -> PrintStatement:
        self._advance()  # skip the opening (
        value = self._expression()
        self._advance()  # skip the closing )
        return PrintStatement(value)  # return a print statement with the value to be printed

    # private method to parse an assignment or an expression
    def _assignment_or_expression(self) -> Optional[ASTNode]:
        expr = self._expression()

        # if the next token is an assignment operator, create an Assignment node
        if self._match(TokenType.ASSIGN):
            if isinstance(expr, Identifier):
                value = self._expression()
                return Assignment(expr.name, value)

        return expr  # else, return the expression as is

    # private method to parse an expression
    def _expression(self) -> ASTNode:
        return self._addition()  # start with addition, which is the lowest precedence operation

    # private methods to handle different levels of precedence in expressions

    def _addition(self) -> ASTNode:
        expr = self._multiplication()  # start with multiplication, which has higher precedence

        # if the next token is a + or -, create a BinaryOp node
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().value
            right = self._multiplication()
            expr = BinaryOp(expr, operator, right)

        return expr  # return the expression with all additions and subtractions applied

    def _multiplication(self) -> ASTNode:
        expr = self._primary()  # start with the primary expression (literals, identifiers, etc.)

        # if the next token is a * or /, create a BinaryOp node
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self._previous().value
            right = self._primary()
            expr = BinaryOp(expr, operator, right)

        return expr  # return the expression with all multiplications and divisions applied

    # private method to handle primary expressions (literals, identifiers, function calls, etc.)
    def _primary(self) -> ASTNode:
        if self._match(TokenType.NUMBER):
            return NumberLiteral(float(self._previous().value))

        if self._match(TokenType.STRING):
            return StringLiteral(self._previous().value)

        if self._match(TokenType.IDENTIFIER):
            name = self._previous().value

            # check if it is a function call
            if self._match(TokenType.LPAREN):
                args = []

                # collect arguments until a ) is found
                while not self._check(TokenType.RPAREN) and not self._is_at_end():
                    args.append(self._expression())
                    if not self._match(TokenType.COMMA):
                        break

                self._advance()  # skip over the closing )
                return FunctionCall(name, args)  # return a function call node with the name and arguments

            return Identifier(name)  # if it is just an identifier, return it

        # if the next token is a (, parse the expression inside parentheses
        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._advance()  # skip over )
            return expr

        raise Exception(f"Unexpected token: {self._current_token()}")  # raise an error if none of the above matches
