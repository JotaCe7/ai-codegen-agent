"""
Handles the generation and revision of code and tests by interacting with an LLM.
"""
import re
from agent.llm_interface import LLMInterface

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
    prompt = (
        "You are a Senior Python engineer assigned to a test-driven "
        "development task.\n\n"
        f"Task: {task_description}\n\n"
        "Please do the following:\n"
        "1. Write a Python function that attempts to solve the task.\n"
        "2. Write a comprehensive set of unit tests using Python's unittest "
        "module.\n"
        "3. Do not include any explanations, comments, or "
        "`if __name__ == '__main__':` blocks.\n"
        "4. Return only valid, runnable Python code in the specified format.\n\n"
        "Use this exact format:\n"
        "[FUNCTION]\n<code>\n[/FUNCTION]\n[TESTS]\n<test_code>\n[/TESTS]"
    )
    full_response = llm.generate(prompt, verbose=verbose)
    if verbose:
        print("--- LLM Response ---\n"
              f"{full_response}\n"
              "--------------------")

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
    prompt = (
        "You're a Senior Python engineer. A previous attempt to solve a task "
        "failed.\n\n"
        f"Original Task: {task_description}\n\n"
        f"Previous Code:\n{original_code}\n\n"
        f"Previous Tests:\n{original_tests}\n\n"
        f"Test Output / Errors:\n{test_output}\n\n"
        "Please analyze the failure. Revise both the function and the tests "
        "so that all tests pass. The issue might be in the code, the tests, "
        "or both.\n\n"
        "Use this exact format:\n"
        "[FUNCTION]\n<code>\n[/FUNCTION]\n[TESTS]\n<test_code>\n[/TESTS]"
    )
    full_response = llm.generate(prompt, verbose=verbose)
    if verbose:
        print("--- LLM Response ---\n"
              f"{full_response}\n"
              "--------------------")

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
    markers = ["[FUNCTION]", "[/FUNCTION]", "[TESTS]", "[/TESTS]"]
    for marker in markers:
        if marker not in response:
            raise ValueError(f"Response format invalid. Missing marker: {marker}")

    # Use re.DOTALL to make '.' match newlines as well.
    function_match = re.search(r"\[FUNCTION\](.*?)\[/FUNCTION\]", response, re.DOTALL)
    tests_match = re.search(r"\[TESTS\](.*?)\[/TESTS\]", response, re.DOTALL)

    if not function_match or not tests_match:
        raise ValueError("Response format invalid. Could not extract code or tests.")

    function_code = function_match.group(1).strip()
    test_code = tests_match.group(1).strip()

    return function_code, test_code
