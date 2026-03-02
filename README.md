#### Demo:
https://github.com/user-attachments/assets/ed78f498-9732-4af8-aef8-8b806caf87b4

#### This README is written by the AI agent itself, by modifying the `work_dir` parameter to the current directory, and running the agent with a prompt to write this README file.

# AI Agent with Google Gemini Function Calling

This project implements an AI agent that leverages Google Gemini's function calling capabilities to interact with the local file system and execute Python scripts. It serves as a Proof of Concept (PoC) for building intelligent agents capable of performing complex operations by orchestrating tool use.

## Capabilities

The agent can perform the following operations:

*   **List Files and Directories:** Retrieve information about files and directories within the working directory (`get_files_info`).
*   **Read File Contents:** Access and return the content of specified files (`get_file_content`).
*   **Execute Python Scripts:** Run Python files with optional command-line arguments and capture their output (`run_python_file`).
*   **Write Files:** Create new files or overwrite existing ones with provided content (`write_file`).

All file system interactions are relative to the working directory for security and isolation.

## Installation

This project requires Python 3.13 or higher.

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**

    **Option A: Using `uv` (recommended, as `uv.lock` is present)**
    If you have `uv` installed, you can create a virtual environment and install dependencies with a single command:
    ```bash
    uv venv
    source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
    uv sync
    ```

    **Option B: Using `pip`**
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
    pip install google-genai python-dotenv
    ```

## Configuration

Set your Google Gemini API key as an environment variable named `GEMINI_API_KEY`. You can do this by creating a `.env` file in the project root with the following content:

```
GEMINI_API_KEY="YOUR_API_KEY"
```

## Usage

Run the `main.py` script with a user prompt. Optional arguments are available for verbose and debug output.

```bash
python main.py "Your coding-related prompt here." [--verbose] [--debug]
```

**Example:**
```bash
python main.py "List all .py files in the current directory and read their contents." --verbose
```

## Project Structure

*   `main.py`: Orchestrates the agent's execution, handles conversational flow, API calls, and function execution.
*   `prompts.py`: Defines the system prompt guiding the agent's behavior.
*   `call_function.py`: Dispatches model-proposed function calls to actual Python functions.
*   `config.py`: Contains configurable parameters for the agent's operation.
*   `pyproject.toml`: Manages project metadata and dependencies.
