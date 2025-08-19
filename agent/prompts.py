# A central place for all LLM prompt templates.

INITIAL_GENERATION_PROMPT = """
You are a Senior Python engineer assigned to a test-driven development task.

Task: {task_description}

Please do the following:
1. Write a Python function that attempts to solve the task.
2. Write a comprehensive set of unit tests using Python's unittest module.
3. Do not include any explanations, comments, or `if __name__ == '__main__':` blocks.
4. Return only valid, runnable Python code in the specified format.
5. Use this exact format:
{function_start}
<code>
{function_end}
{tests_start}
<test_code>
{tests_end}
""" # + "6. **CRITICAL INSTRUCTION**: You MUST include at least one test case that is designed to FAIL. For example: `self.assertEqual(add(2, 2), 5)`. This is required to test the code revision process.\n""

REVISION_PROMPT = """
You're a Senior Python engineer. A previous attempt to solve a task failed.

Original Task: {task_description}

Previous Code:
{original_code}

Previous Tests:
{original_tests}

Test Output / Errors:
{test_output}

Please analyze the failure. Revise both the function and the tests so that all tests pass. The issue might be in the code, the tests, or both.

Use this exact format:
{function_start}
<code>
{function_end}
{tests_start}
<test_code>
{tests_end}
"""