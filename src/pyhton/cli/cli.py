import argparse
import sys

from blessed import Terminal

from pyhton.cli.file_runner import run_pyhton_file
from pyhton.cli.interactive import run_interactive_mode

term = Terminal()


def main():
    parser = argparse.ArgumentParser(
        description="Pyhton interpreter - Python-based esolang with required typos", prog="pyhton"
    )
    parser.add_argument("filename", nargs="?", help="Path to the .yp file to execute (optional)")
    parser.add_argument("--debug", "-d", action="store_true", help="Show debug information for each compilation step")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode (REPL)")

    # pipeline stage options
    execution_group = parser.add_mutually_exclusive_group()
    execution_group.add_argument("--lexer-only", action="store_true", help="Run only the lexer and show tokens")
    execution_group.add_argument(
        "--parser-only", action="store_true", help="Run lexer and parser, show the AST but don't execute code"
    )

    args = parser.parse_args()  # parse arguments supplied from the command being run

    # check if any execution stage flags are used in interactive mode
    if (args.interactive or args.filename is None) and (args.lexer_only or args.parser_only):
        print(
            f"{term.bold_red}Error:{term.normal} Stage-specific options require a filename and cannot be used with interactive mode"
        )
        sys.exit(1)

    # handle running interactive mode if the flag is set or no filename is provided
    if args.interactive or args.filename is None:
        run_interactive_mode(debug=args.debug)
        return

    # enforce that the provided filename must end in .yp
    if not args.filename.endswith(".yp"):
        print(f"{term.bold_red}Error:{term.normal} File must have .yp extension")
        sys.exit(1)

    # determine the execution stage
    stage = "all"
    if args.lexer_only:
        stage = "lexer"
    elif args.parser_only:
        stage = "parser"

    # run the file with the appropriate stage
    run_pyhton_file(args.filename, debug=args.debug, stage=stage)  # run the file


if __name__ == "__main__":
    main()
