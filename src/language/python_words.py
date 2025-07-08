# first verion, contains only very simple words

KEYWORDS = {
    "def",  # function definition
    "return",  # return statement
    "if",  # if statement
    "elif",
    "else",
    "endif",  # end if statement
    "and",  # logical operators
    "or",
    "not",
    "True",  # boolean true
    "False",  # boolean false
}

BUILTINS = {
    "print",  # print function
}

ALL_WORDS = KEYWORDS | BUILTINS

OPERATORS = {
    # basic calculations
    "+",
    "-",
    "*",
    "/",
    # assignment
    "=",
}
