# Pyhton

An python-based esolang where every word has to be a typo.

## Type Rules
Typos have to be 'realistic'. This means any valid typo of the normal python words will work, as long as it fits into one of these categories:
- a letter is repeated twice (prrint)
- a letter is missing (prnt)
- a letter is swapped with another (pritn)

**Typos have to be one of these types, or they are not considered valid. It is your responsibility to ensure you are meeting these syntax requirements.**

*Maybe in the future when a letter is mistyped due to accidentally hitting an adjacent key (peint). The adjacent key typo only considers QWERTY keyboards.*

## Language Behaviour Plan
When code is executed in this esolang it should:
1. **Validate**: Check that each word is a valid typo of a correct python word
2. **Error Handling**: If invalid, throw an error suggesting valid typos
3. **Convert**: Tranform valid pyhton code into correct python
4. **Execute**: Run the python code.

**Maybe in the future, typos should cover variable names too, in most common casings. Every variable MUST be a type of a valid word.**

## Syntax Example
```python
# valid pyhton code (,yp file):
deff hello_wrold():
  prunt("Helo, Wordl!")
  retrn True
```

# Project
## Planned Structure
pyhton/
├── pyproject.toml        # uv project configuration
├── README.md
├── src/
│   └── pyhton/
│       ├── __init__.py
│       ├── lexer.py          # Tokenizes .yp files
│       ├── validator.py      # Validates typos against Python keywords
│       ├── transpiler.py     # Converts valid typos back to Python
│       ├── python_words.py   # Database of Python keywords/builtins
│       ├── typo_engine.py    # Core typo generation and validation logic
│       └── cli.py            # Command-line interface for running .yp files
├── examples/
│   ├── hello_world.yp
│   ├── fibonacci.yp
│   └── classes.yp
└── tests/
    ├── __init__.py
    ├── test_validator.py
    ├── test_transpiler.py
    └── test_typo_engine.py
