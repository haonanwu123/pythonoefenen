def unique_chars_dict(s) -> int:
    char_dict = {}

    for char in s:
        if char not in char_dict:
            char_dict[char] = (
                1  # add any number or char to make the unique_chars  {d:1, a:1, ...}
            )
    return len(char_dict)


def unique_chars_set(s) -> int:
    unique_set = set(s)
    return len(unique_set)


def main():
    user_input = input("Enter a string: ")
    print(f"Unique characters (using dictionary): {unique_chars_dict(user_input)}")
    print(f"Unique characters (using set): {unique_chars_set(user_input)}")


if __name__ == "__main__":
    main()
