import logging
from typing import Union, Dict, Any, List
from src.solidity_parser import ASTNode, parse
from src.ast2brainfuck.memory.memory_manager import MemoryManager
from src.ast2brainfuck.translators.node_translators import NodeTranslators, TranslationError

def translate_to_brainfuck(tinysol_code: str) -> str:
    """
    Translate TinySol code to Brainfuck with comprehensive result preservation
    
    Args:
        tinysol_code (str): TinySol source code
    
    Returns:
        str: Generated Brainfuck code
    """
    # Parse TinySol code to AST
    ast_node = parse(tinysol_code)
    
    # Create translator
    translator = TinySolToBrainfuckTranslator()
    
    # Translate AST to Brainfuck
    brainfuck_code = translator.translate(ast_node)
    
    # Generate output code
    output_code = translator.node_translators._generate_output_code()
    
    # Combine translated code with output code
    brainfuck_code += output_code
    
    return brainfuck_code

class TinySolToBrainfuckTranslator:
    """
    Advanced translator for converting TinySol AST to Brainfuck code
    with comprehensive result preservation
    """
    def __init__(self, 
                 max_recursion_depth: int = 20, 
                 max_iterations: int = 1000, 
                 log_level: int = logging.WARNING):
        """
        Initialize the translator with enhanced result tracking
        """
        # Configure logging
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

        # Initialize memory and translation managers
        self.memory_manager = MemoryManager()
        self.node_translators = NodeTranslators(
            self.memory_manager, 
            max_recursion_depth, 
            max_iterations
        )

    def translate(self, node: Union[ASTNode, Dict, Any]) -> str:
        """
        Translate an AST node to Brainfuck code with result tracking
        """
        try:
            return self.node_translators.translate_node(node)
        except Exception as e:
            self.logger.error(f"Translation failed: {e}")
            raise TranslationError(f"Translation failed: {e}") from e

def generate_brainfuck(node: Union[ASTNode, Dict, Any], 
                       max_recursion_depth: int = 20, 
                       max_iterations: int = 1000, 
                       log_level: int = logging.WARNING) -> str:
    """
    Convenience function to generate Brainfuck code from an AST node
    """
    translator = TinySolToBrainfuckTranslator(
        max_recursion_depth, 
        max_iterations, 
        log_level
    )
    return translator.translate(node)
