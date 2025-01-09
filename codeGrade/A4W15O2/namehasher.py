# Define global variables to store mappings and values
hashmap_key_value = {}
encoded_values = []
decoded_values = []


def encode_string(data: str, hofunction) -> str:
    """
    Encodes the given string using the provided high-order function.
    """
    return "".join(hofunction(char) for char in data)


def decode_string(data: str, hofunction) -> str:
    """
    Decodes the given string using the provided high-order function.
    """
    return "".join(hofunction(char) for char in data)


def encode_list(data: list, hofunction) -> list:
    """
    Encodes a list of strings using the provided high-order function.
    """
    return [encode_string(item, hofunction) for item in data]


def decode_list(data: list, hofunction) -> list:
    """
    Decodes a list of strings using the provided high-order function.
    """
    return [decode_string(item, hofunction) for item in data]


def validate_values(
    encoded: str, decoded: str, encode_function, decode_function
) -> bool:
    """
    Validates if the encoding and decoding of strings match.
    """
    return (
        encode_string(decoded, encode_function) == encoded
        and decode_string(encoded, decode_function) == decoded
    )


def set_dict_key(key: str) -> None:
    """
    Sets up the dictionary for encoding and decoding.
    """
    global hashmap_key_value
    if len(key) % 2 != 0:
        print("Invalid key input. Key must have even number of characters.")
        return False

    hashmap_key_value.clear()
    for i in range(0, len(key), 2):
        hashmap_key_value[key[i]] = key[i + 1]

    return True


def encode_function(char: str) -> str:
    """
    High-order function for encoding characters using hashmap_key_value.
    """
    return hashmap_key_value.get(char, char)


def decode_function(char: str) -> str:
    """
    High-order function for decoding characters using hashmap_key_value.
    """
    reverse_map = {v: k for k, v in hashmap_key_value.items()}
    return reverse_map.get(char, char)


def main():
    key_input = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if not set_dict_key(key_input):
        return

    while True:
        print("\n[Menu]")
        print("[E] Encode value to hashed value")
        print("[D] Decode hashed value to normal value")
        print("[P] Print all encoded/decoded values")
        print("[V] Validate 2 values against eachother")
        print("[Q] Quit program")

        choice = input("Choose an option: ").strip().upper()
        if choice == "E":
            value = input("Enter a value to encode: ").strip()
            encoded = encode_string(value, encode_function)
            encoded_values.append(encoded)
            print(f"Encoded: {encoded}")

        elif choice == "D":
            value = input("Enter a value to decode: ").strip()
            decoded = decode_string(value, decode_function)
            decoded_values.append(decoded)
            print(f"Decoded: {decoded}")

        elif choice == "P":
            print("\nEncoded values:")
            for v in encoded_values:
                print(f"Encoded: {v}")

            print("\nDecoded values:")
            for v in decoded_values:
                print(f"Decoded: {v}")

        elif choice == "V":
            encoded = input("Enter the encoded value: ").strip()
            decoded = input("Enter the decoded value: ").strip()

            if validate_values(encoded, decoded, encode_function, decode_function):
                print("Values match!")
            else:
                print("Values do not match.")

        elif choice == "Q":
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
