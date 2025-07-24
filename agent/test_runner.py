import tempfile
import subprocess
import os


import tempfile
import subprocess
import os
import sys
import uuid

import tempfile
import subprocess
import os
import sys
import uuid



import tempfile
import subprocess
import os
import uuid

def run_tests(code: str, tests: str) -> tuple[bool, str]:
    temp_dir = tempfile.gettempdir()
    unique_id = uuid.uuid4().hex

    code_path = os.path.join(temp_dir, f"{unique_id}_code.py")
    test_path = os.path.join(temp_dir, f"{unique_id}_test.py")

    with open(code_path, "w") as f:
        f.write(code + "\n")

    test_script = f'''
import importlib.util
import unittest

spec = importlib.util.spec_from_file_location("generated_code", r"{code_path}")
generated_code = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generated_code)
globals().update(vars(generated_code))

{tests}
'''

    with open(test_path, "w") as f:
        f.write(test_script)

    try:
        result = subprocess.run(
            ["python", test_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        output = result.stdout.decode()
        passed = result.returncode == 0
        return passed, output
    except Exception as e:
        return False, str(e)


def run_tests4(code: str, tests: str) -> tuple[bool, str]:
    temp_dir = tempfile.gettempdir()
    unique_id = f"m_{uuid.uuid4().hex}"  # <-- prefix with 'm_'

    code_filename = f"{unique_id}_code.py"
    test_filename = f"{unique_id}_test.py"
    code_path = os.path.join(temp_dir, code_filename)
    test_path = os.path.join(temp_dir, test_filename)

    # Write the code file
    with open(code_path, "w") as f:
        f.write(code + "\n")

    # Write the test file with proper import
    module_name = code_filename.replace(".py", "")
    with open(test_path, "w") as f:
        f.write("import sys\n")
        f.write(f"sys.path.insert(0, r'{temp_dir}')\n")
        f.write(f"from {module_name} import *\n\n")
        f.write(tests + "\n")

    try:
        result = subprocess.run(
            ["python", test_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        output = result.stdout.decode()
        passed = result.returncode == 0
        return passed, output
    except Exception as e:
        return False, str(e)

def run_tests3(code: str, tests: str) -> tuple[bool, str]:
    temp_dir = tempfile.gettempdir()
    unique_id = uuid.uuid4().hex

    code_filename = f"{unique_id}_code.py"
    test_filename = f"{unique_id}_test.py"
    code_path = os.path.join(temp_dir, code_filename)
    test_path = os.path.join(temp_dir, test_filename)

    # Write the code file
    with open(code_path, "w") as f:
        f.write(code + "\n")

    # Write the test file with proper import
    module_name = code_filename.replace(".py", "")
    with open(test_path, "w") as f:
        f.write("import sys\n")
        f.write(f"sys.path.insert(0, r'{temp_dir}')\n")
        f.write(f"from {module_name} import *\n\n")
        f.write(tests + "\n")

    try:
        result = subprocess.run(
            ["python", test_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        output = result.stdout.decode()
        passed = result.returncode == 0
        return passed, output
    except Exception as e:
        return False, str(e)



def run_tests2(code: str, tests: str) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile(suffix="_code.py", mode="w", delete=False) as code_file:
        code_file.write(code + "\n")
        code_path = code_file.name

    # Generate a test script that dynamically imports the code file
    test_script = f'''
import importlib.util
import sys
import unittest

# Dynamically load the generated code module
spec = importlib.util.spec_from_file_location("generated_code", r"{code_path}")
generated_code = importlib.util.module_from_spec(spec)
sys.modules["generated_code"] = generated_code
spec.loader.exec_module(generated_code)

{tests}
'''

    with tempfile.NamedTemporaryFile(suffix="_test.py", mode="w", delete=False) as test_file:
        test_file.write(test_script)
        test_path = test_file.name

    try:
        result = subprocess.run(
            ["python", test_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        output = result.stdout.decode()
        passed = result.returncode == 0
        return passed, output
    except Exception as e:
        return False, str(e)


def run_tests_old(code: str, tests: str) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile(suffix="_code.py", mode="w", delete=False) as code_file:
        code_file.write(code + "\n")
        code_path = code_file.name

    with tempfile.NamedTemporaryFile(suffix="_test.py", mode="w", delete=False) as test_file:
        test_file.write(f"import unittest\n")
        test_file.write(f"from {code_path.replace('.py', '').split('/')[-1]} import *\n")
        test_file.write(tests + "\n")
        test_path = test_file.name

    try:
        result = subprocess.run(
            ["python", test_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        output = result.stdout.decode()
        passed = result.returncode == 0
        return passed, output
    except Exception as e:
        return False, str(e)
