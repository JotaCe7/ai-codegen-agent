"""
Handles the generation and revision of code and tests by interacting with an LLM.
"""
import re
from agent.llm_interface import LLMInterface
from agent.prompts import INITIAL_GENERATION_PROMPT, REVISION_PROMPT

# Markers to delimkit code and test in the model response
FUNCTION_START = "[FUNCTION]"
FUNCTION_END = "[/FUNCTION]"
TESTS_START = "[TESTS]"
TESTS_END = "[/TESTS]"

def generate_code_and_tests(
    task_description: str, llm: LLMInterface, verbose: bool = False
) -> tuple[str, str]:
    """Generates initial code and tests from a task description.

    Args:
        task_description: The user's request for code generation.
        llm: An initialized LLMInterface object.
        verbose: If True, prints the full LLM response.

    Returns:
        A tuple containing the generated function code and test code.

    Raises:
        ValueError: If the LLM response does not match the expected format.
    """
    prompt_context = {
        "task_description": task_description,
        "function_start": FUNCTION_START,
        "function_end": FUNCTION_END,
        "tests_start": TESTS_START,
        "tests_end": TESTS_END
    }
    prompt = INITIAL_GENERATION_PROMPT.format(**prompt_context)
    full_response = llm.generate(prompt, verbose=verbose)

    return _parse_code_and_tests(full_response)

def revise_code_and_tests(
    original_code: str,
    original_tests: str,
    test_output: str,
    task_description: str,
    llm: LLMInterface,
    verbose: bool = False,
) -> tuple[str, str]:
    """Revises both the code and tests based on failure feedback.

    Args:
        original_code: The previous version of the code that failed.
        original_tests: The test suite that failed.
        test_output: The error message from the test run.
        task_description: The original high-level task.
        llm: An initialized LLMInterface object.
        verbose: If True, prints the full LLM response.

    Returns:
        A tuple containing the revised code and the revised tests.
    """
    prompt_context = {
        "task_description": task_description,
        "original_code": original_code,
        "original_tests": original_tests,
        "test_output": test_output,
        "function_start": FUNCTION_START,
        "function_end": FUNCTION_END,
        "tests_start": TESTS_START,
        "tests_end": TESTS_END
    }
    prompt = REVISION_PROMPT.format(**prompt_context)
    full_response = llm.generate(prompt, verbose=verbose)

    return _parse_code_and_tests(full_response)

def _parse_code_and_tests(response: str) -> tuple[str, str]:
    """A helper function to parse the LLM's response.

    Args:
        response: The full string response from the LLM.

    Returns:
        A tuple containing the extracted function code and test code.

    Raises:
        ValueError: If the response does not contain the required markers.
    """
    markers = [FUNCTION_START, FUNCTION_END, TESTS_START, TESTS_END]
    for marker in markers:
        if marker not in response:
            raise ValueError(f"Response format invalid. Missing marker: {marker}")

    # Escape markers to safely use them in regex
    escaped_markers = [re.escape(m) for m in markers]

    function_match = re.search(rf"{escaped_markers[0]}(.*?){escaped_markers[1]}", response, re.DOTALL)
    tests_match = re.search(rf"{escaped_markers[2]}(.*?){escaped_markers[3]}", response, re.DOTALL)

    if not function_match or not tests_match:
        raise ValueError("Response format invalid. Could not extract code or tests.")

    function_code = function_match.group(1).strip()
    test_code = tests_match.group(1).strip()

    return function_code, test_code
