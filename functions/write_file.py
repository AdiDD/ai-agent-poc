import os

from google.genai import types


def write_file(working_dir, file_path, content):
    working_path = os.path.abspath(working_dir)
    target_path = os.path.normpath(os.path.join(working_path, file_path))
    is_valid_path = os.path.commonpath([working_path, target_path]) == working_path

    if not is_valid_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    tail, head = os.path.split(target_path)
    # head should be empty when path ends with "/"
    if not head:
        return f'Error: Cannot write to "{file_path}" as it is not pointing to a file'

    try:
        os.makedirs(tail, exist_ok=True)
        print(f"writing to {target_path}")
        with open(target_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: Cannot write to "{file_path}": {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Write to a file at a specific path relative to the working directory. "
        "If some directories specified in the relative path are missing, they will be automatically created. "
        "Rejects paths that escape the working directory or point to a directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_dir": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Absolute or relative base directory that defines the permitted sandbox. "
                    "The target file must resolve within this directory."
                ),
                min_length=1,
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to write, relative to working_dir (e.g. 'outputs/result.txt'). "
                    "Must not escape working_dir (e.g. via '..'). Must point to a file (not end with '/')."
                ),
                min_length=1,
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Full text content to write to the file. This overwrites any existing file.",
            ),
        },
        required=["working_dir", "file_path", "content"],
    ),
)
