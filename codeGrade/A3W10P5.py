def remove_comments(input_file, output_file):
    """
    This function reads the input Python file, removes comments (starting with #),
    and saves the cleaned content to the output file.
    """
    try:
        # Open the input file in read mode
        with open(input_file, "r") as infile:
            lines = infile.readlines()

        # Open the output file in write mode
        with open(output_file, "w") as outfile:
            for line in lines:
                # Remove everything after the first '#' character (including '#')
                cleaned_line = line.split("#", 1)[0]
                outfile.write(cleaned_line)

    except FileNotFoundError:
        print(f'Error reading file: "{input_file}" does not exist.')
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    This is the main function that prompts the user for input and output file names
    and calls the remove_comments function to process the file.
    """
    try:
        # Get the input and output file names from the user
        input_file = input("File to read: ").strip()
        output_file = input("File to save: ").strip()

        # Call the function to remove comments
        remove_comments(input_file, output_file)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
