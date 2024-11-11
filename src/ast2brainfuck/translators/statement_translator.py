from typing import Dict, Any
from src.ast2brainfuck.translators.base_translator import BaseTranslator
from src.ast2brainfuck.translators.expression_translator import ExpressionTranslator

class StatementTranslator(BaseTranslator):
    def __init__(self, memory_manager, *args, **kwargs):
        super().__init__(memory_manager, *args, **kwargs)
        self.expression_translator = ExpressionTranslator(memory_manager)
        self.output_cells = []
    
    def translate_node(self, node: Dict[str, Any]) -> str:
        node_type = node.get('type', '')
        translator_method = getattr(self, f'translate_{node_type}', None)
        
        if translator_method:
            return translator_method(node)
        return ""
    
    def translate_variable_declaration(self, node: Dict[str, Any]) -> str:
        var_name = node.get('id', {}).get('name', '')
        initial_value_node = node.get('init', {})
        
        memory_index = self.memory_manager.allocate_variable(var_name)
        
        brainfuck_code = '>' * memory_index
        brainfuck_code += '[-]'  # Clear the cell
        
        if initial_value_node:
            value = initial_value_node.get('value', 0)
            brainfuck_code += '+' * value
        
        self.output_cells.append(memory_index)
        
        return brainfuck_code
    
    def translate_assignment(self, node: Dict[str, Any]) -> str:
        var_name = node.get('left', {}).get('name', '')
        value_node = node.get('right', {})
        
        memory_index = self.memory_manager.get_variable_memory(var_name)
        
        # Clear the target memory cell before assignment
        brainfuck_code = self._generate_set_value(memory_index, 0)
        
        # Translate the right-hand side expression
        brainfuck_code += self.expression_translator.translate_expression(value_node, memory_index)
        
        return brainfuck_code
    
    def translate_for_statement(self, node: Dict[str, Any]) -> str:
        init_node = node.get('init', {})
        test_node = node.get('test', {})
        update_node = node.get('update', {})
        body_node = node.get('body', {})
        
        brainfuck_code = self.translate_node(init_node)
        
        loop_counter = self.memory_manager.allocate_temp_memory()
        condition_memory = self.memory_manager.allocate_temp_memory()
        
        # Start of loop
        brainfuck_code += ">"  # Move to loop counter
        brainfuck_code += "+"  # Set initial condition to true
        brainfuck_code += "["  # Start loop
        
        # Test condition
        brainfuck_code += self.expression_translator.translate_expression(test_node, condition_memory)
        brainfuck_code += f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}["
        
        # Loop body
        brainfuck_code += self.translate_node(body_node)
        
        # Inner loop to repeat until condition is false
        brainfuck_code += f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[-]"
        brainfuck_code += "]"
        
        # Update
        brainfuck_code += self.translate_node(update_node)
        
        # Close inner loop
        brainfuck_code += f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}]"
        
        # Test condition again
        brainfuck_code += self.expression_translator.translate_expression(test_node, condition_memory)
        
        # Close outer loop
        brainfuck_code += "]"
        
        return brainfuck_code
    
    def translate_if_statement(self, node: Dict[str, Any]) -> str:
        test_node = node.get('test', {})
        consequent_node = node.get('consequent', {})
        alternate_node = node.get('alternate', {})
        
        condition_memory = self.memory_manager.allocate_temp_memory()
        
        brainfuck_code = self.expression_translator.translate_expression(test_node, condition_memory)
        
        brainfuck_code += f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}["
        brainfuck_code += self.translate_node(consequent_node)
        brainfuck_code += f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[-]]"
        
        if alternate_node:
            brainfuck_code += f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}+"
            brainfuck_code += "["
            brainfuck_code += self.translate_node(alternate_node)
            brainfuck_code += f"{'>' if condition_memory > 0 else ''}{'<' if condition_memory < 0 else ''}[-]]"
        
        return brainfuck_code

    def translate_block_statement(self, node: Dict[str, Any]) -> str:
        brainfuck_code = ""
        for statement in node.get('body', []):
            brainfuck_code += self.translate_node(statement)
        return brainfuck_code

    def _generate_output_code(self) -> str:
        """Generate code to output all tracked variables, including zeros"""
        output_code = ""
        for cell in range(max(self.output_cells) + 1):
            output_code += f"{'>' * cell}."
        return output_code

    def _generate_set_value(self, memory_index: int, value: int) -> str:
        """Generate Brainfuck code to set a memory cell to a specific value"""
        return f"{'>' * memory_index}[-]{'+' * value}"
