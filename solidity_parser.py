
import re

class SolidityParser:
    def parse_variable(self, line):
        match = re.match(r'int\s+(\w+)\s*=\s*(\d+);', line)
        if match:
            var_name, value = match.groups()
            return ('variable', {'name': var_name, 'value': int(value)})
        return None

    def parse_for_loop(self, line):
        match = re.match(r'for\s*\((.*);(.*);(.*)\)', line)
        if match:
            initialization, condition, iteration = match.groups()
            return ('for_loop', {'initialization': initialization.strip(), 
                                 'condition': condition.strip(), 
                                 'iteration': iteration.strip()})
        return None

    def parse_if_else(self, line):
        if 'if' in line:
            condition = line.split('(')[1].split(')')[0]
            return ('if', {'condition': condition})
        elif 'else' in line:
            return ('else', {})
        return None

    def parse(self, code):
        parsed_code = []
        lines = code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if 'int' in line:
                parsed_code.append(self.parse_variable(line))
            elif line.startswith('for'):
                parsed_code.append(self.parse_for_loop(line))
            elif line.startswith('if') or line.startswith('else'):
                parsed_code.append(self.parse_if_else(line))
        return parsed_code
