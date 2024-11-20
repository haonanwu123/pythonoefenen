def check_functions_in_file(file_path):
    """
    This function checks a Python file for function definitions that are not preceded by a comment.

    Args:
    - file_path (str): The path of the file to check.

    Returns:
    - None
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Iterate through the lines of the file starting from the second line (index 0)
        for line_number, line in enumerate(lines):
            line = line.strip()

            # Check if the current line is a function definition
            if line.startswith("def "):
                # Check if there's no comment on the previous line
                if line_number == 0 or not lines[line_number - 1].strip().startswith(
                    "#"
                ):
                    # Extract the function name from the current line
                    func_name = line.split("(", 1)[0][4:]  # Extract the function name
                    print(
                        f"File: {file_path} contains a function "
                        f"[{func_name}()] on line [{line_number + 1}] "
                        "without a preceding comment."
                    )

    except FileNotFoundError:
        print(f'Error reading file: "{file_path}" does not exist.')


def main():
    """
    Main function that reads command-line arguments, processes files, and checks functions for comments.

    Args:
    - None

    Returns:
    - None
    """
    # Get the file paths from user input (comma-separated)
    file_paths = input("Enter your file path(s): ").split(",")  # split with comma

    if not file_paths:
        print("No files provided.")
        return

    # Iterate over the list of file paths
    for file_path in file_paths:
        # Remove leading/trailing spaces from each file path
        file_path = file_path.strip()
        check_functions_in_file(file_path)


if __name__ == "__main__":
    main()
