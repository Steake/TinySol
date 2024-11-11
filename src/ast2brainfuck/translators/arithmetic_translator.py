from typing import Dict, Any
from src.ast2brainfuck.memory.memory_manager import MemoryManager
from src.ast2brainfuck.translators.base_translator import BaseTranslator

class ArithmeticTranslator(BaseTranslator):
    def __init__(self, memory_manager: MemoryManager):
        """
        Initialize arithmetic translator with precise computational tracking
        """
        super().__init__(memory_manager)
    
    def translate_multiplication(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Precise multiplication algorithm with computational preservation
        """
        # Allocate temporary memory cells
        temp = self.memory_manager.allocate_temp_memory()
        
        # Clear target and temporary memory
        brainfuck_code = self._generate_set_value(target_memory, 0)
        brainfuck_code += self._generate_set_value(temp, 0)
        
        # Multiplication algorithm
        brainfuck_code += "".join([
            f"{'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[",
            f"{'>' if temp > left_memory else ''}{'<' if temp < left_memory else ''}+",
            f"{'>' if target_memory > temp else ''}{'<' if target_memory < temp else ''}",
            f"{'>' if right_memory > target_memory else ''}{'<' if right_memory < target_memory else ''}[",
            f"{'>' if target_memory > right_memory else ''}{'<' if target_memory < right_memory else ''}+",
            f"{'>' if temp > target_memory else ''}{'<' if temp < target_memory else ''}+",
            f"{'>' if right_memory > temp else ''}{'<' if right_memory < temp else ''}-]",
            f"{'>' if temp > right_memory else ''}{'<' if temp < right_memory else ''}[",
            f"{'>' if right_memory > temp else ''}{'<' if right_memory < temp else ''}+",
            f"{'>' if temp > right_memory else ''}{'<' if temp < right_memory else ''}-]",
            f"{'>' if left_memory > temp else ''}{'<' if left_memory < temp else ''}-]"
        ])
        
        return brainfuck_code
    
    def translate_modulo(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Precise modulo operation with computational tracking
        """
        # Allocate temporary memory cells
        temp1 = self.memory_manager.allocate_temp_memory()
        temp2 = self.memory_manager.allocate_temp_memory()
        
        # Clear target and temporary memory
        brainfuck_code = self._generate_set_value(target_memory, 0)
        brainfuck_code += self._generate_set_value(temp1, 0)
        brainfuck_code += self._generate_set_value(temp2, 0)
        
        # Modulo algorithm
        brainfuck_code += "".join([
            f"{'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[",
            f"{'>' if temp1 > left_memory else ''}{'<' if temp1 < left_memory else ''}+",
            f"{'>' if left_memory > temp1 else ''}{'<' if left_memory < temp1 else ''}-]",
            f"{'>' if temp1 > left_memory else ''}{'<' if temp1 < left_memory else ''}[",
            f"{'>' if right_memory > temp1 else ''}{'<' if right_memory < temp1 else ''}[",
            f"{'>' if temp2 > right_memory else ''}{'<' if temp2 < right_memory else ''}+",
            f"{'>' if temp1 > temp2 else ''}{'<' if temp1 < temp2 else ''}-",
            f"{'>' if right_memory > temp1 else ''}{'<' if right_memory < temp1 else ''}-]",
            f"{'>' if temp2 > right_memory else ''}{'<' if temp2 < right_memory else ''}[",
            f"{'>' if right_memory > temp2 else ''}{'<' if right_memory < temp2 else ''}+",
            f"{'>' if temp2 > right_memory else ''}{'<' if temp2 < right_memory else ''}-]",
            f"{'>' if temp1 > right_memory else ''}{'<' if temp1 < right_memory else ''}]",
            f"{'>' if target_memory > temp1 else ''}{'<' if target_memory < temp1 else ''}+",
            f"{'>' if temp1 > target_memory else ''}{'<' if temp1 < target_memory else ''}-]"
        ])
        
        return brainfuck_code
    
    def translate_addition(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Precise addition
        """
        brainfuck_code = "".join([
            self._generate_set_value(target_memory, 0),
            f"{'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[",
            f"{'>' if target_memory > left_memory else ''}{'<' if target_memory < left_memory else ''}+",
            f"{'>' if left_memory > target_memory else ''}{'<' if left_memory < target_memory else ''}-]",
            f"{'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[",
            f"{'>' if target_memory > right_memory else ''}{'<' if target_memory < right_memory else ''}+",
            f"{'>' if right_memory > target_memory else ''}{'<' if right_memory < target_memory else ''}-]"
        ])
        
        return brainfuck_code

    def translate_subtraction(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Precise subtraction
        """
        brainfuck_code = "".join([
            self._generate_set_value(target_memory, 0),
            f"{'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[",
            f"{'>' if target_memory > left_memory else ''}{'<' if target_memory < left_memory else ''}+",
            f"{'>' if left_memory > target_memory else ''}{'<' if left_memory < target_memory else ''}-]",
            f"{'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[",
            f"{'>' if target_memory > right_memory else ''}{'<' if target_memory < right_memory else ''}-",
            f"{'>' if right_memory > target_memory else ''}{'<' if right_memory < target_memory else ''}-]"
        ])
        
        return brainfuck_code
