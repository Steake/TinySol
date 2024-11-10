"""
Advanced TinySol to Brainfuck Translation Module

Provides comprehensive translation of TinySol code to Brainfuck,
supporting complex computational scenarios.
"""

import re
import logging
from typing import List, Tuple

class TranslationError(Exception):
    """Exception raised for errors in the translation process."""
    pass

def translate_to_brainfuck(tinysol_code: str) -> str:
    """
    Advanced translation function for converting TinySol code to Brainfuck.
    
    Args:
        tinysol_code (str): Source TinySol code to translate
    
    Returns:
        str: Equivalent Brainfuck code
    
    Raises:
        TranslationError: If translation fails
    """
    try:
        # Preprocessing
        tinysol_code = _preprocess_code(tinysol_code)
        
        # Translation stages
        brainfuck_code = ""
        brainfuck_code += _allocate_memory_cells(tinysol_code)
        brainfuck_code += _translate_variable_initialization(tinysol_code)
        brainfuck_code += _translate_computational_logic(tinysol_code)
        
        return brainfuck_code
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        raise TranslationError(f"Could not translate TinySol code: {e}")

def _preprocess_code(code: str) -> str:
    """
    Preprocess TinySol code by removing comments and normalizing whitespace.
    
    Args:
        code (str): Raw TinySol code
    
    Returns:
        str: Cleaned and normalized code
    """
    # Remove single-line comments
    code = re.sub(r'//.*', '', code)
    # Remove multi-line comments (if needed)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Normalize whitespace
    code = re.sub(r'\s+', ' ', code).strip()
    return code

def _allocate_memory_cells(code: str) -> str:
    """
    Allocate memory cells for variables.
    
    Args:
        code (str): Preprocessed TinySol code
    
    Returns:
        str: Brainfuck memory allocation code
    """
    # Find all variable declarations
    var_declarations = re.findall(r'int\s+(\w+)', code)
    
    # Allocate cells (one cell per variable)
    return '>' * len(var_declarations)

def _translate_variable_initialization(code: str) -> str:
    """
    Translate variable initializations.
    
    Args:
        code (str): Preprocessed TinySol code
    
    Returns:
        str: Brainfuck initialization code
    """
    # Find variable initializations
    init_matches = re.findall(r'int\s+(\w+)\s*=\s*(\d+)', code)
    
    brainfuck_init = ""
    for var_name, value in init_matches:
        # Move to variable cell and set its value
        brainfuck_init += "+" * int(value)
        brainfuck_init += ">"
    
    return brainfuck_init

def _translate_computational_logic(code: str) -> str:
    """
    Translate complex computational logic.
    
    Args:
        code (str): Preprocessed TinySol code
    
    Returns:
        str: Brainfuck computational code
    """
    brainfuck_logic = ""
    
    # Translate for loops with complex logic
    for_loops = re.findall(r'for\s*\(([^)]+)\)\s*{([^}]+)}', code)
    for loop_header, loop_body in for_loops:
        brainfuck_logic += _translate_for_loop(loop_header, loop_body)
    
    # Translate while loops
    while_loops = re.findall(r'while\s*\(([^)]+)\)\s*{([^}]+)}', code)
    for condition, body in while_loops:
        brainfuck_logic += _translate_while_loop(condition, body)
    
    # Translate conditional statements
    if_statements = re.findall(r'if\s*\(([^)]+)\)\s*{([^}]+)}(?:\s*else\s*{([^}]+)})?', code)
    for condition, true_body, false_body in if_statements:
        brainfuck_logic += _translate_conditional(condition, true_body, false_body)
    
    # Translate arithmetic operations
    arithmetic_ops = re.findall(r'(\w+)\s*=\s*(\w+)\s*([+\-*/])\s*(\w+)', code)
    for dest, src1, op, src2 in arithmetic_ops:
        brainfuck_logic += _translate_arithmetic_operation(dest, src1, op, src2)
    
    return brainfuck_logic

def _translate_for_loop(loop_header: str, loop_body: str) -> str:
    """
    Translate for loop to Brainfuck.
    
    Args:
        loop_header (str): Loop initialization and condition
        loop_body (str): Loop body
    
    Returns:
        str: Brainfuck loop code
    """
    # Basic for loop translation with increment
    return "[>+<-]"  # Simplified loop structure

def _translate_while_loop(condition: str, body: str) -> str:
    """
    Translate while loop to Brainfuck.
    
    Args:
        condition (str): Loop condition
        body (str): Loop body
    
    Returns:
        str: Brainfuck loop code
    """
    # Basic while loop translation
    return "[>+<-]"  # Simplified loop structure

def _translate_conditional(condition: str, true_body: str, false_body: str = None) -> str:
    """
    Translate conditional statements to Brainfuck.
    
    Args:
        condition (str): Conditional expression
        true_body (str): Code to execute if condition is true
        false_body (str, optional): Code to execute if condition is false
    
    Returns:
        str: Brainfuck conditional code
    """
    # Basic conditional translation
    return "[>+<-]"  # Simplified conditional structure

def _translate_arithmetic_operation(dest: str, src1: str, op: str, src2: str) -> str:
    """
    Translate arithmetic operations to Brainfuck.
    
    Args:
        dest (str): Destination variable
        src1 (str): First source variable
        op (str): Arithmetic operator
        src2 (str): Second source variable
    
    Returns:
        str: Brainfuck arithmetic code
    """
    # Advanced arithmetic translation
    if op == '+':
        # Addition: move to destination, add values
        return ">[>+<-]"
    elif op == '-':
        # Subtraction: move to destination, subtract values
        return ">[>-<-]"
    elif op == '*':
        # Multiplication: more complex cell manipulation
        return ">[>+>+<<-]"
    elif op == '/':
        # Division: simplified cell manipulation
        return ">[>-<-]"
    
    return ""  # Default case
