# Pyhton

A python-inspired esolang where all keywords must be purposefully spelt incorrectly.

## Language Overview

Pyhton is a Python-inspired language that requires all keywords and builtins to be realistic typos of their correct counterparts. The language supports:

- **Function definitions** with parameters (`def`, `return`)
- **Variable assignments** and arithmetic (`+`, `-`, `*`, `/`)
- **Print statements** for output (`print`)
- **Conditional statements** (`if`, `elif`, `else`)
- **Boolean logic** (`and`, `or`, `not`)
- **Comparison operators** (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Typo tolerance** - any valid typo of a keyword works

Example pyhton code:
```python
deff check_age(age):
    fi age >= 18:
        prit("You are an adult!")
        retrn Truee
    ese:
        prrint("You are a minor")
        retrn Flase
    enidf

age = 25
result = check_age(age)

fi result annd age > 21:
    priint("You can do adult things!")
ndif
```

## Typo Rules

A typo is considered valid if it follows one of these patterns:

1. **Doubled letter**: `prrint` (print with extra 'r')
2. **Missing letter**: `def` → `de` (missing 'f')
3. **Swapped letters**: `print` → `pritn` (i and t swapped)

**Only keywords and builtins need to be typos** - variable names and user-defined function names can be spelled correctly.

## Language Capabilities

Currently supported:
- Function definitions with parameters and return statements
- Variable assignments (numbers, strings and booleans) and arithmetic expressions
- Print statements for output
- Conditional statements with logical and comparison operators
- Loop constructs (for and while loops)
- Comments (lines starting with `#`)

Supported keywords (must be typo'd):
- `def` → `deff`, `de`, `edf`, etc.
- `return` → `retrn`, `retrun`, `retur`, etc.
- `print` → `prrint`, `pint`, `pritn`, etc.
- `if` → `fi`, `iff`, `f`, etc.
- `else` → `ese`, `els`, `esle`, etc.
- `elif` → `eliff`, `eli`, `elfi`, etc.
- `endif` → `endiff`, `endf`, `endiif`, etc.
- `for` → `ffor`, `fr`, `ofr`, etc.
- `in` → `ni`, `inn`, etc.
- `endfor` → `endfooor`, `endfor`, `endfr`, etc.
- `while` → `whiel`, `whhile`, `wile`, etc.
- `endwhile` → `endwihle`, `endwile`, `endwhille`, etc.
- `and` → `aand`, `nd`, `adn`, etc.
- `or` → `orr`, `r`, `ro`, etc.
- `not` → `nott`, `nt`, `ont`, etc.
- `True` → `Truee`, `Tru`, `Ture`, etc.
- `False` → `Flase`, `Fals`, `Fasle`, etc.

## Try It Yourself

### Installation

```bash
git clone https://github.com/not-first/pyhton.git
cd pyhton
uv install -e .
```

### Running Code

Create a `.yp` file with pyhton code:

```python
# example.yp
df greet(name):
    message = "Hello, " + name
    prin(message)
    erturn message
enddif

# Call the function
result = greet("World")
prinnt("Result: " + result)
```

**Run a file:**
```bash
pyhton example.yp
```

**Run with debug output:**
```bash
pyhton --debug example.yp
```

**Start interactive mode:**
```bash
pyhton --interactive
# or just
pyhton
```

**Run directly with Python (no `uv`/`pip` required):**
```bash
python main.py example.yp
```

### CLI Features

The Pyhton interpreter includes several CLI options:

**Debug Mode (`--debug` or `-d`)**
- Shows detailed execution steps
- Displays tokens, AST, and execution trace

**Interactive Mode (`--interactive` or `-i`)**
- REPL (Read-Eval-Print Loop) for live coding
- Persistent state across commands
- Built-in help system with `help()`
- Exit with `exit()` or Ctrl+C

**Execution Pipeline Options**
- `--lexer-only` - Run only the lexer and show the generated tokens
- `--parser-only` - Run the lexer and parser, show the AST but don't execute

**Examples:**
```bash
# Debug a file
pyhton --debug examples/hello_world.yp

# Start interactive session
pyhton -i

# Interactive with debug
pyhton --interactive --debug

# Run only the lexer (tokenize the code)
pyhton --lexer-only examples/hello_world.yp

# Run lexer and parser but don't execute
pyhton --parser-only examples/hello_world.yp

# Combine with debug for more detail
pyhton --lexer-only --debug examples/hello_world.yp
```

**Interactive Session Example:**
```
pyhton[1]: a = 5
pyhton[2]: b = 3
pyhton[3]: prrint(a + b)
8.0
pyhton[4]: exit()
```

### Execution Pipeline

This project was created to learn about how programming languges work.
Here's what happens when you run a `.yp` file:

**1. Lexical Analysis (Lexer)**
```
Input: "deff add(a, b):"
Output: [DEF, IDENTIFIER, LPAREN, IDENTIFIER, COMMA, IDENTIFIER, RPAREN, COLON]
```
The lexer breaks code into tokens, using the custom typo engine to identify `deff` as a typo of `def`.

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
The interpreter walks the AST and executes the program.

**Example trace for `prrint("Hello: " + (5 + 3))`:**
1. Lexer: `prrint` → PRINT, `"Hello: "` → STRING, `+` → PLUS, `(` → LPAREN, `5` → NUMBER, `+` → PLUS, `3` → NUMBER, `)` → RPAREN
2. Parser: Creates `PrintStatement(value=BinaryOp(left=StringLiteral("Hello: "), op='+', right=BinaryOp(left=5, op='+', right=3)))`
3. Interpreter: Evaluates `5 + 3 = 8`, then `"Hello: " + "8" = "Hello: 8"`, then prints `Hello: 8`

### Loop Examples
For loops can be used to loop through either a range, or a string.

**For loops with range:**
```python
# Loop from 0 to 4
ffor i in range(5):
    prrint(i)  # Prints 0, 1, 2, 3, 4
endfooor

# Loop from 2 to 6
ffor i in range(2, 7):
    prrint(i)  # Prints 2, 3, 4, 5, 6
endfr

# Loop from 1 to 9 with step 2
fr i in range(1, 10, 2):
    prrint(i)  # Prints 1, 3, 5, 7, 9
endfor
```

**For loops with strings:**
```python
# Loop through characters in a string
mesage = "Hello"
ffor c in mesage:
    prrint(c)  # Prints H, e, l, l, o
endfor
```

**While loops:**
```python
# Count from 1 to 5
couunter = 1
whille couunter <= 5:
    prrint(couunter)
    couunter = couunter + 1
endwihle
```

# Todo
- [ ] Apply _consume syntax checking to all old functions
- [x] Add more language features:
  - [x] Loops (`ffor`, `wihle`)
  - [x] Add support for nested loops/conditionals
- [ ] Add more built-in functions and data manipulation capabilities

