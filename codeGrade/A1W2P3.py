def range_side():
    try:
        user_input = int(input("Please enter a number of sides: "))
        shapes = {3: "Triangle", 4: "Square", 5: "Pentagon", 6: "Hexagon", 
                  7: "Heptagon", 8: "Octagon", 9: "Nonagon", 10: "Decagon"}
        print(shapes.get(user_input, "Amount of sides is out of range"))
    except ValueError:
        print("Invalid input. Please enter a valid number.")

range_side()