import random


def load_words(file_path):
    """
    Load words form a file and return a list of words.
    Each word must have at least 3 characters.
    """
    with open(file_path, "r") as file:
        words = [line.strip() for line in file if len(line.strip()) >= 3]
        return words


def generate_password(words):
    """
    Generate a password by concatenating two random words from the list.
    The password must be 8–10 characters long and capitalize both words.
    """
    while True:
        word1 = random.choice(words)
        word2 = random.choice(words)
        if word1 != word2:
            password = word1.capitalize() + word2.capitalize()
            if 8 <= len(password) <= 10:
                return password


def main():
    """
    Main function to generate a password.
    Input a file path and then get a ramdom password.
    """
    file_path = input("Enter the path to the file containing the word list: ").strip()

    try:
        words = load_words(file_path)

        if len(words) < 2:
            print("The file must contain at least two suitable words (3+ letters).")
            return

        password = generate_password(words)
        print("Generated password:", password)

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
