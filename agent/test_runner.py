import tempfile
import subprocess
import os
import sys
import uuid
import ast

def discover_symbols(source_code: str) -> list[str]:
    """Parse Python source code to find top-level importable names.

    This function uses Python's Abstract Syntax Tree (AST) module to safely
    parse a string of source code. It walks the top level of the parsed tree
    to find all classes, functions (sync and async), and global variable
    assignments.

    Args:
        source_code: A string containing the Python source code to analyze.

    Returns:
        A list of strings, where each string is a discovered name that can be
        imported.
    """
    names = []
    try:
        tree = ast.parse(source_code)
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                names.append(node.name)
            elif isinstance(node, ast.Assign):
                # For assignments, find the names of the variables being assigned.
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names.append(target.id)
    except SyntaxError as e:
        print(f"AST parsing error: {e}")
    return names

def run_tests(code_to_test: str, test_script_content: str) -> tuple[bool, str]:
    """Run unit tests in an isolated subprocess using temporary files.

    This function provides a secure and reliable way to execute tests. It
    creates two temporary files: one for the code to be tested and one for
    the test script. It analyzes the code to find all importable objects,
    dynamically creates an explicit import statement, and injects it into the
    test script. The test script is then executed in a separate Python process
    with a modified environment to ensure the import is successful.

    Args:
        code_to_test: A string of Python code containing functions/classes.
        test_script_content: A string of Python unittest code.

    Returns:
        A tuple containing:
        - A boolean indicating if all tests passed (True) or not (False).
        - A string containing the captured stdout and stderr from the test run.
    """
    temp_dir = tempfile.gettempdir()
    unique_id = uuid.uuid4().hex
    code_module_name = f"module_{unique_id}"
    code_path = os.path.join(temp_dir, f"{code_module_name}.py")
    test_path = os.path.join(temp_dir, f"test_{unique_id}.py")

    # Create a modified environment for the subprocess. This ensures the
    # subprocess can find the temporary module.
    env = os.environ.copy()
    env["PYTHONPATH"] = temp_dir + os.pathsep + env.get("PYTHONPATH", "")

    try:
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code_to_test)

        # Use AST to discover all importable names from the code.
        importable_names = discover_symbols(code_to_test)
        if not importable_names:
            return False, "Execution Error: No importable symbols found in code."

        # Dynamically build the explicit import line.
        import_statement = ", ".join(importable_names)
        import_line = f"from {code_module_name} import {import_statement}\n"
        
        # Add the main execution block to run unittest.
        main_block = "\n\nif __name__ == '__main__':\n    unittest.main()"
        final_test_script = import_line + test_script_content + main_block
        
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(final_test_script)

        # Execute the test script in the isolated environment.
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=10,
            env=env
        )

        passed = result.returncode == 0
        captured_output = result.stdout + result.stderr
        
        return passed, captured_output.strip()

    except Exception as e:
        return False, f"An unexpected error occurred: {e}"
    finally:
        # Ensure temporary files are always cleaned up.
        if os.path.exists(code_path):
            os.remove(code_path)
        if os.path.exists(test_path):
            os.remove(test_path)

if __name__ == "__main__":
    print("--- Running Example Test Case with AST-based Imports ---")
    
    # Example code with a class, function, and global constant.
    example_code = """
MY_CONSTANT = 10

class Calculator:
    def multiply(self, a, b):
        return a * b

def add(a, b):
    return a + b
"""
    
    # Example test script that uses all the symbols from the code.
    example_tests = """
import unittest

class MyExampleTest(unittest.TestCase):
    def test_add_success(self):
        self.assertEqual(add(10, 5), 15)
    
    def test_constant(self):
        self.assertEqual(MY_CONSTANT, 10)

    def test_class_method_failure(self):
        calc = Calculator()
        # This test is designed to fail to show error capture.
        self.assertEqual(calc.multiply(3, 3), 10)
"""

    # Call the final, robust run_tests function.
    passed, output = run_tests(example_code, example_tests)
    
    print("\n--- Results ---")
    print(f"Tests Passed: {passed}")
    print(f"Captured Output:\n---------------------\n{output}")
    print("---------------------\n")
