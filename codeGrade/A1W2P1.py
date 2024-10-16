def is_even_odd():

    try:
        user_input = int(input("Enter a number:"))

        if user_input % 2 == 0:
            print("even")
        else:
            print("odd")

    except (IndexError, ValueError):
        print("Please enter an valid number.")

is_even_odd()