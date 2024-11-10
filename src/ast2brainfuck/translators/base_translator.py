from typing import Dict, Any
from src.ast2brainfuck.memory.memory_manager import MemoryManager

class TranslationError(Exception):
    """Custom exception for translation errors"""
    pass

class BaseTranslator:
    def __init__(self, memory_manager: MemoryManager, 
                 max_recursion_depth: int = 20, 
                 max_iterations: int = 1000):
        """
        Initialize base translator with memory management and constraints
        
        Args:
            memory_manager (MemoryManager): Memory management instance
            max_recursion_depth (int): Maximum allowed recursion depth
            max_iterations (int): Maximum allowed translation iterations
        """
        self.memory_manager = memory_manager
        self.max_recursion_depth = max_recursion_depth
        self.max_iterations = max_iterations
        self.output_cell = None  # Track the final output cell
    
    def _generate_set_value(self, memory_index: int, value: int) -> str:
        """
        Generate Brainfuck code to set a specific value in memory
        
        Args:
            memory_index (int): Memory cell index
            value (int): Value to set
        
        Returns:
            str: Brainfuck code to set value
        """
        # Clear memory cell first
        clear_code = f"{'>' if memory_index > 0 else ''}{'<' if memory_index < 0 else ''}[-]"
        
        # Set value
        set_code = f"{'>' if memory_index > 0 else ''}{'<' if memory_index < 0 else ''}{'+'*value}"
        
        return clear_code + set_code
    
    def _copy_memory_value(self, source_memory: int, target_memory: int) -> str:
        """
        Generate Brainfuck code to copy value between memory cells
        
        Args:
            source_memory (int): Source memory cell index
            target_memory (int): Target memory cell index
        
        Returns:
            str: Brainfuck code to copy value
        """
        # Clear target memory first
        clear_code = f"{'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}[-]"
        
        # Copy value from source to target
        copy_code = f"""
        {'>' if source_memory > target_memory else ''}{'<' if source_memory < target_memory else ''}[
            {'>' if target_memory > source_memory else ''}{'<' if target_memory < source_memory else ''}+
            {'>' if source_memory > target_memory else ''}{'<' if source_memory < target_memory else ''}[-]
        ]
        """
        
        return clear_code + copy_code
    
    def _generate_output(self, memory_cell: int) -> str:
        """
        Generate Brainfuck code to output a memory cell's value
        
        Args:
            memory_cell (int): Memory cell to output
        
        Returns:
            str: Brainfuck output code
        """
        # Output the value and then reset the cell
        return f"{'>' if memory_cell > 0 else ''}{'<' if memory_cell < 0 else ''}.[-]"
