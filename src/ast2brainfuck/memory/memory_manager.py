class MemoryManager:
    def __init__(self, initial_size=30000):
        """
        Initialize memory management for Brainfuck translation
        
        Args:
            initial_size (int): Initial memory tape size, default is 30000 cells
        """
        self.memory_size = initial_size
        self.current_memory_pointer = 0
        self.variable_memory_map = {}
        self.temp_memory_map = {}
    
    def allocate_variable(self, variable_name, initial_value=0):
        """
        Allocate memory for a variable and track its memory location
        
        Args:
            variable_name (str): Name of the variable
            initial_value (int): Initial value for the variable
        
        Returns:
            int: Memory cell index for the variable
        """
        if variable_name in self.variable_memory_map:
            return self.variable_memory_map[variable_name]
        
        memory_index = self.current_memory_pointer
        self.variable_memory_map[variable_name] = memory_index
        self.current_memory_pointer += 1
        
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
    
    def allocate_temp_memory(self):
        """
        Allocate a temporary memory cell
        
        Returns:
            int: Memory cell index for temporary storage
        """
        temp_index = self.current_memory_pointer
        self.current_memory_pointer += 1
        return temp_index
    
    def reset_temp_memory(self):
        """
        Reset temporary memory tracking
        """
        self.temp_memory_map.clear()
