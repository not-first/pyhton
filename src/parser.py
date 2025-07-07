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


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Program:
        statements = []
        while not self._is_at_end():
            if self._current_token().type == TokenType.NEWLINE:
                self._advance()
                continue
            stmt = self._statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def _is_at_end(self) -> bool:
        return self.pos >= len(self.tokens) or self._current_token().type == TokenType.EOF

    def _current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # return eof token
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos = self.pos + 1
        return self._previous()

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._current_token().type == token_type

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _statement(self) -> Optional[ASTNode]:
        if self._match(TokenType.DEF):
            return self._function_def()
        elif self._match(TokenType.RETURN):
            return self._return_statement()
        elif self._match(TokenType.PRINT):
            return self._print_statement()
        else:
            return self._assignment_or_expression()

    def _function_def(self) -> FunctionDef:
        name = self._current_token().value
        self._advance()  # go past function name
        self._advance()  # go over (

        params = []

        while not self._check(TokenType.RPAREN) and not self._is_at_end():
            params.append(self._current_token().value)
            self._advance()
            if self._match(TokenType.COMMA):
                continue

        self._advance()  # go over )
        self._advance()  # go over :

        while self._match(TokenType.NEWLINE):
            pass

        body = []

        while not self._is_at_end() and not self._check(TokenType.DEF):
            if self._check(TokenType.NEWLINE):
                self._advance()
                continue
            stmt = self._statement()
            if stmt:
                body.append(stmt)

        return FunctionDef(name, params, body)

    def _return_statement(self) -> Return:
        value = None
        if not self._check(TokenType.NEWLINE) and not self._is_at_end():
            value = self._expression()
        return Return(value)

    def _print_statement(self) -> PrintStatement:
        self._advance()  # go over (
        value = self._expression()
        self._advance()  # go over )
        return PrintStatement(value)

    def _assignment_or_expression(self) -> Optional[ASTNode]:
        expr = self._expression()

        if self._match(TokenType.ASSIGN):
            if isinstance(expr, Identifier):
                value = self._expression()
                return Assignment(expr.name, value)

        return expr

    def _expression(self) -> ASTNode:
        return self._addition()

    def _addition(self) -> ASTNode:
        expr = self._multiplication()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().value
            right = self._multiplication()
            expr = BinaryOp(expr, operator, right)

        return expr

    def _multiplication(self) -> ASTNode:
        expr = self._primary()

        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self._previous().value
            right = self._primary()
            expr = BinaryOp(expr, operator, right)

        return expr

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
                while not self._check(TokenType.RPAREN) and not self._is_at_end():
                    args.append(self._expression())
                    if not self._match(TokenType.COMMA):
                        break

                self._advance()  # go over )
                return FunctionCall(name, args)

            return Identifier(name)

        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._advance()  # go over )
            return expr

        raise Exception(f"Unexpected token: {self._current_token()}")
