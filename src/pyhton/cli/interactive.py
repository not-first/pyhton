from blessed import Terminal

from pyhton.core.interpreter import Interpreter
from pyhton.core.lexer import Lexer
from pyhton.core.parser import Parser
from pyhton.cli.help import print_help

term = Terminal()


def run_interactive_mode(debug: bool = False):
    # initialize the interpreter
    # by using the same interpreter instance across multiple lines, context is preserved
    interpreter = Interpreter()

    print(f"{term.bold_cyan}╔═════════════════════════╗{term.normal}")
    print(
        f"{term.bold_cyan}║{term.normal} {term.bold_yellow}PYHTON INTERACTIVE MODE{term.normal} {term.bold_cyan}║{term.normal}"
    )
    print(f"{term.bold_cyan}╚═════════════════════════╝{term.normal}")
    print(f"{term.dim}Type your pyhton code line by line. Use 'exit()' or Ctrl+C to quit.{term.normal}")
    print(f"{term.dim}Remember: all keywords must be typos! (deff, prrint, retrn, etc.){term.normal}")
    print()

    line_number = 1

    while True:
        try:
            prompt = f"{term.bright_green}pyhton[{line_number}]:{term.normal} "
            code = input(prompt)  # prompt user for the line of code to execute

            # handle exit commands
            if code.strip().lower() in ["exit()", "quit()", "exit", "quit"]:
                print(f"{term.dim}Goodbye!{term.normal}")
                break

            # skip empty lines
            if code.strip() == "":
                continue

            # handle help command
            if code.strip().lower() in ["help()", "help"]:
                print_help()  # display help information
                continue

            execute_interactive_line(code, interpreter, debug, line_number)  # execute the line of code
            line_number = line_number + 1

        except KeyboardInterrupt:
            print(f"\n{term.dim}Exiting interactive mode!{term.normal}")
            break
        except EOFError:
            print(f"\n{term.dim}Exiting interactive mode!{term.normal}")
            break


def execute_interactive_line(code: str, interpreter: Interpreter, debug: bool, line_number: int):
    try:
        if debug:
            print(f"{term.dim}── Executing line {line_number} ──{term.normal}")

        # tokenize
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        if debug:
            print(
                f"{term.dim}Tokens: {[f'{t.type.value}({t.value})' for t in tokens if t.type.value != 'EOF']}{term.normal}"
            )

        # parse
        parser = Parser(tokens)
        ast = parser.parse()

        if debug:
            print(f"{term.dim}AST: {[f'{type(node).__name__}' for node in ast.statements]}{term.normal}")

        # execute
        interpreter.interpret(ast)

    except Exception as e:
        print(f"{term.bold_red}Error:{term.normal} {e}")
