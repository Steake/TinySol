class MemoryManager:
    def __init__(self, initial_size=30000):
        """
        Initialize memory management for Brainfuck translation
        with enhanced computational result tracking
        
        Args:
            initial_size (int): Initial memory tape size, default is 30000 cells
        """
        self.memory_size = initial_size
        self.current_memory_pointer = 0
        self.variable_memory_map = {}
        self.temp_memory_map = {}
        
        # Enhanced tracking of computational results
        self.computational_result_cells = []
        self.variable_significance = {}

    def allocate_variable(self, variable_name, initial_value=0, is_computational_result=False, significance_level=0):
        """
        Allocate memory for a variable with enhanced tracking
        
        Args:
            variable_name (str): Name of the variable
            initial_value (int): Initial value for the variable
            is_computational_result (bool): Flag to mark as a computational result cell
            significance_level (int): Importance of the variable in computation
        
        Returns:
            int: Memory cell index for the variable
        """
        if variable_name in self.variable_memory_map:
            return self.variable_memory_map[variable_name]
        
        memory_index = self.current_memory_pointer
        self.variable_memory_map[variable_name] = memory_index
        self.current_memory_pointer += 1
        
        # Track computational result cells
        if is_computational_result:
            if memory_index not in self.computational_result_cells:
                self.computational_result_cells.append(memory_index)
        
        # Track variable significance
        self.variable_significance[memory_index] = {
            'name': variable_name,
            'is_result': is_computational_result,
            'significance': significance_level
        }
        
        return memory_index

    def get_variable_memory(self, variable_name):
        """
        Get memory location for a variable
        
        Args:
            variable_name (str): Name of the variable
        
        Returns:
            int: Memory cell index for the variable
        """
        return self.variable_memory_map.get(variable_name, -1)

    def allocate_temp_memory(self, purpose=None):
        """
        Allocate a temporary memory cell
        
        Args:
            purpose (str, optional): Purpose of the temporary memory
        
        Returns:
            int: Memory cell index for temporary storage
        """
        temp_index = self.current_memory_pointer
        self.current_memory_pointer += 1
        
        if purpose:
            self.temp_memory_map[temp_index] = purpose
        
        return temp_index

    def reset_temp_memory(self):
        """
        Reset temporary memory tracking
        """
        self.temp_memory_map.clear()

    def get_computational_result_cells(self):
        """
        Retrieve computational result cells
        
        Returns:
            List[int]: Memory cell indices of computational results
        """
        return sorted(self.computational_result_cells)

    def mark_as_computational_result(self, memory_index, significance_level=1):
        """
        Mark a memory cell as a computational result
        
        Args:
            memory_index (int): Memory cell index to mark
            significance_level (int): Importance of the computational result
        """
        if memory_index not in self.computational_result_cells:
            self.computational_result_cells.append(memory_index)
        
        # Update significance tracking
        self.variable_significance[memory_index] = {
            'is_result': True,
            'significance': significance_level
        }

    def get_most_significant_result(self):
        """
        Get the most significant computational result cell
        
        Returns:
            Optional[int]: Memory index of the most significant result
        """
        if not self.computational_result_cells:
            return None
        
        # Sort result cells by significance
        sorted_results = sorted(
            self.computational_result_cells, 
            key=lambda x: self.variable_significance.get(x, {}).get('significance', 0), 
            reverse=True
        )
        
        return sorted_results[0] if sorted_results else None

    def get_memory_usage_summary(self):
        """
        Provide a summary of memory usage
        
        Returns:
            Dict: Memory usage statistics
        """
        return {
            'total_cells': self.current_memory_pointer,
            'variables': len(self.variable_memory_map),
            'computational_results': len(self.computational_result_cells),
            'temporary_cells': len(self.temp_memory_map)
        }
