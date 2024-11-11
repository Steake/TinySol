from typing import Dict, Any, Union, List
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
        Initialize node translators with comprehensive result tracking
        """
        super().__init__(memory_manager, max_recursion_depth, max_iterations)
        
        # Initialize specialized translators
        self.statement_translator = StatementTranslator(memory_manager)
        self.expression_translator = ExpressionTranslator(memory_manager)
        self.condition_translator = ConditionTranslator(memory_manager)
        self.arithmetic_translator = ArithmeticTranslator(memory_manager)
        
        # Track output cells and computational steps
        self.output_cells = []
        self.computational_steps = []

    def translate_node(self, node: Dict[str, Any]) -> str:
        """
        Enhanced node translation with explicit result tracking
        """
        node_type = node.get('type', '')
        
        # Map node types to translation methods
        translation_methods = {
            'Program': self.translate_program,
            'VariableDeclaration': self.translate_variable_declaration,
            'AssignmentExpression': self.translate_assignment,
            'ForStatement': self.translate_for_statement,
            'IfStatement': self.translate_if_statement,
            'BinaryExpression': self.expression_translator.translate_expression,
            'Literal': self.expression_translator.translate_expression,
            'Identifier': self.expression_translator.translate_expression
        }
        
        # Find and execute the appropriate translation method
        translator_method = translation_methods.get(node_type)
        
        if translator_method:
            return translator_method(node)
        
        raise TranslationError(f"Unsupported node type: {node_type}")

    def translate_program(self, node: Dict[str, Any]) -> str:
        """
        Enhanced program translation with comprehensive output generation
        """
        brainfuck_code = ""
        for item in node.get('body', []):
            brainfuck_code += self.translate_node(item)
        
        # Generate output for computational results
        result_cells = self.memory_manager.get_computational_result_cells()
        for cell in result_cells:
            brainfuck_code += f"{'>' if cell > 0 else ''}{'<' if cell < 0 else ''}."
        
        return brainfuck_code

    def translate_variable_declaration(self, node: Dict[str, Any]) -> str:
        """
        Enhanced variable declaration with result tracking
        """
        return self.statement_translator.translate_variable_declaration(node)

    def translate_assignment(self, node: Dict[str, Any]) -> str:
        """
        Enhanced assignment translation with explicit output
        """
        return self.statement_translator.translate_assignment(node)

    def translate_for_statement(self, node: Dict[str, Any]) -> str:
        """
        Enhanced for statement translation with comprehensive output
        """
        return self.statement_translator.translate_for_statement(node)

    def translate_if_statement(self, node: Dict[str, Any]) -> str:
        """
        Enhanced if statement translation with comprehensive output
        """
        return self.statement_translator.translate_if_statement(node)

    def _generate_comprehensive_result_preservation(self) -> str:
        """
        Generate advanced result preservation and output mechanism
        
        Returns:
            str: Brainfuck code for result preservation
        """
        result_preservation_code = ""
        
        # Retrieve computational result cells
        result_cells = self.memory_manager.get_computational_result_cells()
        
        if result_cells:
            # Sort cells to ensure consistent output
            result_cells.sort()
            
            # Comprehensive result output strategy
            for cell in result_cells:
                # Navigate to cell and output its value
                result_preservation_code += (
                    f"{'>' if cell > 0 else ''}{'<' if cell < 0 else ''}"
                    "."  # Output cell
                )
        
        return result_preservation_code
