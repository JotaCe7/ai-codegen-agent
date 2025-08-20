# AI Code Generation Agent

A **test-driven AI agent** that autonomously generates, validates, and revises Python code.  
This project uses a **FastAPI** back end for the core logic and a **Streamlit** front end for user interaction, demonstrating a modern, full-stack approach to building AI-powered applications.

---

## 🚀 The Problem Solved
Writing boilerplate code and unit tests can be time-consuming.  
This project automates the initial draft of both code and tests by leveraging a **Large Language Model (LLM)** within a **robust TDD loop**.  

The agent:
1. Receives a natural language task.  
2. Generates both Python code and tests.  
3. Iterates in a revision loop until the code passes all tests or maximum tries are reached.  

---

## ✨ Features
- 🤖 **Autonomous Code Generation**: Generates Python functions, classes, and unit tests from a single natural language prompt.  
- 🧪 **Test-Driven Validation**: Automatically runs the generated tests in a secure, isolated environment to validate the code's correctness.
- 🧠 **Intelligent Retry Loop**: Analyzes errors (bugs vs. test issues) and revises automatically.  
- 🌐 **Web API & GUI**: FastAPI back end + Streamlit GUI for easy interaction.  
- 🐳 **Dockerized Deployment**: The back-end application is containerized with Docker for easy, consistent deployment.
- 💻 **Dual-Interface**: Streamlit GUI and CLI (`cli.py`) for flexibility.  
- 🔧 **Verbose Mode**: CLI `--verbose` flag for detailed step-by-step output.  

---

## 🛠️ Technology Stack

- **AI Core:** LangChain, OpenAI / Ollama
- **Back End:** FastAPI, Uvicorn
- **Front End:** Streamlit
- **Testing:** Python Unittest
- **Deployment:** Docker

---

## 🛠️ Project Architecture and Technology Stack
The project follows a **clean, decoupled architecture**:

- **AI Core (LangChain, OpenAI / Ollama)**: The `agent/` package contains all core logic.
  - `llm_interface.py`: Manages LLM interactions (LangChain-based).  
  - `prompts.py`: Centralized prompt templates.  
  - `code_generator.py`: Handles code and test generation/revisions.
  - `test_runner.py`: Runs generated tests safely in an isolated subprocess. 
- **Back End (FastAPI)**: `main.py` serves the core AI logic via a REST API.  
- **Front End (Streamlit)**: `app.py` provides an interactive UI that talks to the FastAPI back end.
- **Deployment (Docker)**: The `Dockerfile` packages the back end into a portable container for easy deployment.

---

## ⚙️ Setup and Installation

Follow these steps to set up and run the project locally.

1. **Clone the Repository**

```bash
git clone https://github.com/JotaCe7/ai-codegen-agent.git
cd ai-codegen-agent
```

2. **Create and Activate a Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

Before running the agent, configure your LLM provider in config.py:

1. Open the `config.py` file.
2. Set `LLM_PROVIDER` to `"openai"` or `"ollama"`.
3. Set `MODEL` to your desired model (e.g., `"gpt-4"`, `"codellama:latest"`).
4. If using OpenAI, make sure to set your `OPENAI_API_KEY`.

---

## ▶️ How to Run

There are two ways to run this project: using Docker (recommended for a stable deployment) or running the services manually

### Option 1: Running with Docker (Recommended)

This method runs the FastAPI back end inside a Docker container.

1. Build the Docker Image

*(Note the . at the end of the command)*

```bash
docker build -t ai-codegen-agent .
```

2. Run the Docker Container

```bash
docker run -p 8000:8000 --name my-ai-codegen-agent ai-codegen-agent
```

The API will now be running and accessible at `http://127.0.0.1:8000`.

3. Start the Front-End GUI

In a separate terminal, start the Streamlit front end.

```bash
streamlit run app.py
```

### Option 2: Running Manually 

1. Start the Back-End API

This requires running the back-end API and the front-end GUI in two separate terminals.

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

2. Start the Front-End GUI

```bash
streamlit run app.py
```

---

## 🚀 How to Use

### Using the Web Interface

1. Navigate to the Streamlit URL provided in your terminal.

2. Enter your code generation task in the text area (e.g., "Create a function to sort a list of numbers").

3. Click the "Generate Code" button.

4. The agent will process the request and display the final code, tests, and test output on the page.

### Using the Command-Line Interface

You can also run the agent directly from the command line for quick tests.

**Basic Usage:**

Run the agent directly from the CLI:

```bash
python cli.py "Your task description here"
```

**Verbose mode:**

To see the full step-by-step process, including LLM prompts and responses, use the `-v` or `--verbose` flag.

```bash
python cli.py "Your task description here" -v
```



