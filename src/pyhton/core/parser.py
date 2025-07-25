from dataclasses import dataclass
from typing import List, Optional
from blessed import Terminal

from pyhton.core.lexer import Token, TokenType

term = Terminal()


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
class BooleanLiteral(ASTNode):
    value: bool


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class ComparisonOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class LogicalOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    op_type: str  # "and" or "or"


@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    elif_clauses: List[tuple[ASTNode, List[ASTNode]]]  # (condition, body) pairs
    else_body: Optional[List[ASTNode]]


@dataclass
class ForLoop(ASTNode):
    variable: str
    iterable: ASTNode
    body: List[ASTNode]


@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: List[ASTNode]


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
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.FOR):
            return self._for_loop()
        elif self._match(TokenType.WHILE):
            return self._while_loop()
        elif self._match(TokenType.DEF):
            return self._function_def()
        elif self._match(TokenType.RETURN):
            return self._return_statement()
        elif self._match(TokenType.PRINT):
            return self._print_statement()
        else:
            return self._assignment_or_expression()

    def _if_statement(self) -> IfStatement:
        condition = self._expression()
        self._advance()  # skip the :

        # skip newlines
        while self._match(TokenType.NEWLINE):
            pass

        # parse the then body - continue until a elif, else, or endif is hit
        then_body = []
        while (
            not self._is_at_end()
            and not self._check(TokenType.ELIF)
            and not self._check(TokenType.ELSE)
            and not self._check(TokenType.ENDIF)
        ):
            if self._match(TokenType.NEWLINE):
                continue

            stmt = self._statement()
            if stmt:
                then_body.append(stmt)

        # parse elif clauses
        elif_clauses = []
        while self._match(TokenType.ELIF):
            elif_condition = self._expression()
            self._advance()  # skip the :

            # skip newlines
            while self._match(TokenType.NEWLINE):
                pass

            elif_body = []
            while (
                not self._is_at_end()
                and not self._check(TokenType.ELIF)
                and not self._check(TokenType.ELSE)
                and not self._check(TokenType.ENDIF)
            ):
                if self._match(TokenType.NEWLINE):
                    continue

                stmt = self._statement()
                if stmt:
                    elif_body.append(stmt)

            elif_clauses.append((elif_condition, elif_body))

        # parse else clause
        else_body = None
        if self._match(TokenType.ELSE):
            self._advance()  # skip the :

            # skip newlines
            while self._match(TokenType.NEWLINE):
                pass

            else_body = []
            while not self._is_at_end() and not self._check(TokenType.ENDIF):
                if self._match(TokenType.NEWLINE):
                    continue

                stmt = self._statement()
                if stmt:
                    else_body.append(stmt)

        # expect and consume the endif token
        self._consume(TokenType.ENDIF, "Expected 'endif' to close if statement")

        return IfStatement(condition, then_body, elif_clauses, else_body)

    # private method to parse a for loop
    def _for_loop(self) -> ForLoop:
        variable_token = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'for'")
        variable = variable_token.value  # extract the variable name

        self._consume(TokenType.IN, "Expected 'in' after for variable")

        iterable = self._expression()  # parse the iterable expression

        self._consume(TokenType.COLON, "Expected ':' after for loop iterable")

        while self._match(TokenType.NEWLINE):
            pass

        # parse the body
        body = []
        while not self._is_at_end() and not self._check(TokenType.ENDFOR):
            if self._match(TokenType.NEWLINE):
                continue

            stmt = self._statement()
            if stmt:
                body.append(stmt)

        # parse the ENDFOR token
        self._consume(TokenType.ENDFOR, "Expected 'endfor' to close for loop")

        return ForLoop(variable, iterable, body)  # return the for loop with its variable, iterable, and body

    # private method to parse a while loop
    def _while_loop(self) -> WhileLoop:
        condition = self._expression()

        self._consume(TokenType.COLON, "Expected ':' after while loop condition")

        # skip newlines
        while self._match(TokenType.NEWLINE):
            pass

        # parse the body
        body = []
        while not self._is_at_end() and not self._check(TokenType.ENDWHILE):
            if self._match(TokenType.NEWLINE):
                continue

            stmt = self._statement()
            if stmt:
                body.append(stmt)

        # parse the ENDWHILE token
        self._consume(TokenType.ENDWHILE, "Expected 'endwhile' to close while loop")

        return WhileLoop(condition, body)  # return the while loop with its condition and body

    # private method to consume a token of a specific type, raising an error if it doesn't match
    def _consume(self, token_type: TokenType, error_message: str) -> Token:
        if self._check(token_type):
            return self._advance()

        raise Exception(f"{error_message}, got {self._current_token()}")  # raise an error if the token doesn't match

    # private method to parse a function definition
    def _function_def(self) -> FunctionDef:
        name = self._current_token().value  # extract the function name
        self._consume(TokenType.IDENTIFIER, "Expected function name after 'def'")
        self._consume(TokenType.LPAREN, "Expected '(' after function name")

        params = []

        # loop through, collecting parameters seperated by a , until a ) is found
        while not self._check(TokenType.RPAREN) and not self._is_at_end():
            params.append(self._current_token().value)
            self._advance()
            if self._match(TokenType.COMMA):
                continue

        self._consume(TokenType.RPAREN, "Expected ')' after function parameters")
        self._consume(TokenType.COLON, "Expected ':' after function parameters")

        while self._match(TokenType.NEWLINE):
            pass

        body = []

        # collect statements until endfunc is found
        while not self._is_at_end() and not self._check(TokenType.ENDFUNC):
            # skip newlines
            if self._match(TokenType.NEWLINE):
                continue

            stmt = self._statement()
            if stmt:
                body.append(stmt)  # append the statement to the body

        # consume the endfunc token
        self._consume(TokenType.ENDFUNC, "Expected 'endfunc' to close function definition")

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
        self._consume(TokenType.LPAREN, "Expected '(' after print")
        value = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after print argument")

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
        return self._logical_or()  # start with logical OR, which has the lowest precedence

    # private method to handle local OR expressions
    def _logical_or(self) -> ASTNode:
        expr = self._logical_and()

        # while the next token is an OR, create a LogicalOp node
        while self._match(TokenType.OR):
            operator = self._previous().value
            right = self._logical_and()
            expr = LogicalOp(expr, operator, right, "or")

        return expr

    # private method to handle logical AND expressions
    def _logical_and(self) -> ASTNode:
        expr = self._equality()

        # while the next token is an AND, create a LogicalOp node
        while self._match(TokenType.AND):
            operator = self._previous().value
            right = self._equality()
            expr = LogicalOp(expr, operator, right, "and")

        return expr

    # private method to handle equality comparisons
    def _equality(self) -> ASTNode:
        expr = self._comparison()

        # while the next token is an EQUALS or NOT_EQUALS, create a ComparisonOp node
        while self._match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self._previous().value
            right = self._comparison()
            expr = ComparisonOp(expr, operator, right)

        return expr

    # private method to handle numerical comparisons
    def _comparison(self) -> ASTNode:
        expr = self._addition()

        # while the next token is a comparison operator, create a ComparisonOp node
        while self._match(TokenType.GREATER_THAN, TokenType.GREATER_EQUAL, TokenType.LESS_THAN, TokenType.LESS_EQUAL):
            operator = self._previous().value
            right = self._addition()
            expr = ComparisonOp(expr, operator, right)

        return expr

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
        expr = self._unary()  # start with the primary expression (literals, identifiers, etc.)

        # if the next token is a * or /, create a BinaryOp node
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self._previous().value
            right = self._unary()
            expr = BinaryOp(expr, operator, right)

        return expr  # return the expression with all multiplications and divisions applied

    def _unary(self) -> ASTNode:
        if self._match(TokenType.NOT):
            operator = self._previous().value
            operand = self._unary()
            return UnaryOp(operator, operand)

        return self._primary()

    # private method to handle primary expressions (literals, identifiers, function calls, etc.)
    def _primary(self) -> ASTNode:
        if self._match(TokenType.NUMBER):
            return NumberLiteral(float(self._previous().value))

        if self._match(TokenType.STRING):
            return StringLiteral(self._previous().value)

        if self._match(TokenType.BOOLEAN):
            token = self._previous()
            is_true = token.original_word == "True"
            return BooleanLiteral(is_true)

        if self._match(TokenType.RANGE):
            name = self._previous().value

            # range must be followed by parentheses
            if self._match(TokenType.LPAREN):
                args = []

                # collect arguments until a ) is found
                while not self._check(TokenType.RPAREN) and not self._is_at_end():
                    args.append(self._expression())
                    if not self._match(TokenType.COMMA):
                        break

                self._consume(TokenType.RPAREN, "Expected ')' after range arguments")
                return FunctionCall("range", args)  # return a function call node with name "range"

            raise Exception("Expected '(' after range")

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

                self._consume(TokenType.RPAREN, "Expected ')' after function arguments")
                return FunctionCall(name, args)  # return a function call node with the name and arguments

            return Identifier(name)  # if it is just an identifier, return it

        # if the next token is a (, parse the expression inside parentheses
        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression in parentheses")
            return expr

        raise Exception(f"Unexpected token: {self._current_token()}")  # raise an error if none of the above matches
