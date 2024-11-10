from typing import Dict, Any
from src.ast2brainfuck.translators.base_translator import BaseTranslator
from src.ast2brainfuck.translators.expression_translator import ExpressionTranslator

class StatementTranslator(BaseTranslator):
    def __init__(self, memory_manager, *args, **kwargs):
        super().__init__(memory_manager, *args, **kwargs)
        self.expression_translator = ExpressionTranslator(memory_manager)
    
    def translate_node(self, node: Dict[str, Any]) -> str:
        """
        Translate different types of nodes
        
        Args:
            node (Dict[str, Any]): AST node to translate
        
        Returns:
            str: Brainfuck code for the node
        """
        node_type = node.get('type', '')
        translator_method = getattr(self, f'translate_{node_type}', None)
        
        if translator_method:
            return translator_method(node)
        return ""
    
    def translate_variable_declaration(self, node: Dict[str, Any]) -> str:
        """
        Translate variable declaration to Brainfuck
        
        Args:
            node (Dict[str, Any]): Variable declaration node
        
        Returns:
            str: Brainfuck code for variable initialization
        """
        var_name = node.get('name', '')
        initial_value_node = node.get('init', {})
        
        # Allocate memory for the variable
        memory_index = self.memory_manager.allocate_variable(var_name)
        
        # If there's an initial value, translate the expression
        if initial_value_node:
            brainfuck_code = self.expression_translator.translate_expression(initial_value_node, memory_index)
        else:
            # Default to zero if no initial value
            brainfuck_code = self._generate_set_value(memory_index, 0)
        
        # Track output cell for final result variables
        if var_name in ['factorial', 'sum', 'result']:
            self.output_cell = memory_index
        
        return brainfuck_code
    
    def translate_assignment(self, node: Dict[str, Any]) -> str:
        """
        Translate assignment operation to Brainfuck
        
        Args:
            node (Dict[str, Any]): Assignment node
        
        Returns:
            str: Brainfuck code for assignment
        """
        var_name = node.get('left', {}).get('name', '')
        value_node = node.get('right', {})
        
        # Get memory location for the variable
        memory_index = self.memory_manager.get_variable_memory(var_name)
        
        # Allocate temporary memory for complex expressions
        temp_memory = self.memory_manager.allocate_temp_memory()
        
        # Translate the right-hand side expression
        brainfuck_code = self.expression_translator.translate_expression(value_node, temp_memory)
        
        # Copy result to target memory
        brainfuck_code += self._copy_memory_value(temp_memory, memory_index)
        
        # Update output cell if needed
        if var_name in ['factorial', 'sum', 'result']:
            self.output_cell = memory_index
        
        return brainfuck_code
    
    def translate_for_statement(self, node: Dict[str, Any]) -> str:
        """
        Translate for loop to Brainfuck
        
        Args:
            node (Dict[str, Any]): For statement node
        
        Returns:
            str: Brainfuck code for the loop
        """
        init_node = node.get('init', {})
        test_node = node.get('test', {})
        body_node = node.get('body', {})
        
        # Translate initialization
        if init_node.get('declarations'):
            init_declaration = init_node.get('declarations', [{}])[0]
            brainfuck_code = self.translate_variable_declaration(init_declaration)
        else:
            brainfuck_code = ""
        
        # Allocate memory for loop variables and condition
        loop_var_name = init_node.get('declarations', [{}])[0].get('name', '')
        limit_var_name = test_node.get('right', {}).get('name', '')
        
        loop_var_memory = self.memory_manager.get_variable_memory(loop_var_name)
        limit_memory = self.memory_manager.get_variable_memory(limit_var_name)
        condition_memory = self.memory_manager.allocate_temp_memory()
        
        # Translate loop with condition handling
        brainfuck_code += "".join([
            "[",  # Outer loop
            f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[-]",
            f"{'>' if loop_var_memory > 0 else ''}{'<' if loop_var_memory < 0 else ''}[",
            f"{'>' if limit_memory > 0 else ''}{'<' if limit_memory < 0 else ''}[",
            f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}+",
            f"{'>' if limit_memory > 0 else ''}{'<' if limit_memory < 0 else ''}[-]",
            "]",
            f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[",
            f"{'>' if loop_var_memory > 0 else ''}{'<' if loop_var_memory < 0 else ''}+",
            f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[-]",
            "]",
            self.translate_node(body_node),
            f"{'>' if loop_var_memory > 0 else ''}{'<' if loop_var_memory < 0 else ''}+",
            f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[-]",
            "]",
            f"{'>' if loop_var_memory > 0 else ''}{'<' if loop_var_memory < 0 else ''}[-]",
            "]"
        ])
        
        return brainfuck_code
    
    def translate_if_statement(self, node: Dict[str, Any]) -> str:
        """
        Translate if statement to Brainfuck
        
        Args:
            node (Dict[str, Any]): If statement node
        
        Returns:
            str: Brainfuck code for the if statement
        """
        test_node = node.get('test', {})
        consequent_node = node.get('consequent', {})
        
        # Allocate memory for condition result
        condition_memory = self.memory_manager.allocate_temp_memory()
        
        # Translate condition
        brainfuck_code = self.expression_translator.translate_expression(test_node, condition_memory)
        
        # Translate consequent body with condition check
        brainfuck_code += "".join([
            f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[",
            self.translate_node(consequent_node),
            f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[-]",
            "]"
        ])
        
        return brainfuck_code
