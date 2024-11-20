import os


def redact_sensitive_words(original_file, sensitive_words_file, redacted_file):
    """
    Redacts sensitive words in a text file by replacing them with asterisks.

    Parameters:
    original_file (str): Path to the original text file.
    sensitive_words_file (str): Path to the file containing sensitive words (one per line).
    redacted_file (str): Path to save the redacted text file.

    The function reads the original text and sensitive words,
    replaces all occurrences of sensitive words with asterisks,
    and writes the redacted text to a new file.
    """
    try:
        # Load sensitive words from the file
        with open(
            os.path.join(os.getcwd(), sensitive_words_file), "r", encoding="utf-8"
        ) as f:
            sensitive_words = [line.strip() for line in f.readlines()]

        # Read the original text
        with open(os.path.join(os.getcwd(), original_file), "r", encoding="utf-8") as f:
            original_text = f.read()

        # Replace each sensitive word with asterisks
        redacted_text = original_text
        for word in sensitive_words:
            redacted_text = redacted_text.replace(word, "*" * len(word))

        # Save the redacted text to the output file
        with open(os.path.join(os.getcwd(), redacted_file), "w", encoding="utf-8") as f:
            f.write(redacted_text)

        print(f"Redacted text has been saved to '{redacted_file}'.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    """
    Main function to prompt user for file names and perform the redaction process.
    """
    print("Welcome to the Text Redactor!")
    original_file = input("Enter the path to the original text file: ").strip()
    sensitive_words_file = input("Enter the path to the sensitive words file: ").strip()
    redacted_file = input("Enter the path to save the redacted file: ").strip()

    redact_sensitive_words(original_file, sensitive_words_file, redacted_file)


if __name__ == "__main__":
    main()
