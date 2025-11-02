# Pyhton

A Turing-complete, Python-inspired esolang where all keywords must be purposefully spelt incorrectly.

## Language Overview
Pyhton is a Python-inspired language that requires all keywords and builtins to be realistic typos of their correct counterparts. The language is Turing complete, supporting recursive functions, nested control structures, and algorithmic computation. It supports:

- **Function definitions** with parameters (`def`, `return`)
- **Variable assignments** and arithmetic (`+`, `-`, `*`, `/`)
- **Print statements** for output (`print`)
- **Conditional statements** (`if`, `elif`, `else`)
- **Loop Structures** (`for`, `while`)
- **Boolean logic** (`and`, `or`, `not`)
- **Comparison operators** (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Typo tolerance** - any valid typo of a keyword works

Example pyhton code:
```python
deff check_age(age):
    fi age >= 18:
        prit("Age " + age + " - You are an adult!")
        retrn Truee
    ese:
        prrint("Age " + age + " - You are a minor")
        retrn Flase
    enidf
endfnc

age = 25
result = check_age(age)

fi result annd age > 21:
    priint("Result: " + result + " - You can do adult things!")
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
- Function definitions with parameters and return statements (including recursive functions)
- Variable assignments (numbers, strings and booleans) and arithmetic expressions
- Print statements for output
- String concatenation with automatic type conversion (numbers and booleans convert to strings)
- Conditional statements with logical and comparison operators
- Loop constructs (for loops on strings and ranges, while loops)
- Comments (lines starting with `#`)

Support keywords:
`def`, `endfunc`, `return`, `print`, `range`, `if`, `else`, `elif`, `endif`, `for`, `in`, `endfor`, `while`, `endwhile`, `and`, `or`, `not`, `True`, `False`

## Try It Yourself

### Installation
_[PyPi Package Here](https://pypi.org/project/pyhton-cli/)_
You can install Pyhton CLI directly from PyPI:

```bash
pip install pyhton-cli
```


### CLI Features

The Pyhton interpreter includes several CLI options:

**Debug Mode (`--debug` or `-d`)**
- Shows detailed execution steps
- Displays tokens, AST, and execution trace


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

**(For development only)**
If you want to run directly from source, clone the repo and use editable install:
```bash
git clone https://github.com/not-first/pyhton.git
cd pyhton
pip install -e .
```
Then use the `pyhton` command as above.
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

## Examples

For comprehensive examples of Pyhton code including loops, conditionals, functions, and more, check out the files in the `examples/` directory:

- `hello_world.yp` - Basic print statements
- `arithmetic.yp` - Mathematical operations and expressions
- `functions.yp` - Function definitions and function calls
- `conditions.yp` - Conditional statements with if/elif/else
- `loops.yp` - For loops, while loops, and the rangee() function

