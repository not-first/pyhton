from src.lexer import Lexer, TokenType


def test_basic_lexing():
    code = """
    deff add(a, b):
      result = a + b
      prrint(result)
      retrn result
    """

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    for token in tokens:
        print(f"{token.type.value}: '{token.value}' at line {token.line}, col {token.column}")
