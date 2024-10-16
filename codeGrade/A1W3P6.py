def binary_to_decimal():
    try:
        binary = input("Binary: ")
        if not all(char in '01' for char in binary):
            print("Invalid binary number. Please enter a binary number with only 1 and 0.")
        else:
            decimal = int(binary, 2)
            print(f"{decimal}")

    except ValueError:
        print("Invalid binary number. Please enter a valid binary number.")

binary_to_decimal()