def chess_square_color():
    try:
        position = input("Position: ").strip().upper()

        if len(position) != 2:
            raise ValueError

        column = position[0]
        row = int(position[1])
        
        if column < 'A' or column > 'H' or row < 1 or row > 8:
            raise ValueError
        
        column_number = ord(column) - ord('A') + 1

        if (column_number + row) % 2 == 0:
            print("Black")
        else:
            print("White")

    except ValueError:
        print("Invalid input. The letter must be between A to H, and the number must be between 1 to 8.")

chess_square_color()