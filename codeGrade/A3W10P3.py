import os


def find_longest_words(file_name):
    """
    Finds and displays the longest word(s) in a file.

    Parameters:
        file_name (str): The path to the file to process.

    The program splits the file's content into words by treating any group of non-whitespace
    characters as a word. It then identifies the longest word(s) in the file and prints their
    length and values. If the file cannot be read, an appropriate error message is displayed.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        # Check if the file exists
        if not os.path.isfile(file_name):
            raise FileNotFoundError

        # Read the file content
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()

        # Split the content into words (manually, without `re`)
        words = []
        current_word = []
        for char in content:
            if char.isspace():  # Treat whitespace as a word boundary
                if current_word:
                    words.append("".join(current_word))
                    current_word = []
            else:
                current_word.append(char)
        if current_word:  # Add the last word if it exists
            words.append("".join(current_word))

        # Find the length of the longest word(s)
        max_length = 0
        longest_words = []
        for word in words:
            word_length = len(word)
            if word_length > max_length:
                max_length = word_length
                longest_words = [word]
            elif word_length == max_length:
                longest_words.append(word)

        # Output the results
        print(f"Length of longest word(s) is [{max_length}] chars")
        print("These are all the words of that length:")
        print(", ".join(longest_words))

    except FileNotFoundError:
        print(f'Error reading file: "{file_name}"')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    file_name = input("Enter the file name: ").strip()
    find_longest_words(file_name)


if __name__ == "__main__":
    main()
