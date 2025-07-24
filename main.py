from agent.llm_interface import LLMInterface
from agent.code_generator import generate_code_and_tests, revise_code
from agent.test_runner import run_tests

MAX_TRIES = 3

def main():
    task_description = input("💬 Enter your code generation task:\n> ")

    agent = LLMInterface()
    
    for attempt in range(1, MAX_TRIES + 1):
        print(f"\n🔁 Attempt {attempt}/{MAX_TRIES}...")

        if attempt == 1:
            code, tests = generate_code_and_tests(task_description, agent)
        else:
            code = revise_code(code, test_output, task_description, agent)

        print("⚙️ Running tests...")
        passed, test_output = run_tests(code, tests)

        if passed:
            print("✅ All tests passed!\n")
            print("🧠 Final Code:\n")
            print(code)
            return

        print("❌ Tests failed:\n")
        print(test_output)

    print("\n🚨 Max attempts reached. Human review required.")
    print("🧠 Last Generated Code:\n")
    print(code)

if __name__ == "__main__":
    main()
