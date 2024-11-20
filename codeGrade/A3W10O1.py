import os
import sys


def add_line_numbers(input_file_name: str, output_file_name: str) -> None:
    """Add line numbers to a file."""
    # Ensure the input file path is resolved relative to the script's location
    input_path = os.path.join(sys.path[0], input_file_name)
    output_path = os.path.join(sys.path[0], output_file_name)

    try:
        # Open input and output files
        with open(input_path, "r", encoding="utf-8") as input_file, open(
            output_path, "w", encoding="utf-8"
        ) as output_file:
            for line_number, line in enumerate(input_file, start=1):
                output_file.write(f"{line_number}: {line}")
        print(f"File '{output_file_name}' created successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file_name}' does not exist.")
    except IOError as e:
        print(f"Error: Unable to read/write files due to {e}")


def main():
    input_file_name = input("Enter the name of the input file: ").strip()
    output_file_name = input("Enter the name of the output file: ").strip()
    add_line_numbers(input_file_name, output_file_name)


if __name__ == "__main__":
    main()
