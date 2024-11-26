import os
from datetime import datetime, timedelta
import math


# Logger class to handle logging actions to a file
class CarParkingLogger:
    def __init__(self, id: str, log_file: str = "carparklog.txt"):
        self.id = id
        self.log_file = log_file

    def log_action(
        self, license_plate: str, action: str, parking_fee: float = None
    ) -> None:
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        fee_part = f";parking_fee={parking_fee:.2f}" if parking_fee is not None else ""
        log_entry = f"{timestamp};cpm_name={self.id};license_plate={license_plate};action={action}{fee_part}\n"
        with open(self.log_file, "a") as file:
            file.write(log_entry)

    def load_unchecked_cars(self) -> dict:
        """
        Load non-checked-out cars from the log file for this parking machine.
        Returns a dictionary of license plates and their ParkedCar instances.
        """
        parked_cars = {}
        if not os.path.exists(self.log_file):
            return parked_cars

        with open(self.log_file, "r") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(";")
            if len(parts) < 3:
                continue
            timestamp, cpm_name, license_plate, action = (
                parts[0],
                parts[1],
                parts[2],
                parts[3],
            )
            if cpm_name.split("=")[1] == self.id:
                plate = license_plate.split("=")[1]
                if action == "action=check-in":
                    check_in_time = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")
                    parked_cars[plate] = ParkedCar(
                        license_plate=plate, check_in=check_in_time
                    )
                elif action == "action=check-out":
                    parked_cars.pop(plate, None)
        return parked_cars

    def get_machine_fee_by_day(
        self, car_parking_machine_id: str, search_date: str
    ) -> float:
        """
        Get the total parking fee for a specific car parking machine on a specific day.
        """
        total_fee = 0.0
        if not os.path.exists(self.log_file):
            return total_fee

        search_date = datetime.strptime(search_date, "%d-%m-%Y").strftime("%d-%m-%Y")

        with open(self.log_file, "r") as file:
            for line in file:
                parts = line.strip().split(";")
                if len(parts) >= 5:
                    timestamp, cpm_name, _, action, fee = parts
                    if cpm_name.split("=")[1].lower() == car_parking_machine_id.lower():
                        log_date = timestamp.split(" ")[0]
                        if log_date == search_date and action == "action=check-out":
                            total_fee += float(fee.split("=")[1])
        return round(total_fee, 2)

    def get_total_car_fee(self, license_plate: str) -> float:
        """
        Get the total parking fee for a specific license plate across all machines.
        """
        total_fee = 0.0
        if not os.path.exists(self.log_file):
            return total_fee

        with open(self.log_file, "r") as file:
            for line in file:
                parts = line.strip().split(";")
                if len(parts) >= 5:
                    _, _, plate, action, fee = parts
                    if (
                        plate.split("=")[1].lower() == license_plate.lower()
                        and action == "action=check-out"
                    ):
                        total_fee += float(fee.split("=")[1])
        return round(total_fee, 2)


class ParkedCar:
    def __init__(self, license_plate: str, check_in: datetime) -> None:
        self.license_plate = license_plate
        self.check_in = check_in


# CarParkingMachine class
class CarParkingMachine:
    def __init__(self, id: str, capacity: int = 10, hourly_rate: float = 2.50) -> None:
        self.id = id
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.logger = CarParkingLogger(id)
        self.parked_cars = self.logger.load_unchecked_cars()

    def check_in(self, license_plate: str, check_in: datetime = None) -> bool:
        if len(self.parked_cars) >= self.capacity:
            return False  # Return False if capacity is reached or car is already checked in
        if license_plate in self.parked_cars:
            return True  # Car already checked in
        check_in = check_in or datetime.now()
        self.parked_cars[license_plate] = ParkedCar(license_plate, check_in)
        self.logger.log_action(license_plate, "check-in")
        return True

    def check_out(self, license_plate: str) -> float:
        if license_plate not in self.parked_cars:
            print(f"License {license_plate} not found!")
            return 0.0
        fee = self.get_parking_fee(license_plate)
        del self.parked_cars[license_plate]
        self.logger.log_action(license_plate, "check-out", parking_fee=fee)
        return fee

    def get_parking_fee(self, license_plate: str) -> float:
        parked_car = self.parked_cars[license_plate]
        parked_duration = datetime.now() - parked_car.check_in
        parked_hours = math.ceil(parked_duration.total_seconds() / 3600)
        parked_hours = min(parked_hours, 24)  # Max fee is 24 hours
        print(f"Check-in time: {parked_car.check_in}")
        print(f"Parked duration (in hours): {parked_duration.total_seconds() / 3600}")
        print(f"Rounded hours: {parked_hours}")
        return self.hourly_rate * parked_hours


# Main function
def main():
    parking_machine = None

    while True:
        # Display the main menu options
        print(
            "[I] Check-in car by license plate\n"
            "[O] Check-out car by license plate\n"
            "[Q] Quit program"
        )
        choice = input("> ").strip().upper()

        if choice == "Q":
            print("Exiting program.")
            break

        elif choice in ["I", "O"]:
            # Initialize parking machine if not already set
            if parking_machine is None:
                parking_machine_id = input("Enter parking machine ID: ").strip()
                parking_machine = CarParkingMachine(parking_machine_id)

            if choice == "I":
                license_plate = input("License: ").strip().upper()
                if parking_machine.check_in(license_plate):
                    print("License registered.")
                else:
                    print("Capacity reached or car already checked in.")
            elif choice == "O":
                license_plate = input("License: ").strip().upper()
                fee = parking_machine.check_out(license_plate)
                if fee > 0:
                    print(f"Parking fee: {fee:.2f} euro.")
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
