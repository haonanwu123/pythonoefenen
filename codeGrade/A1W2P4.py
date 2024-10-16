def classify_triangle():
    user_input = input("Sides (comma separated, e.g. a=5, b=6, c=5): ")
    
    sides = user_input.split(',')
    a = int(sides[0].split('=')[1].strip())
    b = int(sides[1].split('=')[1].strip())
    c = int(sides[2].split('=')[1].strip())

    side_lengths = {a, b, c}

    if len(side_lengths) == 1:
        print("Equilateral triangle")
    elif len(side_lengths) == 2:
        print("Isosceles triangle")
    else:
        print("Scalene triangle")

classify_triangle()