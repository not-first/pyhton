"""
Interactive mode (REPL) functionality for the Pyhton CLI.
"""

from blessed import Terminal

from ..core.interpreter import Interpreter
from ..core.lexer import Lexer
from ..core.parser import Parser
from .help import print_help

term = Terminal()


def run_interactive_mode(debug: bool = False):
    """Run the Pyhton REPL (Read-Eval-Print Loop)."""
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
            prompt = f"{term.bright_green}pyhton[{line_number}]:{term.normal} "
            code = input(prompt)

            # Handle special commands
            if code.strip().lower() in ["exit()", "quit()", "exit", "quit"]:
                print(f"{term.dim}Goodbye!{term.normal}")
                break

            if code.strip() == "":
                continue

            if code.strip().lower() in ["help()", "help"]:
                print_help()
                continue

            execute_interactive_line(code, interpreter, debug, line_number)
            line_number += 1

        except KeyboardInterrupt:
            print(f"\n{term.dim}Goodbye!{term.normal}")
            break
        except EOFError:
            print(f"\n{term.dim}Goodbye!{term.normal}")
            break


def execute_interactive_line(code: str, interpreter: Interpreter, debug: bool, line_number: int):
    """Execute a single line of code in interactive mode."""
    try:
        if debug:
            print(f"{term.dim}── Executing line {line_number} ──{term.normal}")

        # Tokenize
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        if debug:
            print(
                f"{term.dim}Tokens: {[f'{t.type.value}({t.value})' for t in tokens if t.type.value != 'EOF']}{term.normal}"
            )

        # Parse
        parser = Parser(tokens)
        ast = parser.parse()

        if debug:
            print(f"{term.dim}AST: {[f'{type(node).__name__}' for node in ast.statements]}{term.normal}")

        # Execute
        interpreter.interpret(ast)

    except Exception as e:
        print(f"{term.bold_red}Error:{term.normal} {e}")
