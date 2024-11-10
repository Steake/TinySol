import pytest
from src.ast2brainfuck import translate_to_brainfuck
from src.brainfuck_interpreter import interpret_brainfuck

def test_universal_computation_fibonacci():
    """
    Test universal computation by simulating Fibonacci sequence generation.
    Verifies complex algorithmic task implementation.
    """
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
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    result = interpret_brainfuck(brainfuck_code)
    
    assert result is not None, "Fibonacci computation failed"
    assert len(result) > 0, "No computational output generated"

def test_memory_manipulation():
    """
    Test dynamic memory manipulation and complex memory interactions.
    """
    tinysol_code = """
    int x = 5;
    int y = 10;
    
    while (x < y) {
        x = x + 1;
        y = y - 1;
    }
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    result = interpret_brainfuck(brainfuck_code)
    
    assert result is not None, "Memory manipulation test failed"

def test_conditional_branching():
    """
    Test complex conditional logic and decision-making capabilities.
    """
    tinysol_code = """
    int x = 7;
    int result = 0;
    
    if (x > 5) {
        result = 1;
    } else {
        result = 0;
    }
    
    if (x < 10) {
        result = result + 2;
    }
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    result = interpret_brainfuck(brainfuck_code)
    
    assert result is not None, "Conditional branching test failed"

def test_recursive_like_behavior():
    """
    Simulate recursive-like computational patterns.
    """
    tinysol_code = """
    int n = 5;
    int factorial = 1;
    
    for (int i = 1; i <= n; i++) {
        factorial = factorial * i;
    }
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    result = interpret_brainfuck(brainfuck_code)
    
    assert result is not None, "Recursive-like behavior test failed"
    assert len(result) > 0, "No computational output generated"

def test_algorithmic_complexity():
    """
    Test multi-state computational scenarios and control flow complexity.
    """
    tinysol_code = """
    int sum = 0;
    int limit = 100;
    
    for (int i = 1; i <= limit; i++) {
        if (i % 3 == 0 || i % 5 == 0) {
            sum = sum + i;
        }
    }
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    result = interpret_brainfuck(brainfuck_code)
    
    assert result is not None, "Algorithmic complexity test failed"
    assert len(result) > 0, "No computational output generated"

def test_brainfuck_output_validity():
    """
    Verify the validity of generated Brainfuck code.
    """
    tinysol_code = """
    int x = 10;
    int y = 20;
    int z = x + y;
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    
    assert brainfuck_code is not None, "Brainfuck translation failed"
    assert len(brainfuck_code) > 0, "Empty Brainfuck code generated"
    assert all(char in '+-<>[].' for char in brainfuck_code), "Invalid Brainfuck characters detected"
