from typing import Dict, Any
from src.ast2brainfuck.translators.base_translator import BaseTranslator
from src.ast2brainfuck.translators.expression_translator import ExpressionTranslator

class ConditionTranslator(BaseTranslator):
    def __init__(self, memory_manager, *args, **kwargs):
        super().__init__(memory_manager, *args, **kwargs)
        self.expression_translator = ExpressionTranslator(memory_manager)
    
    def translate_binary_condition(self, node: Dict[str, Any], target_memory: int) -> str:
        """
        Translate binary conditions (==, <=, <, >, >=)
        
        Args:
            node (Dict[str, Any]): Condition node
            target_memory (int): Memory cell to store condition result
        
        Returns:
            str: Brainfuck code for condition
        """
        operator = node.get('operator', '')
        left_node = node.get('left', {})
        right_node = node.get('right', {})
        
        # Allocate temporary memory for operands
        left_memory = self.memory_manager.allocate_temp_memory()
        right_memory = self.memory_manager.allocate_temp_memory()
        
        # Translate left and right operands
        brainfuck_code = self.expression_translator.translate_expression(left_node, left_memory)
        brainfuck_code += self.expression_translator.translate_expression(right_node, right_memory)
        
        # Clear target memory
        brainfuck_code += self._generate_set_value(target_memory, 0)
        
        # Condition translation based on operator
        if operator == '==':
            brainfuck_code += self._translate_equality(left_memory, right_memory, target_memory)
        elif operator == '<=':
            brainfuck_code += self._translate_less_or_equal(left_memory, right_memory, target_memory)
        elif operator == '<':
            brainfuck_code += self._translate_less_than(left_memory, right_memory, target_memory)
        elif operator == '%':
            brainfuck_code += self._translate_modulo_condition(left_memory, right_memory, target_memory)
        
        return brainfuck_code
    
    def translate_logical_or(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Translate logical OR condition
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck code for logical OR
        """
        # Clear target memory
        brainfuck_code = self._generate_set_value(target_memory, 0)
        
        # Check left operand
        brainfuck_code += f"""
        {'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[
            {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
            {'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[-]
        ]
        """
        
        # Check right operand if left was zero
        brainfuck_code += f"""
        {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}[
            {'>' if right_memory > 0 else ''}{'<' if right_memory < 0 else ''}[
                {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
                {'>' if right_memory > 0 else ''}{'<' if right_memory < 0 else ''}[-]
            ]
        ]
        """
        
        return brainfuck_code
    
    def _translate_equality(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Translate equality condition
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck code for equality check
        """
        return f"""
        {'>' if left_memory > right_memory else ''}{'<' if left_memory < right_memory else ''}[
            {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[-]
            {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
            {'>' if left_memory > right_memory else ''}{'<' if left_memory < right_memory else ''}[-]
        ]
        {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[
            {'>' if left_memory > right_memory else ''}{'<' if left_memory < right_memory else ''}[-]
            {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
            {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[-]
        ]
        """
    
    def _translate_less_or_equal(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Translate less than or equal to condition
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck code for less than or equal check
        """
        return f"""
        {'>' if left_memory > right_memory else ''}{'<' if left_memory < right_memory else ''}[
            {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[-]
            {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
            {'>' if left_memory > right_memory else ''}{'<' if left_memory < right_memory else ''}[-]
        ]
        {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[
            {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
            {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[-]
        ]
        """
    
    def _translate_less_than(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Translate less than condition
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck code for less than check
        """
        return f"""
        {'>' if left_memory > right_memory else ''}{'<' if left_memory < right_memory else ''}[
            {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[-]
            {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
            {'>' if left_memory > right_memory else ''}{'<' if left_memory < right_memory else ''}[-]
        ]
        """
    
    def _translate_modulo_condition(self, left_memory: int, right_memory: int, target_memory: int) -> str:
        """
        Translate modulo condition (e.g., i % 3 == 0)
        
        Args:
            left_memory (int): Left operand memory cell
            right_memory (int): Right operand memory cell
            target_memory (int): Result memory cell
        
        Returns:
            str: Brainfuck code for modulo condition
        """
        temp_memory = self.memory_manager.allocate_temp_memory()
        
        return f"""
        {'>' if temp_memory > 0 else ''}{'<' if temp_memory < 0 else ''}[-]
        {'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[
            {'>' if right_memory > left_memory else ''}{'<' if right_memory < left_memory else ''}[
                {'>' if temp_memory > right_memory else ''}{'<' if temp_memory < right_memory else ''}+
                {'>' if left_memory > temp_memory else ''}{'<' if left_memory < temp_memory else ''}[-]
            ]
            {'>' if temp_memory > right_memory else ''}{'<' if temp_memory < right_memory else ''}[
                {'>' if right_memory > temp_memory else ''}{'<' if right_memory < temp_memory else ''}+
            ]
            {'>' if target_memory > 0 else ''}{'<' if target_memory < 0 else ''}+
            {'>' if left_memory > 0 else ''}{'<' if left_memory < 0 else ''}[-]
        ]
        """
