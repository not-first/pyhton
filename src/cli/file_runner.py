from blessed import Terminal

from ..core.interpreter import Interpreter
from ..core.lexer import Lexer
from ..core.parser import Parser

term = Terminal()


def run_pyhton_file(filename: str, debug: bool = False):
    try:
        with open(filename, "r") as f:
            code = f.read()  # read the content of the file

        if debug:
            print(f"{term.bold_cyan}╔═══════════════════╗{term.normal}")
            print(
                f"{term.bold_cyan}║{term.normal} {term.bold_yellow}PYHTON DEBUG MODE{term.normal} {term.bold_cyan}║{term.normal}"
            )
            print(f"{term.bold_cyan}╚═══════════════════╝{term.normal}")
            print(f"{term.bold}Input file:{term.normal} {term.italic}{filename}{term.normal}")
            print(f"{term.bold}Source code:{term.normal}")
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

        # step 1: lexical analysis (lexer)
        if debug:
            print(f"{term.bold_blue}STEP 1: LEXICAL ANALYSIS{term.normal}")
            print(f"{term.dim}─────────────────────────────{term.normal}")

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        if debug:
            print(f"{term.bold}Tokens generated:{term.normal}")
            for i, token in enumerate(tokens):
                token_type = f"{term.bright_green}{token.type.value}{term.normal}"
                token_value = f"{term.bright_yellow}'{token.value}'{term.normal}"
                line_info = f"{term.dim}Line {token.line}{term.normal}"
                print(f"  {term.bright_white}{i + 1:2d}.{term.normal} {token_type:20} │ {token_value:20} │ {line_info}")
            print()

        # step 2: syntax analysis (parser)
        if debug:
            print(f"{term.bold_blue}STEP 2: SYNTAX ANALYSIS{term.normal}")
            print(f"{term.dim}─────────────────────────────{term.normal}")

        parser = Parser(tokens)
        ast = parser.parse()

        if debug:
            print(f"{term.bold}Abstract Syntax Tree:{term.normal}")
            print(
                f"{term.dim}└─{term.normal} {term.bold_magenta}Program{term.normal} with {term.bright_cyan}{len(ast.statements)}{term.normal} statement(s)"
            )
            for i, node in enumerate(ast.statements):
                node_type = f"{term.bright_green}{type(node).__name__}{term.normal}"
                print(f"   {term.bright_white}{i + 1}.{term.normal} {node_type}: {term.dim}{node}{term.normal}")
            print()

        # step 3: execution (interpreter)
        if debug:
            print(f"{term.bold_blue}STEP 3: EXECUTION{term.normal}")
            print(f"{term.dim}─────────────────────────────{term.normal}")
            print(f"{term.bold}Program output:{term.normal}")

        interpreter = Interpreter()
        interpreter.interpret(ast)

        if debug:
            print()
            print(f"{term.bold_green}Execution completed successfully!{term.normal}")

    except FileNotFoundError:
        print(f"{term.bold_red}Error:{term.normal} File '{filename}' not found")
    except Exception as e:
        print(f"{term.bold_red}Error:{term.normal} {e}")
