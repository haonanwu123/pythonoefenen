# filename: user_age_program.py
def get_user_age(input_data: str) -> int:
    """
    Probeer de leeftijd te converteren naar een geheel getal.
    """
    try:
        age = int(input_data)
        print(f"The user's age is: {age}")
        return age
    except ValueError:
        print(
            f"Invalid input: '{input_data}' is not a valid age. Please enter a number."
        )
        return None  # Returning None to indicate an invalid age


def process_user_data() -> None:
    """
    Verwerk gebruikersgegevens, inclusief leeftijd.
    """
    age_input = input("Please enter your age: ")
    # Probeer de leeftijd om te zetten en ga door met het programma
    age = get_user_age(age_input)
    if age is not None:
        print("Processing further data...")  # Proceed with further data processing
    else:
        print("Unable to process further data due to invalid age input.")


def main():
    """
    Start het programma
    """
    process_user_data()


if __name__ == "__main__":
    main()
