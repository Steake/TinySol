from typing import Dict, Any
from src.ast2brainfuck.memory.memory_manager import MemoryManager
from src.ast2brainfuck.translators.base_translator import BaseTranslator

class ArithmeticTranslator(BaseTranslator):
    def __init__(self, memory_manager: MemoryManager):
        """
        Initialize arithmetic translator
        
        Args:
            memory_manager (MemoryManager): Memory management instance
        """
        super().__init__(memory_manager)
    
    def translate_multiplication(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Generate Brainfuck code for multiplication with improved algorithm
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck multiplication code
        """
        # Allocate temporary memory cells
        temp1 = self.memory_manager.allocate_temp_memory()
        temp2 = self.memory_manager.allocate_temp_memory()
        
        # Clear target memory
        brainfuck_code = self._generate_set_value(target_memory, 0)
        
        # Advanced multiplication algorithm
        brainfuck_code += "".join([
            # Copy right operand to temp1
            f"{'>' if temp1 > 0 else ''}{'<' if temp1 < 0 else ''}[-]",
            f"{'>' if right_memory > temp1 else ''}{'<' if right_memory < temp1 else ''}[",
            f"{'>' if temp1 > right_memory else ''}{'<' if temp1 < right_memory else ''}+",
            f"{'>' if right_memory > temp1 else ''}{'<' if right_memory < temp1 else ''}[-]",
            "]",
            
            # Multiply by left operand
            f"{'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[",
            f"{'>' if temp1 > left_memory else ''}{'<' if temp1 < left_memory else ''}[",
            f"{'>' if target_memory > temp1 else ''}{'<' if target_memory < temp1 else ''}+",
            f"{'>' if temp1 > left_memory else ''}{'<' if temp1 < left_memory else ''}[-]",
            "]",
            f"{'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[-]",
            "]"
        ])
        
        return brainfuck_code
    
    def translate_modulo(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Generate Brainfuck code for modulo operation with improved algorithm
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck modulo code
        """
        # Allocate temporary memory cells
        temp1 = self.memory_manager.allocate_temp_memory()
        temp2 = self.memory_manager.allocate_temp_memory()
        
        # Clear target memory
        brainfuck_code = self._generate_set_value(target_memory, 0)
        
        # Advanced modulo algorithm
        brainfuck_code += "".join([
            # Copy left operand to temp1
            f"{'>' if temp1 > 0 else ''}{'<' if temp1 < 0 else ''}[-]",
            f"{'>' if left_memory > temp1 else ''}{'<' if left_memory < temp1 else ''}[",
            f"{'>' if temp1 > left_memory else ''}{'<' if temp1 < left_memory else ''}+",
            f"{'>' if left_memory > temp1 else ''}{'<' if left_memory < temp1 else ''}[-]",
            "]",
            
            # Perform modulo calculation
            f"{'>' if temp1 > 0 else ''}{'<' if temp1 < 0 else ''}[",
            f"{'>' if right_memory > temp1 else ''}{'<' if right_memory < temp1 else ''}[",
            f"{'>' if temp1 > right_memory else ''}{'<' if temp1 < right_memory else ''}[-]",
            f"{'>' if right_memory > temp1 else ''}{'<' if right_memory < temp1 else ''}[-]",
            "]",
            
            # If remainder is zero, set target to zero
            f"{'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}[-]",
            f"{'>' if temp1 > 0 else ''}{'<' if temp1 < 0 else ''}[",
            f"{'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+",
            f"{'>' if temp1 > 0 else ''}{'<' if temp1 < 0 else ''}[-]",
            "]"
        ])
        
        return brainfuck_code
    
    def translate_addition(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Generate Brainfuck code for addition with improved algorithm
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck addition code
        """
        # Clear target memory first
        brainfuck_code = self._generate_set_value(target_memory, 0)
        
        # Copy left value to target
        brainfuck_code += self._copy_memory_value(left_memory, target_memory)
        
        # Add right value to target
        brainfuck_code += "".join([
            f"{'>' if right_memory > target_memory else ''}{'<' if right_memory < target_memory else ''}[",
            f"{'>' if target_memory > right_memory else ''}{'<' if target_memory < right_memory else ''}+",
            f"{'>' if right_memory > target_memory else ''}{'<' if right_memory < target_memory else ''}[-]",
            "]"
        ])
        
        return brainfuck_code
