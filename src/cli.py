import sys

from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


def run_pyhton_file(filename: str):
    try:
        with open(filename, "r") as f:
            code = f.read()

        # lexer -> parser -> interpreter
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(ast)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m src.cli <filename.yp>")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith(".yp"):
        print("Error: File must have .yp extension")
        sys.exit(1)

    run_pyhton_file(filename)


if __name__ == "__main__":
    main()
