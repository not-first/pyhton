"""Collection of python words to validate against."""

# first verion, contains only very simple words

KEYWORDS = {
    # function definition
    "def",
    "return",
    # control flow
    "if",
    "else",
    "elif",
    # loops
    "for",
    "while",
    # imports
    "import",
    "from",
}

BUILTINS = {
    # functions
    "print",
    "input",
    "len",
    "str",
    "int",
    "float",
}

ALL_WORDS = KEYWORDS | BUILTINS

OPERATORS = {
    # basic calculations
    "+",
    "-",
    "*",
    "/",
    # comparison
    "==",
    "!=",
    "<",
    ">",
    # assignment
    "=",
}
