def dog_years():
    try:
        human_age = int(input("Human age: "))

        if human_age == 1:
            print(f"Dog age: 10.5")
        elif human_age ==2:
            print(f"Dog age: 21")
        elif human_age >= 3:
            dog_age = (human_age - 2) * 4 + 21
            print(f"Dog age: {dog_age}")
        elif human_age < 0:
            print(f"Only positive numbers are allowd.")
        else:
            print("Invalid input.")
    except ValueError:
        print("Invalid input. Please enter a valid age.")
dog_years()