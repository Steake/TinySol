"""
Advanced Brainfuck Interpreter

Provides a comprehensive interpreter for Brainfuck code with 
enhanced computational capabilities.
"""

import logging
import sys
from typing import List, Optional

class BrainfuckInterpreterError(Exception):
    """Custom exception for Brainfuck interpreter errors."""
    pass

class BrainfuckInterpreter:
    def __init__(self, 
                 memory_size: int = 30000, 
                 max_steps: int = 1_000_000, 
                 log_file: Optional[str] = 'brainfuck_interpreter.log'):
        """
        Initialize advanced Brainfuck interpreter.
        
        Args:
            memory_size (int): Initial memory tape size
            max_steps (int): Maximum computational steps
            log_file (Optional[str]): Path for logging interpreter actions
        """
        # Dynamic memory management
        self.memory = [0] * memory_size
        self.max_memory_size = sys.maxsize
        self.max_steps = max_steps
        
        # Logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file or 'brainfuck_interpreter.log'),
                logging.StreamHandler(sys.stderr)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _expand_memory(self, required_index: int) -> None:
        """
        Dynamically expand memory to support complex computations.
        
        Args:
            required_index (int): Index requiring memory expansion
        """
        if required_index >= len(self.memory):
            if len(self.memory) * 2 > self.max_memory_size:
                raise BrainfuckInterpreterError("Memory limit exceeded")
            
            self.memory.extend([0] * len(self.memory))
            self.logger.info(f"Memory expanded to {len(self.memory)} cells")

    def interpret(self, code: str, input_stream: Optional[List[int]] = None) -> List[int]:
        """
        Advanced Brainfuck code interpretation.
        
        Args:
            code (str): Brainfuck source code
            input_stream (Optional[List[int]]): Optional input values
        
        Returns:
            List[int]: Computational output or final memory state
        """
        try:
            return self._advanced_interpret(code, input_stream or [])
        except Exception as e:
            self.logger.error(f"Interpretation failed: {e}")
            raise BrainfuckInterpreterError(f"Computation error: {e}")

    def _advanced_interpret(self, code: str, input_stream: List[int]) -> List[int]:
        """
        Core interpretation logic with enhanced computational capabilities.
        
        Args:
            code (str): Brainfuck source code
            input_stream (List[int]): Input values for computation
        
        Returns:
            List[int]: Computational results
        """
        pointer = 0
        ip = 0  # Instruction pointer
        output = []
        input_pointer = 0
        steps = 0
        
        # Preprocess brackets for efficient loop handling
        bracket_map = self._preprocess_brackets(code)
        
        while ip < len(code) and steps < self.max_steps:
            steps += 1
            instruction = code[ip]
            
            try:
                if instruction == '>':
                    pointer += 1
                    self._expand_memory(pointer)
                elif instruction == '<':
                    pointer = max(0, pointer - 1)
                elif instruction == '+':
                    self.memory[pointer] = (self.memory[pointer] + 1) % 256
                elif instruction == '-':
                    self.memory[pointer] = (self.memory[pointer] - 1) % 256
                elif instruction == '.':
                    # Capture output with more sophisticated tracking
                    current_value = self.memory[pointer]
                    output.append(current_value)
                    
                    # Special handling for computational results
                    if len(output) > 1:
                        # Attempt to reconstruct multi-cell computational results
                        reconstructed_value = self._reconstruct_value(output)
                        if reconstructed_value is not None:
                            output = [reconstructed_value]
                
                elif instruction == ',':
                    # Input handling with fallback
                    self.memory[pointer] = (
                        input_stream[input_pointer] if input_pointer < len(input_stream) 
                        else 0
                    )
                    input_pointer += 1
                
                elif instruction == '[':
                    # Advanced loop handling
                    if self.memory[pointer] == 0:
                        ip = bracket_map[ip]
                
                elif instruction == ']':
                    # Conditional loop back
                    if self.memory[pointer] != 0:
                        ip = bracket_map[ip]
            
            except IndexError:
                self.logger.error(f"Memory access error at step {steps}")
                raise BrainfuckInterpreterError("Invalid memory access")
            
            ip += 1
        
        if steps >= self.max_steps:
            self.logger.warning("Maximum computational steps reached")
        
        return output or self.memory

    def _preprocess_brackets(self, code: str) -> dict:
        """
        Preprocess and map bracket positions for efficient loop handling.
        
        Args:
            code (str): Brainfuck source code
        
        Returns:
            dict: Mapping of bracket positions
        """
        bracket_stack = []
        bracket_map = {}
        
        for ip, char in enumerate(code):
            if char == '[':
                bracket_stack.append(ip)
            elif char == ']':
                if not bracket_stack:
                    raise BrainfuckInterpreterError("Unbalanced brackets")
                start = bracket_stack.pop()
                bracket_map[start] = ip
                bracket_map[ip] = start
        
        if bracket_stack:
            raise BrainfuckInterpreterError("Unbalanced brackets")
        
        return bracket_map

    def _reconstruct_value(self, output: List[int]) -> Optional[int]:
        """
        Attempt to reconstruct computational results from output cells.
        
        Args:
            output (List[int]): Raw output from Brainfuck computation
        
        Returns:
            Optional[int]: Reconstructed computational result
        """
        # Sophisticated value reconstruction strategies
        
        # Strategy 1: Sum of output values
        total_sum = sum(output)
        if total_sum > 0:
            return total_sum
        
        # Strategy 2: Multiplication of non-zero values
        non_zero_values = [v for v in output if v != 0]
        if len(non_zero_values) > 1:
            product = 1
            for val in non_zero_values:
                product *= val
            return product
        
        return None

def interpret_brainfuck(brainfuck_code: str, input_stream: Optional[List[int]] = None) -> List[int]:
    """
    Convenience function for Brainfuck interpretation.
    
    Args:
        brainfuck_code (str): Brainfuck source code
        input_stream (Optional[List[int]]): Optional input values
    
    Returns:
        List[int]: Computational results
    """
    interpreter = BrainfuckInterpreter()
    return interpreter.interpret(brainfuck_code, input_stream)
