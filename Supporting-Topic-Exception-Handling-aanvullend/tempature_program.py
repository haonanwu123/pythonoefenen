import os
import sys


class TemperatureDataAnalyzer:
    def __init__(self, file_path):
        self.file_path = os.path.join(sys.path[0], file_path)  # Add relative path
        self.temperature_data = []

    # Method to open the file and load lines as an attribute
    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                for line_number, line in enumerate(file, start=1):
                    try:
                        # Parse and process data line by line
                        parts = line.strip().split()
                        if len(parts) != 4:  # Check if the line has four fields
                            raise ValueError(
                                f"Line {line_number} has an incorrect format."
                            )
                        # Parsing date and temperature
                        date_parts = list(map(int, parts[:3]))  # Month, Day, Year
                        temperature = float(parts[3])  # temperature
                        self.temperature_data.append(date_parts + [temperature])
                    except ValueError as ve:
                        print(f"Skipping line {line_number}: {ve}")
                    except Exception as e:
                        print(f"Unexpected error on line {line_number}: {e}")
        except FileNotFoundError:
            print(f"The file {self.file_path} was not found.")
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")

    # Method to perform the analysis and construct the list
    def construct_temperature_list(self):
        try:
            temperature_list = []
            for data in self.temperature_data:
                month, day, year, temperature = data[:]
                # Whether the year exists in the result list
                if year not in [item[0] for item in temperature_list]:
                    temperature_list.append((year, {}))
                # Whether the month exists in the year's sub-dictionary
                if month not in temperature_list[-1][1]:
                    temperature_list[-1][1][month] = 0.0
                # Record the highest temperature of the month
                temperature_list[-1][1][month] = max(
                    temperature, temperature_list[-1][1][month]
                )
            return temperature_list
        except Exception as e:
            print(f"An unexpected error occurred during analysis: {e}")
            return []


def main():
    file_path = "./temps.txt"
    analyzer = TemperatureDataAnalyzer(file_path)
    analyzer.load_data()
    temperature_list = analyzer.construct_temperature_list()
    if temperature_list:
        print("Processed Temperature List:", temperature_list)
    else:
        print("Failed to construct temperature list due to errors.")


if __name__ == "__main__":
    main()
