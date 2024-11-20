import sys
import os


def display_head(file_name):
    """
    Display the first 10 lines of the specified file.
    If the file has fewer than 10 lines, display all the lines.

    Parameters:
    file_name (str): The name of the file to read.

    Returns:
    None
    """
    try:
        # Check if the file exists
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f'Error reading file: "{file_name}"')

        # Open and read the file
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Display the first 10 lines
        print("".join(lines[:10]), end="")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    """
    Main function to handle command-line arguments and call display_head.
    """
    if len(sys.argv) != 2:  # Ensure exactly one argument is provided
        print("Usage: python3 head.py <filename>")
        sys.exit(1)

    file_name = sys.argv[1]
    display_head(file_name)


if __name__ == "__main__":
    main()
