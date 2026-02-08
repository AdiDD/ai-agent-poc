from functions.run_python_file import run_python_file


def main():
    # Should print usage instructions
    print(run_python_file("calculator", "main.py"))
    # Should print calculator result
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    # Should run all the calculator tests
    print(run_python_file("calculator", "tests.py"))
    # Should return an error
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
    print(run_python_file("calculator", "lorem.txt"))
   

if __name__ == '__main__':
    print('Running tests for executing python files')
    main()

