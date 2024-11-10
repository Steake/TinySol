import re
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

class ArrayNode(ASTNode):
    def __init__(self, name, dimensions, element_type='int'):
        super().__init__('Array')
        self.name = name
        self.dimensions = dimensions
        self.element_type = element_type

class ArrayAccessNode(ASTNode):
    def __init__(self, array_name, indices):
        super().__init__('ArrayAccess')
        self.array_name = array_name
        self.indices = indices

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, return_type, body):
        super().__init__('Function')
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

class SolidityParser:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.current_scope = [{}]
        self.max_recursion_depth = 50  # Prevent excessive recursion

    def tokenize(self, code: str) -> List[str]:
        """
        Enhanced tokenization with robust error handling
        
        :param code: Raw TinySol code
        :return: List of tokens
        """
        try:
            # Remove comments
            code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.DOTALL)
            code = code.replace('\n', ' ').replace('\t', ' ')
            
            # Enhanced tokenization pattern
            pattern = r'(int\[.*?\]|int|return|while|if|else|==|!=|>=|<=|>|<|\+|-|\*|/|=|\(|\)|\{|\}|\[|\]|;|\w+|\d+)'
            tokens = re.findall(pattern, code)
            
            logger.debug(f"Tokenization result: {tokens}")
            return tokens
        except Exception as e:
            logger.error(f"Tokenization error: {e}")
            raise

    def parse(self, code: str, depth=0) -> ASTNode:
        """
        Enhanced parsing with robust error handling and recursion limit
        
        :param code: Raw TinySol code
        :param depth: Current recursion depth
        :return: Root AST node
        """
        if depth > self.max_recursion_depth:
            raise RecursionError("Maximum parsing depth exceeded")

        try:
            tokens = self.tokenize(code)
            root = ASTNode('Program')
            
            logger.debug(f"Starting parsing with tokens: {tokens}")
            
            while tokens:
                try:
                    if self._is_array_declaration(tokens):
                        array_node = self._parse_array_declaration(tokens)
                        root.children.append(array_node)
                        tokens = tokens[tokens.index(';') + 1:] if ';' in tokens else []
                    elif tokens[0] == 'int' and len(tokens) > 2 and tokens[2] == '(':
                        # Function definition
                        function_node = self._parse_function_definition(tokens)
                        root.children.append(function_node)
                        tokens = tokens[tokens.index('}') + 1:] if '}' in tokens else []
                    else:
                        # Regular statement parsing
                        statement = self._parse_statement(tokens, depth + 1)
                        if statement:
                            root.children.append(statement)
                            tokens = tokens[tokens.index(';') + 1:] if ';' in tokens else []
                        else:
                            # If no statement could be parsed, break to prevent infinite loop
                            logger.warning(f"Unable to parse tokens: {tokens}")
                            break
                except Exception as parse_error:
                    logger.error(f"Error parsing tokens {tokens}: {parse_error}")
                    break
            
            return root
        except Exception as e:
            logger.error(f"Parsing error: {e}")
            raise

    def _is_array_declaration(self, tokens: List[str]) -> bool:
        """
        Check if tokens represent an array declaration
        
        :param tokens: List of tokens
        :return: Boolean indicating array declaration
        """
        try:
            return (len(tokens) > 2 and 
                    tokens[0] == 'int' and 
                    '[' in tokens[1] and 
                    ']' in tokens[1])
        except Exception as e:
            logger.error(f"Error in array declaration check: {e}")
            return False

    def _parse_function_definition(self, tokens: List[str]) -> FunctionNode:
        """
        Parse function definition with improved error handling and loop prevention
        
        :param tokens: List of tokens
        :return: Function AST node
        """
        try:
            # Extract function details
            return_type = tokens.pop(0)  # 'int'
            function_name = tokens.pop(0)
            tokens.pop(0)  # Remove '('
            
            # Parse parameters
            parameters = []
            while tokens and tokens[0] != ')':
                param_type = tokens.pop(0)
                param_name = tokens.pop(0)
                parameters.append({'type': param_type, 'name': param_name})
                if tokens and tokens[0] == ',':
                    tokens.pop(0)
            
            if not tokens or tokens[0] != ')':
                raise ValueError("Expected ')' after function parameters")
            tokens.pop(0)  # Remove ')'
            
            if not tokens or tokens[0] != '{':
                raise ValueError("Expected '{' after function declaration")
            tokens.pop(0)  # Remove '{'
            
            # Parse function body
            body = ASTNode('Block')
            brace_count = 1  # Track nested braces
            max_iterations = 1000  # Prevent infinite loops
            iterations = 0
            
            while tokens and brace_count > 0 and iterations < max_iterations:
                if tokens[0] == '{':
                    brace_count += 1
                elif tokens[0] == '}':
                    brace_count -= 1
                
                if brace_count == 0:
                    break
                
                statement = self._parse_statement(tokens)
                if statement:
                    body.children.append(statement)
                    if tokens and tokens[0] == ';':
                        tokens.pop(0)  # Remove ';'
                else:
                    # If no statement could be parsed, move to next token
                    tokens.pop(0)
                
                iterations += 1
            
            if iterations == max_iterations:
                raise ValueError("Function body parsing exceeded maximum iterations")
            
            if not tokens or tokens[0] != '}':
                raise ValueError("Expected '}' at end of function body")
            tokens.pop(0)  # Remove '}'
            
            return FunctionNode(function_name, parameters, return_type, body)
        except Exception as e:
            logger.error(f"Error parsing function definition: {e}")
            raise

    def _parse_array_declaration(self, tokens: List[str]) -> ArrayNode:
        """
        Parse array declaration
        
        :param tokens: List of tokens
        :return: Array AST node
        """
        # Remove 'int'
        tokens.pop(0)
        
        # Parse array declaration
        array_def = tokens.pop(0)
        
        # Extract array name and dimensions
        match = re.match(r'(\w+)(\[.*?\])', array_def)
        if not match:
            raise ValueError(f"Invalid array declaration: {array_def}")
        
        array_name = match.group(1)
        dimensions_str = match.group(2)
        
        # Parse dimensions
        dimensions = [int(d) for d in re.findall(r'\d+', dimensions_str)]
        
        # Optional initialization
        if tokens and tokens[0] == '=':
            tokens.pop(0)  # Remove '='
            # TODO: Implement array initialization parsing
        
        return ArrayNode(array_name, dimensions)

    def _parse_statement(self, tokens: List[str], depth=0) -> ASTNode:
        """
        Enhanced statement parsing with array access support
        
        :param tokens: List of tokens
        :param depth: Current recursion depth
        :return: Appropriate AST node
        """
        if depth > self.max_recursion_depth:
            raise RecursionError("Maximum statement parsing depth exceeded")

        try:
            if not tokens:
                return None

            if tokens[0] == 'int':
                return self._parse_variable_declaration(tokens)
            elif self._is_array_access(tokens[0], tokens):
                return self._parse_array_access(tokens)
            elif tokens[0] in ['while', 'if']:
                return self._parse_control_flow(tokens, depth)
            elif self._is_assignment(tokens[0], tokens):
                return self._parse_assignment(tokens)
            elif self._is_function_call(tokens[0], tokens):
                return self._parse_function_call(tokens)
            return None
        except Exception as e:
            logger.error(f"Error parsing statement: {e}")
            raise

    def _is_array_access(self, token, tokens):
        """
        Check if tokens represent an array access
        """
        try:
            return (len(tokens) > 2 and 
                    tokens[1] == '[' and 
                    ']' in tokens)
        except Exception as e:
            logger.error(f"Error in array access check: {e}")
            return False

    def _parse_array_access(self, tokens: List[str]) -> ArrayAccessNode:
        """
        Parse array access
        
        :param tokens: List of tokens
        :return: Array access AST node
        """
        try:
            array_name = tokens.pop(0)
            tokens.pop(0)  # Remove '['
            
            indices = []
            while tokens[0] != ']':
                index = tokens.pop(0)
                indices.append(index)
                if tokens[0] == ',':
                    tokens.pop(0)
            
            tokens.pop(0)  # Remove ']'
            
            return ArrayAccessNode(array_name, indices)
        except Exception as e:
            logger.error(f"Error parsing array access: {e}")
            raise

    def _parse_variable_declaration(self, tokens):
        """
        Parse variable declaration with optional initialization
        """
        try:
            # Remove 'int'
            tokens.pop(0)
            
            # Variable name
            name = tokens.pop(0)
            
            # Optional assignment
            if tokens and tokens[0] == '=':
                tokens.pop(0)  # Remove '='
                value = tokens.pop(0)  # Get value
                return ASTNode('VariableDeclaration', 
                               {'name': name, 'value': value})
            
            return ASTNode('VariableDeclaration', {'name': name})
        except Exception as e:
            logger.error(f"Error parsing variable declaration: {e}")
            raise

    def _is_assignment(self, token, tokens):
        """
        Check if tokens represent an assignment
        """
        try:
            return (len(tokens) > 2 and 
                    tokens[1] == '=')
        except Exception as e:
            logger.error(f"Error in assignment check: {e}")
            return False

    def _parse_assignment(self, tokens):
        """
        Parse assignment with support for simple and complex expressions
        """
        try:
            variable = tokens.pop(0)
            tokens.pop(0)  # Remove '='
            
            # Collect expression tokens
            expression = []
            while tokens and tokens[0] != ';':
                expression.append(tokens.pop(0))
            
            return ASTNode('Assignment', 
                           {'variable': variable, 
                            'value': ' '.join(expression)})
        except Exception as e:
            logger.error(f"Error parsing assignment: {e}")
            raise

    def _is_function_call(self, token, tokens):
        """
        Check if tokens represent a function call
        """
        try:
            return (len(tokens) > 2 and 
                    tokens[1] == '(')
        except Exception as e:
            logger.error(f"Error in function call check: {e}")
            return False

    def _parse_function_call(self, tokens):
        """
        Parse function call with arguments
        """
        try:
            function_name = tokens.pop(0)
            tokens.pop(0)  # Remove '('
            
            arguments = []
            while tokens[0] != ')':
                arg = tokens.pop(0)
                arguments.append(arg)
                if tokens[0] == ',':
                    tokens.pop(0)
            
            tokens.pop(0)  # Remove ')'
            
            return ASTNode('FunctionCall', 
                           {'name': function_name, 
                            'arguments': arguments})
        except Exception as e:
            logger.error(f"Error parsing function call: {e}")
            raise

    def _parse_expression(self, tokens):
        """
        Parse simple arithmetic expressions
        """
        try:
            # Collect expression tokens
            expression = []
            while tokens and tokens[0] not in [';', ')', ']']:
                expression.append(tokens.pop(0))
            
            return ASTNode('Expression', 
                           {'value': ' '.join(expression)})
        except Exception as e:
            logger.error(f"Error parsing expression: {e}")
            raise

    def _parse_control_flow(self, tokens, depth=0):
        """
        Parse control flow statements (if, while)
        """
        if depth > self.max_recursion_depth:
            raise RecursionError("Maximum control flow parsing depth exceeded")

        try:
            control_type = tokens.pop(0)  # 'if' or 'while'
            tokens.pop(0)  # Remove '('
            
            # Parse condition
            condition = []
            while tokens[0] != ')':
                condition.append(tokens.pop(0))
            
            tokens.pop(0)  # Remove ')'
            tokens.pop(0)  # Remove '{'
            
            # Parse body
            body = ASTNode('Block')
            while tokens[0] != '}':
                statement = self._parse_statement(tokens, depth + 1)
                if statement:
                    body.children.append(statement)
                    if tokens and tokens[0] == ';':
                        tokens.pop(0)  # Remove ';'
            
            tokens.pop(0)  # Remove '}'
            
            return ASTNode(control_type.capitalize(), 
                           {'condition': ' '.join(condition), 
                            'body': body})
        except Exception as e:
            logger.error(f"Error parsing control flow: {e}")
            raise
