def unique_chars_dict(s: str) -> int:
    """
    Returns the number of unique characters in the given string using a dictionary.

    This function iterates through the input string and adds each unique character
    to a dictionary as a key. The length of the dictionary (number of keys) is
    then returned, which represents the number of unique characters.

    Args:
        s (str): The input string.

    Returns:
        int: The number of unique characters in the string.
    """
    char_dict = {}

    for char in s:
        if char not in char_dict:
            char_dict[char] = 1  # Placeholder to track unique characters
    return len(char_dict)


def unique_chars_set(s: str) -> int:
    """
    Returns the number of unique characters in the given string using a set.

    This function uses a set to store only unique characters from the input string,
    and then returns the size of the set.

    Args:
        s (str): The input string.

    Returns:
        int: The number of unique characters in the string.
    """
    unique_set = set(s)
    return len(unique_set)


def main():
    """
    Main function that prompts the user to input a string and displays
    the number of unique characters in the string using both the dictionary
    and set methods.
    """
    user_input = input("Enter a string: ")
    print(f"Unique characters (using dictionary): {unique_chars_dict(user_input)}")
    print(f"Unique characters (using set): {unique_chars_set(user_input)}")


if __name__ == "__main__":
    main()
