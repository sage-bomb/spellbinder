import ast
import astor
import re


"""
code_reshaper.py
----------------

A utility module for parsing, refactoring, and reformatting Python source code.

Core features:
- Converts variable, function, class, and argument names into a specified case style (snake_case, camelCase, PascalCase).
- Detects full-line and inline comments for optional reinjection.
- Optionally injects placeholder docstrings into functions ([AUTO] TODO style).
- Adds structural whitespace to visually separate code blocks when indentation decreases (purely cosmetic but improves human readability).
- Provides an extension hook (default_rules_engine) for future rule-based comment injection or static analysis.

Main exposed function:
- reshape_code(code:str) → str
    - Runs the full pipeline: renames identifiers to camelCase, reinjects comments, inserts docstring placeholders, and applies visual whitespace formatting.

Note:
- The AST transformations are intentionally blunt-force and prioritize readability + refactorability over perfection.
- This module is a prototype-grade tool intended for internal use in Spellbinder dev flows.

"""


# --------------------
# Core Functions
# --------------------

def detect_comments(lines):
    inside_string = False
    comments = []
    triple_quote_pattern = re.compile(r'("""|\'\'\')')

    for lineno, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        if triple_quote_pattern.findall(line):
            count = len(triple_quote_pattern.findall(line))
            if count % 2 != 0:
                inside_string = not inside_string

        if inside_string:
            continue

        stripped = line.strip()
        if re.match(r'^\s*#', line):
            comments.append((lineno, stripped, False, False, False))
        elif '#' in line:
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
    total_length = 0
    if hasattr(node, 'body'):
        total_length += len(node.body)
        for child_node in node.body:
            total_length += sum_body_lengths(child_node)
    return total_length

def sum_bodies_in_tree(tree):
    total_length = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.For):
            total_length += sum_body_lengths(node)
    return total_length

def default_rules_engine(tree):
    return []

# --------------------
# Renaming Functions
# --------------------

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
        raise ValueError(f"Unsupported style: {style}.")

    name_mapping = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name_mapping[node.name] = style_map[style](node.name)

        if isinstance(node, ast.Name):
            if isinstance(node.ctx, (ast.Store, ast.Load)):
                if node.id not in name_mapping:
                    name_mapping[node.id] = style_map[style](node.id)

        if isinstance(node, ast.arg):
            node.arg = style_map[style](node.arg)

    def rename_node(node):
        if isinstance(node, ast.Name):
            node.id = name_mapping.get(node.id, node.id)
        if isinstance(node, ast.arg):
            node.arg = name_mapping.get(node.arg, node.arg)

    for node in ast.walk(tree):
        rename_node(node)

    return name_mapping

def rescry_refactor_names(source_code, style='snake', rules_engine=default_rules_engine):
    lines = source_code.splitlines(keepends=True)
    tree = ast.parse(source_code)
    rename_variable_names(tree, style)
    comment_injections = detect_comments([line.rstrip("\n") for line in lines])
    inject_docstring_into_function(tree, docstring_text="[AUTO] TODO: Document this function")
    rebuilt_code = astor.to_source(tree)
    rebuilt_lines = rebuilt_code.splitlines(keepends=True)
    rule_injections = rules_engine(tree)

    all_injections = comment_injections + rule_injections
    all_injections.sort(reverse=True)

    for lineno, comment, inline, _, shift_indent in all_injections:
        idx = lineno - 1
        if idx >= len(rebuilt_lines):
            rebuilt_lines.append(comment + "\n")
            continue
        if inline:
            rebuilt_lines[idx] = rebuilt_lines[idx].rstrip("\n") + f"  {comment}\n"
            continue
        indentation = re.match(r'(\s*)', rebuilt_lines[idx]).group(1)
        rebuilt_lines.insert(idx, indentation + comment + "\n")

    return "".join(rebuilt_lines)

def add_whitespace_on_indent_change(code):
    lines = code.splitlines(keepends=True)
    result_lines = []
    previous_indent_level = None

    for line in lines:
        current_indent_level = len(line) - len(line.lstrip())
        if previous_indent_level is not None and current_indent_level < previous_indent_level:
            result_lines.append('\n')
        result_lines.append(line)
        previous_indent_level = current_indent_level

    return "".join(result_lines)

def reshape_code(code):
    new_code = rescry_refactor_names(code, style="camel")
    new_code = add_whitespace_on_indent_change(new_code)
    return new_code

# --------------------
# CLI Entry
# --------------------

if __name__ == "__main__":
    import sys

    # --- BEGIN RELATIVE PATH HACK ---
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    # --- END RELATIVE PATH HACK ---

    import argparse

    def process_file(input_path, output_path=None, style="camel"):
        with open(input_path, "r", encoding="utf-8") as f:
            original = f.read()
        reshaped = rescry_refactor_names(original, style=style)
        reshaped = add_whitespace_on_indent_change(reshaped)

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(reshaped)
        else:
            print(f"\n--- {input_path} ---\n")
            print(reshaped)

    parser = argparse.ArgumentParser(description="Reshape Python code using code_reshaper.")
    parser.add_argument("--input", required=True, help="Input file or directory")
    parser.add_argument("--output", required=False, help="Output file or directory (if omitted, print result)")
    parser.add_argument("--style", choices=["snake", "camel", "pascal"], default="camel", help="Case style (default: camel)")

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    if os.path.isfile(input_path):
        if output_path and os.path.isdir(output_path):
            out_file = os.path.join(output_path, os.path.basename(input_path))
            process_file(input_path, output_path=out_file, style=args.style)
        else:
            process_file(input_path, output_path=output_path, style=args.style)

    elif os.path.isdir(input_path):
        if output_path and not os.path.exists(output_path):
            os.makedirs(output_path)
        if output_path and not os.path.isdir(output_path):
            print("If input is a directory, output must be a directory.")
            exit(1)

        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".py"):
                    in_file = os.path.join(root, file)
                    if output_path:
                        rel_path = os.path.relpath(in_file, input_path)
                        out_file = os.path.join(output_path, rel_path)
                        os.makedirs(os.path.dirname(out_file), exist_ok=True)
                        process_file(in_file, output_path=out_file, style=args.style)
                    else:
                        process_file(in_file, output_path=None, style=args.style)
    else:
        print(f"Input path not found: {input_path}")
