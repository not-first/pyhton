# Pyhton

A minimalist esoteric programming language where Python keywords must be typos. Write functions, perform arithmetic, and print output - all while deliberately misspelling every keyword.

## Language Overview

Pyhton is a Python-inspired language that requires all keywords and builtins to be realistic typos of their correct counterparts. The language supports:

- **Function definitions** with parameters (`deff`, `retrn`)
- **Variable assignments** and arithmetic (`+`, `-`, `*`, `/`)
- **Print statements** for output (`prrint`)
- **Typo tolerance** - any valid typo of a keyword works

Example pyhton code:
```python
deff add_numbers(a, b):
    result = a + b
    prrint(result)
    retrn result
```

## Typo Rules

A typo is considered valid if it follows one of these patterns:

1. **Doubled letter**: `prrint` (print with extra 'r')
2. **Missing letter**: `def` → `de` (missing 'f')
3. **Swapped letters**: `print` → `pritn` (i and t swapped)

**Only keywords and builtins need to be typos** - variable names and user-defined function names can be spelled correctly.

## Language Capabilities

Currently supported:
- Function definitions with parameters
- Variable assignments
- Arithmetic expressions (`+`, `-`, `*`, `/`)
- Print statements
- Return statements
- Local and global variable scopes

Supported keywords (must be typo'd):
- `def` → `deff`, `de`, `edf`, etc.
- `return` → `retrn`, `retrun`, `retur`, etc.
- `print` → `prrint`, `pint`, `pritn`, etc.

## Try It Yourself

### Installation

```bash
git clone <repo-url>
cd pyhton
uv install -e .
```

### Running Code

Create a `.yp` file with pyhton code:

```python
# example.yp
deff greet(name):
    message = "Hello, " + name
    prrint(message)
    retrn message

result = greet("World")
```

Run it:
```bash
uv run pyhton example.yp
```

### Execution Pipeline

Here's what happens when you run a `.yp` file:

**1. Lexical Analysis (Lexer)**
```
Input: "deff add(a, b):"
Output: [DEF, IDENTIFIER, LPAREN, IDENTIFIER, COMMA, IDENTIFIER, RPAREN, COLON]
```
The lexer breaks code into tokens and uses the typo engine to identify `deff` as a typo of `def`.

**2. Syntax Analysis (Parser)**
```
Tokens: [DEF, IDENTIFIER, ...]
Output: FunctionDef(name='add', params=['a', 'b'], body=[...])
```
The parser builds an Abstract Syntax Tree representing the program structure.

**3. Execution (Interpreter)**
```
AST: FunctionDef(...)
Output: Function stored in memory, ready to be called
```
The interpreter walks the AST and executes the program, maintaining variable scopes and function definitions.

**Example trace for `prrint(5 + 3)`:**
1. Lexer: `prrint` → PRINT token, `5` → NUMBER, `+` → PLUS, `3` → NUMBER
2. Parser: Creates `PrintStatement(value=BinaryOp(left=5, op='+', right=3))`
3. Interpreter: Evaluates `5 + 3 = 8`, then prints `8`

# Todo
- [ ] Add more tests
- [ ] Add errors for exactly correct words
- [ ] Add CLI options for:
  - [ ] Running only certain steps (lexer, parser, interpreter)
  - [ ] Interactive mode
  - [ ] Showing debug logs