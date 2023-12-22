# TinySol Language Specification

## Overview

TinySol is a simplified subset of Solidity, designed for translation into the Brainfuck programming language. It is intended for use in environments where Brainfuck is the execution medium, such as certain blockchain or smart contract platforms.

## Syntax and Semantics

### Data Types

- **Integer**: The primary data type in TinySol is the integer. It supports basic integer operations.

### Variables

- **Declaration and Assignment**: Variables are declared with the `int` keyword followed by an identifier and an optional initialization.
  - Syntax: `int variable_name [= initial_value];`
  - Example: `int x = 5;`

### Control Structures

#### Loops

- **For Loop**: Used for iterating over a range of values.
  - Syntax: `for (initialization; condition; iteration) { /* code */ }`
  - Example: `for (int i = 0; i < 10; i++) { /* code */ }`
- **While Loop**: Executes code as long as a condition is true.
  - Syntax: `while (condition) { /* code */ }`
  - Example: `while (x < 10) { /* code */ }`

#### Conditional Statements

- **If-Else Statement**: Used for executing code based on a condition.
  - Syntax: `if (condition) { /* code */ } else { /* code */ }`
  - Example: `if (x > 5) { /* code */ } else { /* code */ }`

### Arithmetic and Logical Operations

- Supports basic arithmetic operations like addition, subtraction, multiplication, and division.
- Includes logical operations such as `>`, `<`, `==`, and `!=`.

### Functions

- If implemented, functions will allow basic parameter passing and return values. However, advanced features like recursion may not be supported due to Brainfuck's limitations.

### Comments

- Single-line comments are initiated with `//`.
  - Example: `// This is a comment`

## Translation to Brainfuck

The TinySol compiler translates TinySol code into Brainfuck, mapping TinySol constructs to equivalent Brainfuck instructions. This translation focuses on maintaining the logical structure and operations defined in TinySol while adhering to the constraints and capabilities of Brainfuck.

## Limitations

- Given its design for compatibility with Brainfuck, TinySol has inherent limitations in terms of complexity, memory management, and computational efficiency.
- Advanced features like complex data structures, extensive memory operations, and high-level abstractions are outside the scope of TinySol.
