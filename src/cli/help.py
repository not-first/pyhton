"""
Help system for the Pyhton CLI.
"""

from blessed import Terminal

term = Terminal()


def print_help():
    """Print help information for interactive mode."""
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
    print(f'  {term.bright_yellow}    prrint("Hello, " + name){term.normal}')
    print(f'  {term.bright_yellow}    retrn "Hello, " + name{term.normal}')
    print()
    print("Remember: All keywords must be typos!")
    print(f"  {term.bright_cyan}def{term.normal} → {term.bright_green}deff, de, edf{term.normal}")
    print(f"  {term.bright_cyan}print{term.normal} → {term.bright_green}prrint, pint, pritn{term.normal}")
    print(f"  {term.bright_cyan}return{term.normal} → {term.bright_green}retrn, retrun, retur{term.normal}")
    print()
