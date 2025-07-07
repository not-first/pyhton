import argparse
import sys

from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


def run_pyhton_file(filename: str, debug: bool = False):
    try:
        with open(filename, "r") as f:
            code = f.read()

        if debug:
            print("=== DEBUG MODE ===")
            print(f"Input file: {filename}")
            print(f"source code: \n{code}")
            print()

        # lexer -> parser -> interpreter

        if debug:
            print("Beginning lexical analysis (lexer)")

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        if debug:
            print("Tokens generated:")
            for i, token in enumerate(tokens):
                print(f"  {i + 1:2d}. {token.type.value:12} | '{token.value}' | Line {token.line}")
            print()

        if debug:
            print("Beginning syntax analysis (parser)")

        parser = Parser(tokens)
        ast = parser.parse()

        if debug:
            print("Abstract Syntax Tree:")
            print(f"- Program with {len(ast.statements)} statement(s)")
            for i, node in enumerate(ast.statements):
                print(f"  {i + 1}. {node}")
            print()

        if debug:
            print("Beginning execution (interpreter)")
            print("---------------")

        interpreter = Interpreter()
        interpreter.interpret(ast)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Pyhton interpreter - Python-based esolang with required typos", prog="pyhton"
    )
    parser.add_argument("filename", help="Path to the .yp file to execute")
    parser.add_argument("--debug", "-d", action="store_true", help="Show debug information for each compilation step")

    args = parser.parse_args()

    if not args.filename.endswith(".yp"):
        print("Error: File must have .yp extension")
        sys.exit(1)

    run_pyhton_file(args.filename, debug=args.debug)


if __name__ == "__main__":
    main()
