def check_triangle(side_a, side_b, side_c) -> bool:
    sides = sorted([side_a, side_b, side_c])

    return sides[0] + sides[1] > sides[2]

def main():
    side_a = int(input("Side A: "))
    side_b = int(input("Side B: "))
    side_c = int(input("Side C: "))

    if check_triangle(side_a, side_b, side_c):
        print("Possible triangle")
    else:
        print("Impossible triangle")

if __name__ == "__main__":
    main()