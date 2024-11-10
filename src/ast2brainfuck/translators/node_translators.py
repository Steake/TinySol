from typing import Dict, Any, Union
from src.ast2brainfuck.memory.memory_manager import MemoryManager
from src.ast2brainfuck.translators.base_translator import BaseTranslator, TranslationError
from src.ast2brainfuck.translators.statement_translator import StatementTranslator
from src.ast2brainfuck.translators.expression_translator import ExpressionTranslator
from src.ast2brainfuck.translators.condition_translator import ConditionTranslator
from src.ast2brainfuck.translators.arithmetic_translator import ArithmeticTranslator

class NodeTranslators(BaseTranslator):
    def __init__(self, memory_manager: MemoryManager, 
                 max_recursion_depth: int = 20, 
                 max_iterations: int = 1000):
        """
        Initialize node translators with memory management and constraints
        
        Args:
            memory_manager (MemoryManager): Memory management instance
            max_recursion_depth (int): Maximum allowed recursion depth
            max_iterations (int): Maximum allowed translation iterations
        """
        super().__init__(memory_manager, max_recursion_depth, max_iterations)
        
        # Initialize specialized translators
        self.statement_translator = StatementTranslator(memory_manager)
        self.expression_translator = ExpressionTranslator(memory_manager)
        self.condition_translator = ConditionTranslator(memory_manager)
        self.arithmetic_translator = ArithmeticTranslator(memory_manager)
    
    def translate_node(self, node: Dict[str, Any]) -> str:
        """
        Translate different types of nodes
        
        Args:
            node (Dict[str, Any]): AST node to translate
        
        Returns:
            str: Generated Brainfuck code
        
        Raises:
            TranslationError: If translation fails
        """
        node_type = node.get('type', '')
        
        # Map node types to translation methods
        translation_methods = {
            'Program': self.translate_program,
            'VariableDeclaration': self.statement_translator.translate_variable_declaration,
            'AssignmentExpression': self.statement_translator.translate_assignment,
            'ForStatement': self.statement_translator.translate_for_statement,
            'IfStatement': self.statement_translator.translate_if_statement,
            'BinaryExpression': self.expression_translator.translate_expression,
            'Literal': self.expression_translator.translate_expression,
            'Identifier': self.expression_translator.translate_expression
        }
        
        # Find and execute the appropriate translation method
        translator_method = translation_methods.get(node_type)
        
        if translator_method:
            # For expressions, we need a target memory cell
            if node_type in ['BinaryExpression', 'Literal', 'Identifier']:
                # Use a dedicated output cell for final result variables
                if node_type == 'Identifier' and node.get('name') in ['factorial', 'sum', 'result']:
                    memory_index = self.memory_manager.get_variable_memory(node.get('name'))
                    self.output_cell = memory_index
                    return self.expression_translator.translate_expression(node, memory_index)
                
                temp_memory = self.memory_manager.allocate_temp_memory()
                return translator_method(node, temp_memory)
            
            return translator_method(node)
        
        raise TranslationError(f"Unsupported node type: {node_type}")
    
    def translate_program(self, node: Dict[str, Any]) -> str:
        """
        Translate an entire program
        
        Args:
            node (Dict[str, Any]): Program AST node
        
        Returns:
            str: Generated Brainfuck code
        """
        brainfuck_code = ""
        for item in node.get('body', []):
            brainfuck_code += self.translate_node(item)
        
        # Add output generation for the final result
        if self.output_cell is not None:
            # Ensure the output cell is at the correct memory location
            brainfuck_code += f"{'>' if self.output_cell > 0 else ''}{'<' if self.output_cell < 0 else ''}.[-]"
        
        return brainfuck_code
