# TinySol

#### Language Spec

---

TinySol is a highish level language designed for writing smart contracts for the TinyChain blockchain, which utilises Brainfuck as its underlying VM.



TinySol aims to s̵i̵m̵p̵l̵i̵f̵y̵ make possible Smart Contract development by providing a human-readable syntax that compiles into Brainfuck code.

---

## Syntax

### **Variables**

Variables are statically typed at declaration. Supported types include integers which are compiled into Brainfuck cell values.

\```tinysol
int count;
\```

Variable assignment and initialization:

\```tinysol
int total = 10;
\```

### **Operators**

****TinySol supports basic arithmetic operators: `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division), and `=` (assignment).

### ** Control Structures**

#### If Statements

TinySol includes conditional `if` statements with optional `else` clauses.

\```tinysol
if (condition) {
    // Code for truthy condition
} else {
    // Code for falsy condition
}
\```

#### While Loop

Loops are created with the `while` keyword and are executed as long as a condition is true.

\```tinysol
while (condition) {
    // Loop body code
}
\```

### Functions

Functions are first-class citizens in TinySol and are declared with a return type, name, and parameters.

\```tinysol
function int add(int x, int y) {
    return x + y;
}
\```

Calling a function:

\```tinysol
int result;
result = add(5, 3);
\```

## Comments

Single-line comments are supported with `//`.

\```tinysol
// This is a comment
\```

## Data Types

### Integer

Integer (`int`) is the primary data type used to represent numerical values.

## Error Handling

Errors in TinySol are reported at compile-time and include syntax errors, type mismatches, and unresolved references.

---

## Brainfuck Compilation Strategy

TinySol is designed to compile into efficient Brainfuck code. The following strategies are employed:

- Variable allocation is mapped to fixed cells on the Brainfuck memory tape.
- Arithmetic operations are translated directly into Brainfuck loops and cell manipulations.
- Conditional logic is translated using Brainfuck's loop (`[...]`) and cell value manipulation.

---

This language specification is an initial overview of the features and behaviors expected for TinySol. The TinySol compiler will translate code written following this specification into Brainfuck, taking into account the simplicity and constraints of the Brainfuck language.

The completion of this specification will be followed by the creation of a language reference manual that includes detailed descriptions of all language features, including standard libraries and advanced features for smart contract development. Additionally, sample contracts and developer guides will be provided to help users get started with TinySol on TinyChain.

Please note that developing a new programming language is an iterative process and the specification may expand or adjust as development continues and as feedback from early adopters is incorporated.
