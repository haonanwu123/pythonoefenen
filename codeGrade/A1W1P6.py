def sum_of_digits():
    user_input = input("Please enter a four-digits number")

    try:
        if len(user_input) == 4 and user_input.isdigit():
            digits = [int(digit) for digit in user_input]
            total_sum = sum(digits)

            print(f"{'+'.join(user_input)}={total_sum}")
        else:
            print("Invalid input. Please enter a valid four-digit integer.")
    except ValueError:
        print("Invalid input. Please enter a valid four-digit integer.")

sum_of_digits()