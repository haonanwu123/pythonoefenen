import os
import sys


def detect_repeated_words(file_path):
    """
    Detects and optionally removes consecutive duplicate words in a text file.

    Parameters:
    file_path (str): The path to the file to process.

    The function reads the file line by line and checks for consecutive duplicate words.
    If a duplicate is found, the user can choose to either remove the duplicate or stop processing.
    """
    try:
        # Open the file safely with proper encoding and error handling
        with open(
            os.path.join(sys.path[0], file_path), "r", newline="", encoding="utf8"
        ) as file:
            lines = file.readlines()

        # Process each line in the file
        for line_number, line in enumerate(lines, start=1):
            words = line.split()  # Split the line into individual words
            duplicate_found = False  # Flag to track if a duplicate is found

            # Iterate through the words to check for consecutive duplicates
            for i in range(1, len(words)):
                if (
                    words[i].lower() == words[i - 1].lower()
                ):  # Case-insensitive comparison
                    duplicate_found = True
                    repeat_word = words[i]

                    # Notify the user about the duplicate word
                    print(
                        f"Duplicate word '{repeat_word}' found on line {line_number}."
                    )

                    # Ask the user what to do with the duplicate
                    while True:
                        response = (
                            input(
                                f"Do you want to remove '{repeat_word}' or find the next duplicate? (remove/continue/no): "
                            )
                            .strip()
                            .lower()
                        )

                        if response in ["remove", "continue", "no"]:
                            break
                        else:
                            print(
                                "Invalid input. Please enter 'remove', 'continue', or 'no'."
                            )

                    # Handle the user's response
                    if response == "remove":
                        # Remove the duplicate word and update the line
                        line = line.replace(
                            f"{repeat_word} {repeat_word}", f"{repeat_word}", 1
                        )
                        print(
                            f"Removed duplicate '{repeat_word}' from line {line_number}."
                        )
                        break  # Stop further duplicate checks for this line after removal

                    elif response == "no":
                        print("Exiting duplicate detection.")
                        return  # Exit the function entirely

                    # If 'continue', simply move to the next duplicate in the same line
                    elif response == "continue":
                        continue

            # Display the processed line (modified or unmodified)
            if duplicate_found:
                print(f"Processed line {line_number}: {line.strip()}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    """
    Main function to initiate the repeated word detection program.
    """
    # Prompt the user for the file path
    file_path = input("Please enter your file path: ").strip()
    detect_repeated_words(file_path)


if __name__ == "__main__":
    main()
