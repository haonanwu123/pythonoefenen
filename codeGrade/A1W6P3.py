def is_valid_password(password):
    digits = set("0123456789")
    lowercase = set("abcdefghijklmnopqrstuvwxyz")
    uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    allowed_special_symbols = set("*@!?")

    if len(password) < 8 or len(password) > 20:
        return False

    password_chars = set(password)

    has_digit = not password_chars.isdisjoint(digits)
    has_lowercase = not password_chars.isdisjoint(lowercase)
    has_uppercase = not password_chars.isdisjoint(uppercase)
    has_special_symbols = not password_chars.isdisjoint(allowed_special_symbols)

    invalid_special_symbols = password_chars
    invalid_special_symbols.difference_update(digits, lowercase, uppercase, allowed_special_symbols)
    if invalid_special_symbols:
        return False

    return has_digit and has_lowercase and has_uppercase and has_special_symbols


def main():
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        password = input("Enter a password: ").strip()

        if is_valid_password(password):
            print("Password is valid.")
            return
        else:
            print("Password is invalid.")
            attempts += 1

    print("Maximum attempts reached. Try again later.")


if __name__ == "__main__":
    main()