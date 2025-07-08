import argparse
import sys

from .file_runner import run_pyhton_file
from .interactive import run_interactive_mode


def main():
    parser = argparse.ArgumentParser(
        description="Pyhton interpreter - Python-based esolang with required typos", prog="pyhton"
    )
    parser.add_argument("filename", nargs="?", help="Path to the .yp file to execute (optional)")
    parser.add_argument("--debug", "-d", action="store_true", help="Show debug information for each compilation step")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode (REPL)")

    args = parser.parse_args()  # parse arguments supplied from the command being run

    # handle running interactive mode if the flag is set or no filename is provided
    if args.interactive or args.filename is None:
        run_interactive_mode(debug=args.debug)
        return

    # enforce that the provided filename must end in .yp
    if not args.filename.endswith(".yp"):
        print("Error: File must have .yp extension")
        sys.exit(1)

    run_pyhton_file(args.filename, debug=args.debug)  # run the file


if __name__ == "__main__":
    main()
