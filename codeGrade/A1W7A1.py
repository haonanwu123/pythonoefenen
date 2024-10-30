dict_key_value = {}
encoded_values = []
decoded_values = []


def encode_string(data: str, key: str = None) -> str:
    key_map = (
        dict_key_value
        if key is None
        else {key[i]: key[i + 1] for i in range(0, len(key), 2)}
    )
    return "".join(key_map.get(char, char) for char in data)


def decode_string(data: str, key: str = None) -> str:
    key_map = (
        dict_key_value
        if key is None
        else {key[i]: key[i + 1] for i in range(0, len(key), 2)}
    )
    reverse_map = {v: k for k, v in key_map.items()}
    return "".join(reverse_map.get(char, char) for char in data)


def encode_list(data: list, key: str = None) -> list:
    return list(map(lambda s: encode_string(s, key), data))


def decode_list(data: list, key: str = None) -> list:
    return list(map(lambda s: decode_string(s, key), data))


def validate_values(encoded: str, decoded: str, key: str = None) -> bool:
    return (
        encode_string(decoded, key) == encoded
        and decode_string(encoded, key) == decoded
    )


def set_dict_key(key: str) -> None:
    global dict_key_value
    if len(key) % 2 != 0:
        print("Invalid hashvalue input")
        return False

    dict_key_value.clear()

    for i in range(0, len(key), 2):
        dict_key_value[key[i]] = key[i + 1]

    return dict_key_value


def main():
    key_input = input(
        "Please enter a key string (or press Enter to use default key): "
    ).strip()

    if set_dict_key(key_input) is False:
        return

    while True:
        print("\n[Menu]")
        print("[E] Encode value to hashed value")
        print("[D] Decode hashed value to normal value")
        print("[P] Print all encoded/decoded values")
        print("[V] Validate 2 values against eachother")
        print("[Q] Quit program")

        choice = input("Choose an option: ").upper().strip()

        if choice == "E":
            value = input("Enter a value to encode: ").strip().replace(",", "")
            encoded = encode_string(value)
            encoded_values.append(encoded)
            list_encoded = encode_list(value)
            print(f"Encoded: {list_encoded}")

        elif choice == "D":
            value = input("Enter a value to decode: ").strip().replace(",", "")
            decoded = decode_string(value)
            decoded_values.append(decoded)
            list_decoded = decode_list(value)
            print(f"Decoded: {list_decoded}")

        elif choice == "P":
            print("\nEncoded values:")
            for value in encoded_values:
                print(f"Encoded: {value}")

            print("\nDecoded values:")
            for value in decoded_values:
                print(f"Decoded: {value}")

        elif choice == "V":
            encoded = input("Enter the encoded value: ").strip()
            decoded = input("Enter the decoded value: ").strip()

            if validate_values(encoded, decoded):
                print("Values match")
            else:
                print("Values do not match")

        elif choice == "Q":
            break

        else:
            print("Invalid option. Please choose a valid option.")


if __name__ == "__main__":
    main()
