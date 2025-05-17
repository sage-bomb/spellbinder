import os
import inspect
import importlib.util
import argparse

from spellbinder_llm.prompt_manager import PromptManager

def get_module_name(file_path, root_path):
    rel_path = os.path.relpath(file_path, root_path)
    module_name = rel_path.replace(os.path.sep, ".")
    if module_name.endswith(".py"):
        module_name = module_name[:-3]
    return module_name

def get_code_structure_with_descriptions(root_path, describe=False, use_docstring=False):
    structure = []
    pm = PromptManager() if describe else None

    exclude_dirs = {"venv", ".env", "__pycache__", "site-packages", "build", "dist", ".git"}

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            if not filename.endswith(".py") or filename == "__init__.py":
                continue

            file_path = os.path.join(dirpath, filename)
            module_name = get_module_name(file_path, root_path)

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception:
                continue

            module_entry = {"module": module_name, "classes": [], "functions": []}

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    class_entry = {"class_name": name, "methods": []}

                    for meth_name, meth in inspect.getmembers(obj, predicate=inspect.isfunction):
                        if meth.__module__ == module.__name__:
                            prototype = str(inspect.signature(meth))
                            description = ""

                            if describe:
                                try:
                                    source = inspect.getsource(meth)
                                    description = pm.run_template(
                                        name="Analyst.FunctionSummarizer",
                                        variables={"input": f"Please summarize this function in a single line: \n{source}"},
                                        metadata={"allow_expensive": False}
                                    )
                                except Exception:
                                    description = "[LLM error]"
                            elif use_docstring:
                                description = inspect.getdoc(meth) or ""

                            class_entry["methods"].append(
                                f"{meth_name}{prototype} -- {description}" if (describe or use_docstring) else f"{meth_name}{prototype}"
                            )

                    module_entry["classes"].append(class_entry)

                elif inspect.isfunction(obj) and obj.__module__ == module.__name__:
                    prototype = str(inspect.signature(obj))
                    description = ""

                    if describe:
                        try:
                            source = inspect.getsource(obj)
                            description = pm.run_template(
                                name="Analyst.FunctionSummarizer",
                                variables={"input": f"Please summarize this function in a single line: \n{source}"},
                                metadata={"allow_expensive": False}
                            )
                        except Exception:
                            description = "[LLM error]"
                    elif use_docstring:
                        description = inspect.getdoc(obj) or ""

                    module_entry["functions"].append(
                        f"{name}{prototype} -- {description}" if (describe or use_docstring) else f"{name}{prototype}"
                    )

            structure.append(module_entry)

    return structure

def print_structure_with_descriptions(structure):
    print("\n🗂️  Project Code Structure with Descriptions:\n")
    for module in structure:
        print(f"📄 {module['module']}")

        for cls in module["classes"]:
            print(f"   🏛️  Class: {cls['class_name']}")
            for method in cls["methods"]:
                print(f"      - {method}")

        for func in module["functions"]:
            print(f"   🔧 Function: {func}")

def main():
    parser = argparse.ArgumentParser(description="Analyze Python project structure with optional descriptions.")
    parser.add_argument("path", type=str, help="Path to the Python project root")
    parser.add_argument("--describe", action="store_true", help="Use LLM to describe functions and methods")
    parser.add_argument("--docstring", action="store_true", help="Use native docstrings to describe functions and methods")
    args = parser.parse_args()

    structure = get_code_structure_with_descriptions(
        args.path,
        describe=args.describe,
        use_docstring=args.docstring
    )
    print_structure_with_descriptions(structure)

if __name__ == "__main__":
    main()
