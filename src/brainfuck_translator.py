
class BrainfuckTranslator:
    def translate_variable(self, variable):
        name, value = variable['name'], variable['value']
        return '>' * (ord(name) - ord('a') + 1) + '+' * value

    def translate_for_loop(self, for_loop):
        return '[->+<]'

    def translate_if_else(self, if_else):
        condition = if_else.get('condition', '')
        return '[>]' if condition else '[<]'

    def translate(self, parsed_code):
        bf_code = ''
        for command, details in parsed_code:
            if command == 'variable':
                bf_code += self.translate_variable(details)
            elif command == 'for_loop':
                bf_code += self.translate_for_loop(details)
            elif command == 'if' or command == 'else':
                bf_code += self.translate_if_else(details)
        return bf_code
