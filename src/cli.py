import argparse
import sys

from blessed import Terminal

from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser

term = Terminal()


def run_pyhton_file(filename: str, debug: bool = False):
    try:
        with open(filename, "r") as f:
            code = f.read()

        if debug:
            print(f"{term.bold_cyan}╔══════════════════════╗{term.normal}")
            print(
                f"{term.bold_cyan}║{term.normal} {term.bold_yellow}🔍 PYHTON DEBUG MODE{term.normal} {term.bold_cyan}║{term.normal}"
            )
            print(f"{term.bold_cyan}╚══════════════════════╝{term.normal}")
            print(f"{term.bold}📄 Input file:{term.normal} {term.italic}{filename}{term.normal}")
            print(f"{term.bold}📝 Source code:{term.normal}")
            print(
                f"{term.dim}┌─────────────────────────────────────────────────────────────────────────────────────┐{term.normal}"
            )
            for i, line in enumerate(code.split("\n"), 1):
                if line.strip():
                    print(f"{term.dim}│{term.normal} {term.bright_white}{line}{term.normal}")
            print(
                f"{term.dim}└─────────────────────────────────────────────────────────────────────────────────────┘{term.normal}"
            )
            print()

        # Step 1: Lexical Analysis
        if debug:
            print(f"{term.bold_blue}🔍 STEP 1: LEXICAL ANALYSIS{term.normal}")
            print(f"{term.dim}─────────────────────────────{term.normal}")

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        if debug:
            print(f"{term.bold}📊 Tokens generated:{term.normal}")
            for i, token in enumerate(tokens):
                token_type = f"{term.bright_green}{token.type.value}{term.normal}"
                token_value = f"{term.bright_yellow}'{token.value}'{term.normal}"
                line_info = f"{term.dim}Line {token.line}{term.normal}"
                print(f"  {term.bright_white}{i + 1:2d}.{term.normal} {token_type:20} │ {token_value:20} │ {line_info}")
            print()

        # Step 2: Syntax Analysis
        if debug:
            print(f"{term.bold_blue}🏗️  STEP 2: SYNTAX ANALYSIS{term.normal}")
            print(f"{term.dim}─────────────────────────────{term.normal}")

        parser = Parser(tokens)
        ast = parser.parse()

        if debug:
            print(f"{term.bold}🌳 Abstract Syntax Tree:{term.normal}")
            print(
                f"{term.dim}└─{term.normal} {term.bold_magenta}Program{term.normal} with {term.bright_cyan}{len(ast.statements)}{term.normal} statement(s)"
            )
            for i, node in enumerate(ast.statements):
                node_type = f"{term.bright_green}{type(node).__name__}{term.normal}"
                print(f"   {term.bright_white}{i + 1}.{term.normal} {node_type}: {term.dim}{node}{term.normal}")
            print()

        # Step 3: Execution
        if debug:
            print(f"{term.bold_blue}⚡ STEP 3: EXECUTION{term.normal}")
            print(f"{term.dim}─────────────────────────────{term.normal}")
            print(f"{term.bold}📤 Program output:{term.normal}")

        interpreter = Interpreter()
        interpreter.interpret(ast)

        if debug:
            print()
            print(f"{term.bold_green}✅ Execution completed successfully!{term.normal}")

    except FileNotFoundError:
        print(f"{term.bold_red}Error:{term.normal} File '{filename}' not found")
    except Exception as e:
        print(f"{term.bold_red}Error:{term.normal} {e}")


