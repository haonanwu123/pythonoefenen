import os
import sys


def clean_word(word):
    """
    Cleans a word by removing leading/trailing punctuation and converting it to lowercase.
    """
    # Manually remove leading/trailing punctuation
    word = "".join([char for char in word if char.isalpha()])
    return word.lower()


def find_most_and_least_frequent_words(file_path):
    """
    Find and display the most and least frequent words in the given file.
    """
    try:
        word_counts = {}

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f'Error reading file: "{file_path}" does not exist.')
            return

        # Open and read the file
        with open(file_path, "r") as file:
            for line in file:
                # Split the line into words
                words = line.split()

                for word in words:
                    # Clean each word (remove punctuation and convert to lowercase)
                    cleaned_word = clean_word(word)

                    if cleaned_word:  # Only count non-empty words
                        word_counts[cleaned_word] = word_counts.get(cleaned_word, 0) + 1

        if not word_counts:
            print("The file is empty or does not contain valid words.")
            return

        # Find the maximum and minimum frequencies
        max_frequency = max(word_counts.values())
        min_frequency = min(word_counts.values())

        # Find all words with the max and min frequencies
        most_frequent_words = [
            word for word, count in word_counts.items() if count == max_frequency
        ]
        least_frequent_words = [
            word for word, count in word_counts.items() if count == min_frequency
        ]

        # Display the results
        print(f"Most: {most_frequent_words}")
        print(f"Least: {least_frequent_words}")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main function to read the file name from user input and display the most and least frequent words.
    """
    # Check if the file path was passed via the command line argument
    if len(sys.argv) != 1:
        print("Usage: python3 script.py <file_path>")
        return

    try:
        file_path = input("Enter your path: ").strip()

        if not file_path:
            file_path = sys.argv[0]
    except Exception as e:
        print(f"An error occurred: {e}")

    find_most_and_least_frequent_words(file_path)


if __name__ == "__main__":
    main()
