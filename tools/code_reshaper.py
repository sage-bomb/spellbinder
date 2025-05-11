import ast
import astor

def detect_comments(lines):
    inside_string = False
    comments = []
    triple_quote_pattern = re.compile(r'("""|\'\'\')')

    for lineno, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        # toggle inside_string state on triple quotes
        if triple_quote_pattern.findall(line):
            count = len(triple_quote_pattern.findall(line))
            if count % 2 != 0:
                inside_string = not inside_string

        if inside_string:
            continue

        stripped = line.strip()
        if re.match(r'^\s*#', line):
            # full-line comment
            comments.append((lineno, stripped, False, False, False))
        elif '#' in line:
            # inline comment
            code, comment = line.split('#', 1)
            comments.append((lineno, '#' + comment.strip(), True, False, False))

    return comments


def inject_docstring_into_function(tree, docstring_text):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring_node = ast.Expr(value=ast.Constant(value=docstring_text))
            node.body.insert(0, docstring_node)
            break

def trees_equal_ignore_docstrings(tree1, tree2):
    def clean_tree(tree):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    node.body = node.body[1:]
        return tree
    return ast.dump(clean_tree(tree1)) == ast.dump(clean_tree(tree2))

def sum_body_lengths(node):
    """Recursively sum all body lengths under a parent node."""
    total_length = 0
    
    # If the node has a body, sum its length
    if hasattr(node, 'body'):
        total_length += len(node.body)  # Add the length of the current body's list
        
        # For each child node in the body, recursively sum their body lengths
        for child_node in node.body:
            total_length += sum_body_lengths(child_node)
    
    return total_length

def sum_bodies_in_tree(tree):
    """Sum the lengths of body lists for each parent node in the AST."""
    total_length = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.For):
            total_length += sum_body_lengths(node)
    return total_length
def default_rules_engine(tree):
    """
    Placeholder for the rules engine.
    
    Returns:
        list: A list of comment injections where each injection is a tuple.
              Example: [(lineno, comment, inline, rule_based, shift_indent)]
    """
    return []

import ast
import astor

import re

# Renaming Functions
def convert_to_snake_case(name):
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def convert_to_camel_case(name):
    components = name.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

def convert_to_pascal_case(name):
    components = name.split('_')
    return ''.join(x.title() for x in components)

def rename_variable_names(tree, style='snake'):
    style_map = {
        'snake': convert_to_snake_case,
        'camel': convert_to_camel_case,
        'pascal': convert_to_pascal_case
    }

    if style not in style_map:
        raise ValueError(f"Unsupported style: {style}. Choose from 'snake', 'camel', or 'pascal'.")

    name_mapping = {}

    # Walk the AST and rename variables
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            name_mapping[node.name] = style_map[style](node.name)
        
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, (ast.Store, ast.Load)):
                if node.id not in name_mapping:
                    name_mapping[node.id] = style_map[style](node.id)
        
        if isinstance(node, ast.arg):
            node.arg = style_map[style](node.arg)

    # Now rename variables and functions
    def rename_node(node):
        if isinstance(node, ast.Name):
            node.id = name_mapping.get(node.id, node.id)

        if isinstance(node, ast.arg):
            node.arg = name_mapping.get(node.arg, node.arg)

    # Apply renaming to every node in the tree
    for node in ast.walk(tree):
        rename_node(node)

    return name_mapping  # We return the name mapping for reference
def rescry_refactor_names(source_code, style='snake', rules_engine=default_rules_engine):
    lines = source_code.splitlines(keepends=True)

    # Parse the source code into AST
    tree = ast.parse(source_code)

    # Rename variables based on the desired style
    name_mapping = rename_variable_names(tree, style)
    
    # Extract comments using the modified detect_comments (same as before)
    comment_injections = detect_comments([line.rstrip("\n") for line in lines])
    
    # Inject docstrings into functions
    inject_docstring_into_function(tree, docstring_text="[AUTO] TODO: Document this function")

    # Rebuild the code after renaming
    rebuilt_code = astor.to_source(tree)
    rebuilt_lines = rebuilt_code.splitlines(keepends=True)

    # Add rule-based injections from the rules engine
    rule_injections = rules_engine(tree)

    # Merge all injections (comment + rule-based)
    all_injections = comment_injections + rule_injections
    all_injections.sort(reverse=True)  # Ensure rule-based and normal comments are ordered

    for lineno, comment, inline, rule_based, shift_indent in all_injections:
        idx = lineno - 1
        if idx >= len(rebuilt_lines):
            rebuilt_lines.append(comment + "\n")  # Ensure trailing comments are appended
            continue

        if inline:
            rebuilt_lines[idx] = rebuilt_lines[idx].rstrip("\n") + f"  {comment}\n"
            continue

        # Adjust indentation based on the shift_indent flag
        if shift_indent:
            # Shift the indentation one level deeper for nested blocks (loops, etc.)
            parent_idx = idx - 1
            while parent_idx >= 0:
                # Skip over empty lines or comments
                if rebuilt_lines[parent_idx].strip():
                    indentation = re.match(r'(\s*)', rebuilt_lines[parent_idx]).group(1)
                    indentation = '    ' + indentation  # Shift by one more tab
                    break
                parent_idx -= 1
        else:
            # For non-nested comments, we just take the next line's indentation
            indentation = re.match(r'(\s*)', rebuilt_lines[idx]).group(1)

        rebuilt_lines.insert(idx, indentation + comment + "\n")

    return "".join(rebuilt_lines)


def add_whitespace_on_indent_change(code):
    lines = code.splitlines(keepends=True)  # Split the code into lines
    result_lines = []

    # Track the previous line's indentation level
    previous_indent_level = None

    for line in lines:
        # Get the current line's indentation
        current_indent_level = len(line) - len(line.lstrip())

        # If the current line has less indentation than the previous one, add a blank line
        if previous_indent_level is not None and current_indent_level < previous_indent_level:
            result_lines.append('\n')  # Add a blank line

        # Add the current line to the result
        result_lines.append(line)

        # Update the previous indent level
        previous_indent_level = current_indent_level

    return "".join(result_lines)

def reshape_code(code):
    new_code = rescry_refactor_names(code,style="camel")
    new_code = add_whitespace_on_indent_change(new_code)
    return new_code