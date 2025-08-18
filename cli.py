import argparse
import sys
from typing import Optional
from agent.llm_interface import LLMInterface
from agent.code_generator import generate_code_and_tests, revise_code_and_tests
from agent.test_runner import run_tests

DEFAULT_MAX_TRIES = 3

def run_task(
    task_description: str,
    agent: Optional[LLMInterface] = None,
    max_tries: int = DEFAULT_MAX_TRIES,
    verbose: bool = False
) -> tuple[str, bool, str, str]:
    """Orchestrates the main AI agent loop for code generation and testing.

    This function manages the iterative process of generating code, running
    tests, and attempting revisions based on test failures.

    Args:
        task_description: The user's request for code generation.
        agent: An initialized LLMInterface object. If None, a new one is created.
        max_tries: The maximum number of attempts to generate and fix the code.
        verbose: If True, prints detailed step-by-step progress.

    Returns:
        A tuple containing the final generated code, a boolean indicating if
        tests passed, the final test suite, and the final test output.
    """
    if agent is None:
        agent = LLMInterface()

    code, tests, test_output = "", "", ""

    for attempt in range(1, max_tries + 1):
        if verbose:
            print(f"\n🔁 Attempt {attempt}/{max_tries}...")

        try:
            if attempt == 1:
                # First attempt: generate code and tests from the initial task.
                code, tests = generate_code_and_tests(task_description, agent, verbose=verbose)
            else:
                # Subsequent attempts: revise both based on the last failure.
                if verbose:
                    print("Tests failed. Attempting revision of code and tests...")
                code, tests = revise_code_and_tests(
                    original_code=code,
                    original_tests=tests,
                    test_output=test_output,
                    task_description=task_description,
                    llm=agent,
                    verbose=verbose
                )
            
            if verbose:
                print("⚙️ Running tests...")
            passed, test_output = run_tests(code, tests)

            if passed:
                # If tests pass, the loop is successful.
                return code, True, tests, test_output
        
        except ValueError as e:
            # Handle cases where the LLM response is not in the expected format.
            print(f"Error processing LLM response: {e}")
            test_output = f"Error during attempt {attempt}: {e}"
            continue
        except Exception as e:
            print(f"An unexpected error occurred during attempt {attempt}: {e}")
            test_output = f"Unexpected error during attempt {attempt}: {e}"
            break

    # If the loop completes without success.
    return code, False, tests, test_output

def print_result(code: str, passed: bool, tests: str, output: str) -> None:
    """Formats and prints the final results of the agent's run."""
    print("\n" + "="*20 + " FINAL RESULT " + "="*20)
    if passed:
        print("✅ All tests passed!\n")
        print("🧠 Final Code:")
    else:
        print("🚨 Max attempts reached. Human review required.")
        print("🧠 Last Generated Code:")

    print(code)
    print("\n" + "-"*15 + " Tests " + "-"*15)
    print(tests)
    print("\n" + "-"*15 + " Test Output " + "-"*15)
    
    if output:
        print(output)
    else:
        print("[No output was captured from the test run]")
    print("="*54)

def main():
    """Parses command-line arguments and starts the AI agent task."""
    parser = argparse.ArgumentParser(
        description="Generate and test Python code with LLM assistance."
    )
    parser.add_argument(
        "task",
        type=str,
        nargs="?",
        help="Code generation task description (optional)."
    )
    parser.add_argument(
        "--max-tries",
        type=int,
        default=DEFAULT_MAX_TRIES,
        help=f"Number of retry attempts (default: {DEFAULT_MAX_TRIES})."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output to see step-by-step progress."
    )
    args = parser.parse_args()

    if args.task:
        task_description = args.task
    else:
        task_description = input("💬 Enter your code generation task:\n> ")

    try:
        code, passed, tests, output = run_task(
            task_description, max_tries=args.max_tries, verbose=args.verbose
        )
        print_result(code, passed, tests, output)
    except Exception as e:
        print(f"\n🚨 A critical error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
