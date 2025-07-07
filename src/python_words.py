"""Collection of python words to validate against."""

# first verion, contains only very simple words

KEYWORDS = {
    # variables and assigning
    "def",
    "return",
    "if",
    "else",
    "elif",
    # basic literals
    "True",
    "False",
    "None",
    # word compmarison
    "and",
    "or",
    "not",
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
