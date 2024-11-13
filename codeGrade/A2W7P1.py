import os
import sys

MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def load_txt_file(file_name):
    file_content = {}

    with open(
        os.path.join(sys.path[0], file_name), newline="", encoding="utf8"
    ) as file_obj:
        for line in file_obj.readlines():
            month, day, year, temp_f = line.split()
            year = int(year)
            month = int(month)
            day = int(day)
            temp_f = float(temp_f)

            if year not in file_content:
                file_content[year] = {}

            if month not in file_content[year]:
                file_content[year][month] = []

            file_content[year][month].append(temp_f)

    return file_content


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5.0 / 9.0


def average_temp_per_month(temperatures_for_year: dict) -> list:
    avg_temps = []
    for month, temps in temperatures_for_year.items():
        avg_temp = sum(temps) / len(temps)
        avg_temps.append((month, avg_temp))
    return avg_temps


def average_temp_per_year(temperatures: dict) -> list:
    avg_temps_per_year = []
    for year, months in temperatures.items():
        all_temps = [temp for month in months.values() for temp in month]
        avg_temp = sum(all_temps) / len(all_temps)
        # truncated_avg_temp = int(avg_temp * 100) / 100  # No rounding is performed
        avg_temps_per_year.append((year, avg_temp))
    return avg_temps_per_year


def warmest_and_coldest_year(avg_temps_per_year: list) -> tuple:
    warmest_year = max(avg_temps_per_year, key=lambda x: x[1])
    coldest_year = min(avg_temps_per_year, key=lambda x: x[1])
    return (warmest_year[0], coldest_year[0])


def extreme_month_of_year(temperatures: dict, year: int, warmest=True) -> str:
    if year not in temperatures:
        return "Year not found."

    avg_temps = average_temp_per_month(temperatures[year])
    if warmest:
        month_num, _ = max(avg_temps, key=lambda x: x[1])
    else:
        month_num, _ = min(avg_temps, key=lambda x: x[1])

    return MONTHS[month_num]


def average_temp_per_month_in_celsius(temperatures: dict) -> list:
    result = []

    for year, months_data in temperatures.items():
        month_avg_celsius = {}
        for month, temps in months_data.items():
            avg_f = sum(temps) / len(temps)
            avg_c = fahrenheit_to_celsius(avg_f)
            month_avg_celsius[MONTHS[month]] = avg_c
        result.append((year, month_avg_celsius))

    return result


def main():
    file_name = "file/NLAMSTDM.txt"
    temperatures = load_txt_file(file_name)

    print("[1] Print the average temperatures per year (Fahrenheit)")
    print("[2] Print the average temperatures per year (Celsius)")
    print("[3] Print the warmest and coldest year based on the average temperature")
    print("[4] Print the warmest month of a year")
    print("[5] Print the coldest month of a year")
    print("[6] Print average temperatures per month in Celsius per year")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        avg_temps = average_temp_per_year(temperatures)
        output = ", ".join(
            [f"({year}, {avg_temp})" for year, avg_temp in avg_temps])
        print(f"[{output}]")

    elif choice == "2":
        avg_temps = average_temp_per_year(temperatures)
        output = ", ".join(
            [
                f"({year}, {fahrenheit_to_celsius(avg_temp)})"
                for year, avg_temp in avg_temps
            ]
        )
        print(f"[{output}]")

    elif choice == "3":
        avg_temps = average_temp_per_year(temperatures)
        warmest, coldest = warmest_and_coldest_year(avg_temps)
        print(f"({warmest}, {coldest})")

    elif choice == "4":
        year = int(input("Enter the year: "))
        warmest_month = extreme_month_of_year(temperatures, year, warmest=True)
        print(f"The warmest month in {year} is {warmest_month}")

    elif choice == "5":
        year = int(input("Enter the year: "))
        coldest_month = extreme_month_of_year(
            temperatures, year, warmest=False)
        print(f"The coldest month in {year} is {coldest_month}")

    elif choice == "6":
        avg_temps_celsius = average_temp_per_month_in_celsius(temperatures)
        for year, months_data in avg_temps_celsius:
            print(f"({year}, " + "{", end="")
            month_strings = []
            for month_name, avg_temp_c in months_data.items():
                month_number = next(key for key, value in MONTHS.items() if value == month_name)
                month_strings.append(f"{month_number}: {avg_temp_c}")

            print(", ".join(month_strings), end="")
            print("})")
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
