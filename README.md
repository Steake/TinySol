# TinySol to Brainfuck Translator

## Overview

TinySol is a sophisticated source-to-source compiler that translates a subset of a high-level programming language (TinySol) to Brainfuck, a minimalist Turing-complete programming language. This project demonstrates advanced compiler design principles, including abstract syntax tree (AST) manipulation, memory management, and code generation.

## Features

- Modular translation architecture
- Support for complex computational scenarios
- Turing-complete translation
- Extensive test coverage
- Flexible and extensible design

## Architecture

### Translation Modules

The translation process is broken down into specialized modules:

1. **Memory Management** (`memory_manager.py`)
   - Tracks memory allocation
   - Manages memory cell tracking
   - Supports complex memory operations

2. **Base Translator** (`base_translator.py`)
   - Provides core translation utilities
   - Implements fundamental translation methods

3. **Arithmetic Translator** (`arithmetic_translator.py`)
   - Handles arithmetic operations
   - Translates multiplication, addition, and modulo operations
   - Implements complex Brainfuck arithmetic algorithms

4. **Condition Translator** (`condition_translator.py`)
   - Manages conditional logic translation
   - Supports various comparison and logical operations

5. **Expression Translator** (`expression_translator.py`)
   - Translates complex expressions
   - Handles binary and unary expressions
   - Manages memory cell allocation for expressions

6. **Statement Translator** (`statement_translator.py`)
   - Translates programming constructs
   - Supports variable declarations
   - Handles loops and conditional statements

7. **Node Translators** (`node_translators.py`)
   - Orchestrates the overall translation process
   - Coordinates between different translation modules

## Supported Constructs

- Variable declarations
- Arithmetic operations (+, -, *, /)
- Comparison operations (==, <=, <, >, >=)
- Logical operations (&&, ||)
- For loops
- Conditional statements (if)

## Installation

```bash
git clone https://github.com/steake/TinySol.git
cd TinySol
pip install -r requirements.txt
```

## Running Tests

```bash
python run_tests.py
```

## Example

```python
# TinySol code
tinysol_code = """
int n = 5;
int factorial = 1;

for (int i = 1; i <= n; i++) {
    factorial = factorial * i;
}
"""

# Translate to Brainfuck
brainfuck_code = translate_to_brainfuck(tinysol_code)
```

## Limitations

- Subset of language features supported
- Complex computational scenarios may require optimization
- Performance overhead due to translation complexity

## Future Improvements

- Enhanced arithmetic algorithms
- More comprehensive language support
- Performance optimizations
- Additional test cases

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.


## Author

GitHub: @steake
