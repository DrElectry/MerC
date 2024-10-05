import re
import sys
import os
import time

class MerCCompiler:
    def __init__(self):
        self.variables = {}
        self.lists = {}

    def parse(self, code):
        # Split the code into lines
        lines = code.strip().split('\n')

        # Check for the required start and end commands
        if lines[0].strip() != "bonjour":
            raise SyntaxError("The program must start with 'bonjour'")
        if lines[-1].strip() != "au revoir":
            raise SyntaxError("The program must end with 'au revoir'")

        # Process each line of the program
        self.process_lines(lines[1:-1])

    def process_lines(self, lines):
        """Process each line of the code."""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line:  # Ignore empty lines
                i = self.process_line(line, lines, i)
            else:
                i += 1  # Skip empty line

    def process_line(self, line, lines, current_index):
        # Remove comments
        line = self.remove_comments(line)

        # Ignore empty lines after comment removal
        if not line:
            return current_index + 1

        # Match 'talktoseniour>insert text here<'
        match_talk = re.match(r'talktoseniour>(.*?)<', line)
        if match_talk:
            text_to_print = match_talk.group(1)
            # Replace variable names in the text with their values
            for var in self.variables:
                text_to_print = text_to_print.replace(var, str(self.variables[var]))
            # Replace list values
            for list_name in self.lists:
                text_to_print = text_to_print.replace(list_name, str(self.lists[list_name]))
            print(text_to_print)
            return current_index + 1

        # Match list declaration
        match_list_declaration = re.match(r'the\s*eiffel\s*tower\s*(\w+)\s*=\s*\[(.*?)\]', line)
        if match_list_declaration:
            list_name = match_list_declaration.group(1)
            elements = match_list_declaration.group(2).split(',')
            self.lists[list_name] = [self.evaluate_part(el.strip()) for el in elements]
            return current_index + 1

        # Match variable declarations
        match_declaration = re.match(r'(baguette|tea\s*liters|clever\s*joke|vrai)\s*(\w+)', line)
        if match_declaration:
            var_type, var_name = match_declaration.groups()
            if var_type == "baguette":
                self.variables[var_name] = 0
            elif var_type == "tea liters":
                self.variables[var_name] = 0.0
            elif var_type == "clever joke":
                self.variables[var_name] = ""
            elif var_type == "vrai":
                self.variables[var_name] = False  # Default boolean value
            return current_index + 1

        # Match variable assignment
        match_assignment = re.match(r'(\w+)\s*=\s*(.*)', line)
        if match_assignment:
            var_name = match_assignment.group(1)
            value = match_assignment.group(2).strip()
            if var_name in self.variables:
                # Evaluate the expression
                try:
                    self.variables[var_name] = self.evaluate_expression(value)
                except Exception as e:
                    raise SyntaxError(f"Error assigning to variable '{var_name}': {e}")
            else:
                raise SyntaxError(f"Variable '{var_name}' is not declared.")
            return current_index + 1

        # Match 'imagine' statement with parentheses
        match_imagine = re.match(r'imagine\s*\(\s*(.+?)\s*\)', line)
        if match_imagine:
            condition = match_imagine.group(1).strip()
            if self.evaluate_condition(condition):
                # Process lines until a corresponding "meanwhile" or "au revoir"
                inner_index = current_index + 1
                while inner_index < len(lines):
                    inner_line = lines[inner_index].strip()
                    if inner_line.startswith("meanwhile"):
                        return inner_index + 1  # Skip to next line
                    elif inner_line == "au revoir":
                        return inner_index  # End of program
                    self.process_line(inner_line, lines, inner_index)
                    inner_index += 1
                return inner_index  # Return to the current position after processing

            # If the condition is false, skip to the next line after 'meanwhile'
            inner_index = current_index + 1
            while inner_index < len(lines):
                inner_line = lines[inner_index].strip()
                if inner_line.startswith("meanwhile"):
                    return inner_index + 1  # Move to the next line after 'meanwhile'
                inner_index += 1
            return inner_index  # Return current position after handling 'imagine'

        # Match 'make tea until' statement
        match_make_tea = re.match(r'make tea until\s*\((.*?)\)', line)
        if match_make_tea:
            condition = match_make_tea.group(1).strip()
            while not self.evaluate_condition(condition):
                inner_index = current_index + 1
                while inner_index < len(lines):
                    inner_line = lines[inner_index].strip()
                    if inner_line.startswith("au revoir"):
                        return inner_index  # End of program
                    self.process_line(inner_line, lines, inner_index)
                    inner_index += 1
            return current_index + 1  # Return after the loop finishes

        # Match 'wakebacktoreality' command
        if line.strip() == "wakebacktoreality":
            # Placeholder for handling end of ongoing commands
            return current_index + 1

        # Match 'AmericaWin' error command
        if line.strip() == "AmericaWin":
            raise RuntimeError("An error has occurred: America has won!")

        raise SyntaxError(f"Unknown command: {line}")

    def evaluate_expression(self, expr):
        """Evaluate an arithmetic or boolean expression."""
        # For this basic example, split the expression into parts and evaluate them.
        parts = expr.split()
        return self.perform_operations(parts)

    def perform_operations(self, parts):
        """Perform the operations on the evaluated parts."""
        result = self.evaluate_part(parts[0])  # Start with the first element's evaluated value
        i = 1
        while i < len(parts):
            operator = parts[i]
            next_value = self.evaluate_part(parts[i + 1])
            if operator == '+':
                result += next_value
            elif operator == '-':
                result -= next_value
            elif operator == '*':
                result *= next_value
            elif operator == '/':
                if next_value == 0:
                    raise ZeroDivisionError("Division by zero.")
                result /= next_value
            i += 2
        return result

    def evaluate_condition(self, condition):
        """Evaluate the condition for if/while statements."""
        condition = condition.replace('AND', 'and').replace('OR', 'or')  # Normalize the keywords
        for var in self.variables:
            condition = condition.replace(var, str(self.variables[var]))
        try:
            return eval(condition)  # Use eval for simple condition evaluation
        except Exception as e:
            raise SyntaxError(f"Error evaluating condition: {condition}. Error: {e}")

    def evaluate_part(self, part):
        """Evaluate a single part of an expression or a variable."""
        part = part.strip()
        if part.isdigit():
            return int(part)
        elif re.match(r'^\d+\.\d+$', part):  # Match floating point
            return float(part)
        elif part in self.variables:
            return self.variables[part]
        elif re.match(r'^\w+\[\d+\]$', part):  # List index access
            list_name, index = part[:-1].split('[')
            index = int(index)
            if list_name in self.lists and 0 <= index < len(self.lists[list_name]):
                return self.lists[list_name][index]
            else:
                raise IndexError(f"Index {index} out of range for list '{list_name}'.")
        else:
            raise NameError(f"Undefined variable or invalid expression: {part}")

    def remove_comments(self, line):
        """Remove comments from the line."""
        comment_start = line.find(">>")
        comment_end = line.find("<<")

        if comment_start != -1 and comment_end != -1 and comment_start < comment_end:
            return line[:comment_start].strip()
        return line.strip()

# Sample program using the MerCCompiler commands
def read_file(filename):
    """Read the contents of a file."""
    with open(filename, 'r') as file:
        return file.read()

if __name__ == "__main__":
    # Prompt for a .merc file
    filename = input("Please enter the path to your .merc file: ").strip()

    # Validate the file extension
    if not filename.endswith('.merc'):
        print("Error: File must end with '.merc'")
        sys.exit(1)

    # Check if the file exists
    if not os.path.isfile(filename):
        print("Error: File does not exist.")
        sys.exit(1)

    # Read the contents of the file
    code = read_file(filename)

    # Create a compiler instance and parse the code
    compiler = MerCCompiler()
    try:
        compiler.parse(code)
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        
    
    print("PROGRAM EXECUTED")
    print("THIS WINDOW WILL BE TERMINATED IN 5 SECONDS")
    time.sleep(5)