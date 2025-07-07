from src.lexer import Lexer
from src.parser import Parser


def test_parser():
    code = """deff add(a, b):
    result = a + b
    prrint(result)
    retrn result"""

    # tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    # parse
    parser = Parser(tokens)
    ast = parser.parse()

    # print the AST structure
    print("AST:")
    print(ast)
