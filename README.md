# TinySol & TinySol-2-Brainfuck Compiler
<center><img width='75%' style='margin:auto;' src='./TinySol.jpg'></img></center>

## Overview
TinySol is a subset of the Solidity language, designed to be compatible with Brainfuck, a Turing-complete language with a minimalist instruction set. This project includes a compiler that translates TinySol code into Brainfuck, allowing for the execution of smart contracts and other logic within the Brainfuck environment.

## Features of TinySol
- **Basic Data Types**: Supports integers and basic data types.
- **Variable Declarations and Assignments**: Allows for the declaration and assignment of variables.
- **Control Structures**: Includes if-else statements and for/while loops.
- **Function Calls**: Basic support for function calls with parameters and return values.
- **Arithmetic and Logical Operations**: Supports basic arithmetic operations and logical expressions.

## Using the Compiler
To use the TinySol to Brainfuck compiler, follow these steps:
1. Write your TinySol code according to the specifications and limitations outlined above.
2. Use the `BrainfuckTranslator` class to translate your TinySol code into Brainfuck.
3. Run the translated Brainfuck code in any standard Brainfuck interpreter.

## Examples
Below are some examples of TinySol code and their corresponding Brainfuck translations.

### Example 1: Variable Declaration
**TinySol Code:**
```solidity
int x = 5;
```

**Brainfuck Translation:**
```brainfuck
>+++++
```

### Example 2: Basic For Loop
**TinySol Code:**
```solidity
for (int i = 0; i < 5; i++) {
    // Loop body
}
```

**Brainfuck Translation:**
```brainfuck
[->+<]
```

### Example 3: If-Else Statement
**TinySol Code:**
```solidity
if (x > 1) {
    // If body
} else {
    // Else body
}
```

**Brainfuck Translation:**

```brainfuck
[>]
```

## Next Steps
- Extensive testing with various TinySol code samples.
- Further optimization of the Brainfuck translation logic.
- Comprehensive documentation and example codes for TinySol features.
- Final compilation and review of the TinySol to Brainfuck compiler.

## Contribution
Contributions to the TinySol project and the Brainfuck compiler are welcome. Feel free to fork the repository, make your changes, and submit a pull request.

## Licence

GPLv3
