def calculate_area():
    try:
        width = float(input("Width: "))
        length = float(input("Length: "))

        area = width * length

        print(f"The Area of the Room: {area}")
    
    except ValueError:
        print("Invalid input. Please enter numeric values for width and length.")

calculate_area()