def draw_modular_ractangle(width, height):
    for row in range(height):
        row_values = [(row * width + col) % 10 for col in range(width)]
        row_str = " ".join(f'{value}' for value in row_values)
        print(row_str + " ")


def main():
    try:
        width = int(input("enter a number of width: "))
        height = int(input("enter a number of height: "))

        draw_modular_ractangle(width, height)
    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
