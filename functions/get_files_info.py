import os

from google.genai import types


def get_files_info(working_dir, directory="."):
    working_path = os.path.abspath(working_dir)
    target_path = os.path.normpath(os.path.join(working_path, directory))
    valid_target_dir = os.path.commonpath([working_path, target_path]) == working_path

    if not valid_target_dir:
        return (
            f'Error: Cannot list "{directory}" as is outside the permitted working directory'
        )

    if not os.path.isdir(target_path):
        return f"Error: {directory} is not a directory"

    try:
        dir_list = os.listdir(target_path)
    except Exception as e:
        return f"Could not see contents of {directory}, {e}"

    dir_contents = {}
    for item in dir_list:
        item_path = os.path.normpath(os.path.join(target_path, item))
        try:
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            dir_contents[item_path] = {
                "name": item,
                "file_size": size,
                "is_dir": is_dir,
            }
        except FileNotFoundError:
            # If a file was moved or deleted while iterating, skip it
            continue
        except PermissionError:
            # Skip files we don't have permission to access
            continue
        except Exception:
            continue

    dir_info = []
    for item in dir_contents.values():
        dir_info.append(
            f"- {item['name']}: file_size={item['file_size']} bytes, is_dir={item['is_dir']}"
        )
    result = "\n".join(dir_info)
    print(result)
    return result


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
