def generate_code_and_tests(task_description: str, llm) -> tuple[str, str]:
    prompt = (
        f"You are a Senior Python engineer.\n\n"
        f"Task: {task_description}\n\n"
        f"Please do the following:\n"
        f"1. Write the solution as a Python function.\n"
        f"2. Then, write basic unit tests using Python's unittest module.\n"
        f"3. Do not include any explanations or comments.\n"
        f"4. Return only valid Python code.\n\n"
        f"Use this format:\n"
        f"[FUNCTION]\n<code>\n[TESTS]\n<test_code>"
    )
    full_response = llm.generate(prompt)
    print("-----------------")
    print(full_response)
    print("-----------------")

    if "[FUNCTION]" not in full_response or "[TESTS]" not in full_response:
        raise ValueError("Response format invalid. Could not find [FUNCTION] or [/TESTS] markers.")

    _, function_part = full_response.split("[FUNCTION]", 1)
    function_code, test_part = function_part.split("[TESTS]", 1)

    return function_code.strip(), test_part.strip()

def revise_code(original_code: str, test_output: str, task_description: str, llm) -> str:
    prompt = (
        "You're a Senior Python engineer. Your last function failed the tests.\n\n"
        f"Task: {task_description}\n\n"
        f"Previous Code:\n{original_code}\n\n"
        f"Test Output / Errors:\n{test_output}\n\n"
        "Revise the function so that it passes all tests. Only output the new function. No tests, no explanations."
    )
    return llm.generate(prompt)
