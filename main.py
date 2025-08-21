from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from cli import run_task

app = FastAPI(
    title="AI Code Generation Agent",
    description=("An API for a test-driven AI agent that generates "
                 "and validates Python code."),
    version="1.0.0",
)

# Add CORS Middleware

origins = [
    "http://localhost:8501", # Streamlit's default port
    "http://127.0.0.1:8501",
    "null", # For local file:// access when opening index.html directly
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods, including POST and OPTIONS
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    """The request model for the code generation task."""

    task_description: str
    max_tries: int = 3
    verbose: bool = False

class TaskResponse(BaseModel):
    """The response model for the code generation task"""

    passed: bool
    code: str
    tests: str
    output: str

@app.post("/generate-code", response_model=TaskResponse)
def generate_code_endpoint(request: TaskRequest):
    """
    Receives a code generation task, runs the AI agent, and return the result.
    """
    print(f"received task: {request.task_description}")

    code, passed, tests, output = run_task(
        task_description=request.task_description,
        max_tries=request.max_tries,
        verbose=request.verbose
    )

    return {
        "passed": passed,
        "code": code,
        "tests": tests,
        "output": output
    }

@app.get("/")
def read_root():
    """A simple endpoint to confirm the server is running."""
    return {
        "message": (
            "AI Code Generation Agent is running. "
            "Send a POST request to /generate-code."
        )
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)