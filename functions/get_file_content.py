import os

from google.genai import types
from config import READ_FILE_CHAR_LIMIT


def get_file_content(working_dir, file_path):
    working_path = os.path.abspath(working_dir)
    target_path = os.path.normpath(os.path.join(working_path, file_path))
    valid_target_path = os.path.commonpath([working_path, target_path]) == working_path

    if not valid_target_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path) as f:
            content = f.read(READ_FILE_CHAR_LIMIT)
            # If there are more characters available after reading max limit
            # append an explanation on the content
            if f.read(1):
                content += f'[... File "{file_path}" truncated at {READ_FILE_CHAR_LIMIT} characters]'
    except Exception as e:
        return f'Error: could not read "{file_path}": {e}'

    return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Read and return the content of a file located within the permitted working directory. "
        "The file_path must resolve inside working_dir and must point to an existing regular file. "
        "Content may be truncated to a maximum character limit."
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
                    "Path to the file to read, relative to working_dir (e.g. 'data/input.txt'). "
                    "Must not escape working_dir (e.g. via '..'). Must point to a regular file."
                ),
                min_length=1,
            ),
        },
        required=["working_dir", "file_path"],
    ),
)
