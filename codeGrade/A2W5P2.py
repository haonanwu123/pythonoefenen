def calculate_fare(distance):
    base_fare = 4.00
    fare_per_140m = 0.25
    distance_meters = distance * 1000
    blocks = distance_meters // 140

    if distance_meters % 140 != 0:
        blocks += 1
    total_fare = base_fare + (blocks * fare_per_140m)

    return total_fare


def main():
    distance = float(input("Distance traveled (in kilometers): "))
    fare = calculate_fare(distance)
    print(f"Total fare: {fare:.2f} EUR")


if __name__ == "__main__":
    main()