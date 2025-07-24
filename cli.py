from agent.llm_interface import LLMInterface
from agent.code_generator import generate_code_and_tests, revise_code
from agent.test_runner import run_tests

MAX_TRIES = 3

def run_task(task_description: str, agent=None) -> tuple[str , bool, str]:

    if agent is None:
        agent = LLMInterface()

    code, tests, test_output = "", "", ""

    for attempt in range(1, MAX_TRIES + 1):
        print(f"\n🔁 Attempt {attempt}/{MAX_TRIES}...")

        if attempt == 1:
            code, tests = generate_code_and_tests(task_description, agent)
        else:
            code = revise_code(code, test_output, task_description, agent)

        print("⚙️ Running tests...")
        passed, test_output = run_tests(code, tests)

        if passed:
            return code, True, test_output

    return code, False, test_output

def main():
    task_description = input("💬 Enter your code generation task:\n> ")
    code, passed, output = run_task(task_description)

    if passed:
        print("✅ All tests passed!\n")
        print("🧠 Final Code:\n")
    else:
        print("🚨 Max attempts reached. Human review required.")
        print("🧠 Last Generated Code:\n")
    
    print(code)
    print("\n🧪 Final Test Output:\n")
    print(output)

if __name__ == "__main__":
    main()