def run_interactive_mode(debug: bool = False):
    interpreter = Interpreter()

    print(
        f"{term.bold_cyan}╔══════════════════════════════════════════════════════════════════════════════════════╗{term.normal}"
    )
    print(
        f"{term.bold_cyan}║{term.normal} {term.bold_yellow}🎯 PYHTON INTERACTIVE MODE{term.normal} {term.bold_cyan}║{term.normal}"
    )
    print(
        f"{term.bold_cyan}╚══════════════════════════════════════════════════════════════════════════════════════╝{term.normal}"
    )
    print(f"{term.dim}Type your pyhton code line by line. Use 'exit()' or Ctrl+C to quit.{term.normal}")
    print(f"{term.dim}Remember: all keywords must be typos! (deff, prrint, retrn, etc.){term.normal}")
    print()

    line_number = 1

    while True:
        try:
            prompt = f"{term.bright_green}pyhton[{line_number}]:{term.normal}"
            code = input(prompt)

            # handle special commands
            if code.strip.lower() in ["exit()", "quit()", "exit", "quit"]
                print(f"{term.dim}Goodbye!{term.normal}")
                break

            if code.strip() == "":
                continue

            if code.strip.lower() in ["help()", "help"]:
                print_help()
                continue

            execute_interactive_line(code, interpreter, debug, line_number)
            line_number = line_number + 1

        except KeyboardInterrupt:
            print(f"\n{term.dim}Goodbye!{term.normal}")
            break
        except EOFError:
            print(f"\n{term.dim}Goodbye!{term.normal}")
            break

def execute_interactive_line(code: str, interpreter: Interpreter, debug: bool, line_number: int):
    try:
        if debug:
            print(f"{term.dim}── Executing line {line_number} ──{term.normal}")

        # tokenize
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        if debug:
            print(f"{term.dim}Tokens: {[f'{t.type.value}({t.value})' for t in tokens if t.type.value != 'EOF']}{term.normal}")

        parser = Parser(tokens)
        ast = parser.parse()

        if debug:
            print(f"{term.dim}AST: {[f'{type(node).__name__}' for node in ast.statements]}{term.normal}")

        interpreter.interpret(ast)

    except Exception as e:
        print(f"{term.bold_red}Error:{term.normal} {e}")

def print_help():
    """Print help information for interactive mode"""
    print(f"{term.bold}📚 Pyhton Interactive Help{term.normal}")
    print(f"{term.dim}─────────────────────────{term.normal}")
    print("Available commands:")
    print(f"  {term.bright_green}help(){term.normal} - Show this help message")
    print(f"  {term.bright_green}exit(){term.normal} - Quit the interactive mode")
    print()
    print("Example usage:")
    print(f"  {term.bright_yellow}a = 5{term.normal}")
    print(f"  {term.bright_yellow}b = 3{term.normal}")
    print(f"  {term.bright_yellow}prrint(a + b){term.normal}")
    print(f"  {term.bright_yellow}deff greet(name):{term.normal}")
    print(f"  {term.bright_yellow}    prrint(\"Hello, \" + name){term.normal}")
    print(f"  {term.bright_yellow}    retrn \"Hello, \" + name{term.normal}")
    print()
    print("Remember: All keywords must be typos!")
    print(f"  {term.bright_cyan}def{term.normal} → {term.bright_green}deff, de, edf{term.normal}")
    print(f"  {term.bright_cyan}print{term.normal} → {term.bright_green}prrint, pint, pritn{term.normal}")
    print(f"  {term.bright_cyan}return{term.normal} → {term.bright_green}retrn, retrun, retur{term.normal}")
    print()




def main():
    parser = argparse.ArgumentParser(
        description="Pyhton interpreter - Python-based esolang with required typos", prog="pyhton"
    )
    parser.add_argument("filename", help="Path to the .yp file to execute")
    parser.add_argument("--debug", "-d", action="store_true", help="Show debug information for each compilation step")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode (REPL)")

    args = parser.parse_args()

    if args.interactive or args.filename is None:
        run_interactive_mode(debug=args.debug)
        return

    if not args.filename.endswith(".yp"):
        print("Error: File must have .yp extension")
        sys.exit(1)

    run_pyhton_file(args.filename, debug=args.debug)


if __name__ == "__main__":
    main()
