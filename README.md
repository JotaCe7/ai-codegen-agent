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
- 🐳 **Dockerized Deployment**: The application is containerized with Docker and managed with Docker Compose for easy, multi-service deployment.
- 💻 **Dual-Interface**: Streamlit GUI and CLI (`cli.py`) for flexibility.  
- 🔧 **Verbose Mode**: CLI `--verbose` flag for detailed step-by-step output.  

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
- **Deployment (Docker)**:  The `Dockerfile.backend` and `Dockerfile.frontend` package the services, and `docker-compose.yml` orchestrates the API, GUI, and Ollama services.

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
pip install -r requirements-backend.txt -r requirements-frontend.txt
```

---

## 🔧 Configuration

This project uses separate environment files for local development and for running with Docker Compose.

### For Local Runs (e.g. python cli.py)

Create a file named `.env` in the project root. This file is for your local secrets and machine-specific settings and should be added to `.gitignore.`

```bash
# === LLM Configuration ===
LLM_PROVIDER=ollama
# or 'apenai'
MODEL=codellama:latest
# or 'gpt-4'

# === API Keys / Endpoints ===
OPENAI_API_KEY=sk-...
OLLAMA_HOST=http://localhost:11434

# == Front-End Configuration ==
API_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
```

*Your `config.py` file will automatically read these values.*

### For Docker Compose Runs

When running with Docker, you need two environment files.

1. **`.env` file:** This file is used by Docker Compose for variable substitution (like the models path). It should be in your .gitignore.


    ```bash
    # Contents for your .env file for Docker runs

    # == Ollama Configuration ==
    OLLAMA_MODELS_PATH=C:\Users\YourUsername\.ollama
    ```

2. **`.env.docker` file:** This file provides the application-level configuration to the containers. This file should be committed to your repository.

    ```bash
    # Contents for your .env.docker file for Docker runs

    # === LLM Configuration ===
    LLM_PROVIDER=ollama
    # or 'apenai'
    MODEL=codellama:latest
    # or 'gpt-4'

    # === API Keys ===
    # Secrets like API keys can be managed in your local .env file,
    # which Docker Compose will also read and pass to the container.
    OPENAI_API_KEY=sk-...
    ```

---

## ▶️ How to Run

This project uses Docker Compose to run the FastAPI back end, the Ollama server, and the Streamlit GUI in separate, managed containers.

### First-Time Setup Only (If you are not using existing models):

If you have not configured `OLLAMA_MODELS_PATH` in your `.env` file, you need to pre-download your model once.

1. **Start the servive in the background:**

```bash
docker-compose up --build -d
```

2. **Pre-download your LLM model:** (Replace `codellama:latest` with the model from your `.env.docker` file)

```bash
docker-compose exec ollama ollama pull codellama:latest
```

3. **Stop** the services for **now**.

```bash
docker-compose down
```

### Normal Run

1. Start all services

```bash
docker-compose up
```

*This will start the API, Ollama, and the Streamlit GUI all at once.*

---

## 🚀 How to Use

### Using the Web Interface

1. Navigate to the Streamlit URL provided in your terminal (usually `http://localhost:8501`).

2. Enter your code generation task in the text area (e.g., "Create a function to sort a list of numbers").

3. Click the "Generate Code" button.

4. The agent will process the request and display the final code, tests, and test output on the page.

### Using the Command-Line Interface

You can also run the agent directly from the command line for quick tests.

#### Basic Usage:

Run the agent directly from the CLI:

```bash
python cli.py "Your task description here"
```

#### Verbose mode:

To see the full step-by-step process, including LLM prompts and responses, use the `-v` or `--verbose` flag.

```bash
python cli.py "Your task description here" -v
```



