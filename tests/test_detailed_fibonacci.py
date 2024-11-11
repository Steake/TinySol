import pytest
from src.ast2brainfuck import translate_to_brainfuck
from src.brainfuck_interpreter import interpret_brainfuck as our_interpreter
from brainfuck import NiceInterpreter

def test_variable_initialization():
    tinysol_code = """
    int a = 0;
    int b = 1;
    int n = 10;
    int result = 0;
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Brainfuck code: {brainfuck_code}")
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    expected_output = [0, 1, 10, 0]
    assert our_output == external_output == expected_output

def test_single_fibonacci_iteration():
    tinysol_code = """
    int a = 0;
    int b = 1;
    int result = a;
    a = b;
    b = result + b;
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Brainfuck code: {brainfuck_code}")
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    expected_output = [1, 1, 0]
    assert our_output == external_output == expected_output

def test_for_loop_structure():
    tinysol_code = """
    int n = 5;
    int i = 0;
    for (i = 0; i < n; i++) {
        int temp = i;
    }
    """
    brainfuck_code = translate_to_brainfuck(tinysol_code)
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Brainfuck code: {brainfuck_code}")
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    expected_output = [5, 5]  # n and final value of i
    assert our_output == external_output == expected_output

def test_full_fibonacci_sequence():
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
    our_output = our_interpreter(brainfuck_code)
    external_interpreter = NiceInterpreter()
    external_interpreter.execute(brainfuck_code)
    external_output = [cell for cell in external_interpreter.array if cell != 0]
    
    print(f"Brainfuck code: {brainfuck_code}")
    print(f"Our output: {our_output}")
    print(f"External output: {external_output}")
    
    expected_output = [34, 55, 10, 34]  # Final values of a, b, n, and result
    assert our_output == external_output == expected_output

if __name__ == "__main__":
    pytest.main([__file__])
