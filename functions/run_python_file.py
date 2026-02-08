import os
import subprocess

from google.genai import types


def run_python_file(working_dir, file_path, args=None):
    working_path = os.path.abspath(working_dir)
    target_path = os.path.normpath(os.path.join(working_path, file_path))
    is_valid_path = os.path.commonpath([working_path, target_path]) == working_path

    if not is_valid_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if os.path.splitext(target_path)[1] != ".py":
        return f'Error: "{file_path}" is not a Python file'

    # Prepare the subprocess to run the file
    command = ["python", target_path]
    if args:
        command.extend(args)

    try:
        cp = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_str = ""
        if cp.returncode != 0:
            output_str += f"Process exited with code {cp.returncode}.\n"
        if not cp.stdout and not cp.stderr:
            output_str += f"No output produced.\n"
        else:
            if cp.stdout:
                output_str += f"STDOUT: {cp.stdout}\n"
            if cp.stderr:
                output_str += f"STDERR: {cp.stderr}\n"
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return output_str


if __name__ == "__main__":
    run_python_file("calculator", "main.py")


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Execute a Python (.py) file located within the permitted working directory and return its output. "
        "The file_path must resolve inside working_dir and must point to an existing regular .py file. "
        "Optional args are passed as command-line arguments to the script."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_dir": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Absolute or relative base directory that defines the permitted sandbox. "
                    "The script must resolve within this directory."
                ),
                min_length=1,
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the Python script to execute, relative to working_dir "
                    "(e.g. 'scripts/run_me.py'). Must not escape working_dir and must end with '.py'."
                ),
                min_length=1,
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of command-line arguments to pass to the script. "
                    "Each list item becomes one argument token."
                ),
                items=types.Schema(
                    type=types.Type.STRING,
                    description="One command-line argument token (e.g. '--flag' or 'value').",
                ),
            ),
        },
        required=["working_dir", "file_path"],
    ),
)
