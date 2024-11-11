"""
Behavior-Driven Development (BDD) Tests for TinySol to Brainfuck Compiler

These tests describe specific computational scenarios from a user's perspective,
validating the translation and interpretation process.
"""

import pytest
from src.ast2brainfuck import translate_to_brainfuck
from src.brainfuck_interpreter import interpret_brainfuck as our_interpreter
from brainfuck import NiceInterpreter

def test_fibonacci_sequence_generation():
    """
    Scenario: Generate Fibonacci sequence
    As a programmer
    I want to write a TinySol program to generate Fibonacci numbers
    So that I can verify complex algorithmic computation
    """
    # Given a TinySol program for Fibonacci sequence
    tinysol_code = """
    int a = 0;
    int b = 1;
    int n = 10;
    int result = 0;
    
    for (int i = 0; i < n; i++) {
        result = a;
        a = b;
        b = result + b;
    }
    """
    
    # When I translate the code to Brainfuck
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    
    # Then the Brainfuck code should be valid
    assert brainfuck_code is not None
    assert len(brainfuck_code) > 0
    print(f"Generated Brainfuck code:\n{brainfuck_code}")
    
    # And when I interpret the Brainfuck code
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    # Then the output should match the expected Fibonacci sequence
    expected_fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert len(our_output) >= len(expected_fibonacci)
    assert our_output == external_output
    assert expected_fibonacci == our_output[:len(expected_fibonacci)]

def test_prime_number_checker():
    """
    Scenario: Check if a number is prime
    As a programmer
    I want to write a TinySol program to determine prime numbers
    So that I can validate complex conditional logic
    """
    # Given a TinySol program to check prime numbers
    tinysol_code = """
    int n = 17;
    int is_prime = 1;
    
    for (int i = 2; i < n; i++) {
        if (n % i == 0) {
            is_prime = 0;
        }
    }
    """
    
    # When I translate the code to Brainfuck
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    
    # Then the Brainfuck code should be valid
    assert brainfuck_code is not None
    assert len(brainfuck_code) > 0
    print(f"Generated Brainfuck code:\n{brainfuck_code}")
    
    # And when I interpret the Brainfuck code
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    # Then the output should indicate the number is prime
    assert our_output == external_output
    assert 1 in our_output  # 17 is a prime number

def test_factorial_computation():
    """
    Scenario: Compute factorial of a number
    As a programmer
    I want to write a TinySol program to calculate factorial
    So that I can test recursive-like computational patterns
    """
    # Given a TinySol program to calculate factorial
    tinysol_code = """
    int n = 5;
    int factorial = 1;
    
    for (int i = 1; i <= n; i++) {
        factorial = factorial * i;
    }
    """
    
    # When I translate the code to Brainfuck
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    
    # Then the Brainfuck code should be valid
    assert brainfuck_code is not None
    assert len(brainfuck_code) > 0
    print(f"Generated Brainfuck code:\n{brainfuck_code}")
    
    # And when I interpret the Brainfuck code
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    # Then the output should match the factorial of 5 (120)
    assert our_output == external_output
    assert 120 in our_output

def test_sum_of_multiples():
    """
    Scenario: Calculate sum of multiples
    As a programmer
    I want to write a TinySol program to sum multiples of 3 and 5
    So that I can test algorithmic complexity
    """
    # Given a TinySol program to sum multiples
    tinysol_code = """
    int sum = 0;
    int limit = 100;
    
    for (int i = 1; i < limit; i++) {
        if (i % 3 == 0 || i % 5 == 0) {
            sum = sum + i;
        }
    }
    """
    
    # When I translate the code to Brainfuck
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    
    # Then the Brainfuck code should be valid
    assert brainfuck_code is not None
    assert len(brainfuck_code) > 0
    print(f"Generated Brainfuck code:\n{brainfuck_code}")
    
    # And when I interpret the Brainfuck code
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    # Then the output should match the sum of multiples of 3 and 5 below 100
    assert our_output == external_output
    assert 2318 in our_output  # Sum of multiples of 3 and 5 below 100
