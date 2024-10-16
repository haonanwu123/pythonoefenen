def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def print_conversion_table():
    print(f"{'°C':>3} {'°F':>5}")
    print("-" * 10)

    for celsius in range(0, 101, 10):
        fahrenheit = celsius_to_fahrenheit(celsius)
        print(f"{celsius:>3} {int(fahrenheit):>5}")

print_conversion_table()