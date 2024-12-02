import os
import json
from datetime import datetime
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Logger class to handle logging actions to a file
class CarParkingLogger:
    """
    Handles logging of parking actions to a log file.

    Attributes:
        id (str): The unique identifier for the car parking machine.
        log_file (str): The path to the log file where actions are recorded.
    """

    def __init__(self, id: str, log_file: str = "carparklog.txt"):
        """
        Initializes the CarParkingLogger with an ID and log file path.

        Args:
            id (str): The unique identifier for the car parking machine.
            log_file (str, optional): The log file path. Defaults to 'carparklog.txt'.
        """
        self.id = id
        self.log_file = os.path.join(BASE_DIR, log_file)

    def log_action(
        self, license_plate: str, action: str, parking_fee: float = None
    ) -> None:
        """
        Logs a parking action to the log file.

        Args:
            license_plate (str): The license plate of the car.
            action (str): The action performed ('check-in' or 'check-out').
            parking_fee (float, optional): The parking fee if applicable. Defaults to None.
        """
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        fee_part = f";parking_fee={parking_fee:.2f}" if parking_fee is not None else ""
        log_entry = f"{timestamp};cpm_name={self.id};license_plate={license_plate};action={action}{fee_part}\n"
        with open(self.log_file, "a") as file:
            file.write(log_entry)


# JSON-based state management
class JSONStateManager:
    """
    Manages the state of parked cars using a JSON file.

    Attributes:
        file_path (str): The path to the JSON file for storing parked car data.
    """

    def __init__(self, id: str):
        """
        Initializes the JSONStateManager with a unique machine ID.

        Args:
            id (str): The unique identifier for the car parking machine.
        """
        self.file_path = os.path.join(BASE_DIR, f"{id}_state.json")
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def save_state(self, parked_cars: dict):
        """
        Saves the current state of parked cars to the JSON file.

        Args:
            parked_cars (dict): A dictionary of ParkedCar objects.
        """
        data = [
            {
                "license_plate": car.license_plate,
                "check_in": car.check_in.strftime("%d-%m-%Y %H:%M:%S"),
            }
            for car in parked_cars.values()
        ]
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load_state(self) -> dict:
        """
        Loads the state of parked cars from the JSON file.

        Returns:
            dict: A dictionary of ParkedCar objects.
        """
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r") as file:
            data = json.load(file)
        parked_cars = {
            car["license_plate"]: ParkedCar(
                license_plate=car["license_plate"],
                check_in=datetime.strptime(car["check_in"], "%d-%m-%Y %H:%M:%S"),
            )
            for car in data
        }
        return parked_cars


class ParkedCar:
    """
    Represents a car that is currently parked.

    Attributes:
        license_plate (str): The license plate of the car.
        check_in (datetime): The timestamp when the car checked in.
    """

    def __init__(self, license_plate: str, check_in: datetime) -> None:
        """
        Initializes a ParkedCar instance.

        Args:
            license_plate (str): The license plate of the car.
            check_in (datetime): The timestamp of the check-in time.
        """
        self.license_plate = license_plate
        self.check_in = check_in


class CarParkingMachine:
    """
    Represents a car parking machine with parking functionality.

    Attributes:
        id (str): The unique identifier for the parking machine.
        capacity (int): The maximum number of cars that can be parked.
        hourly_rate (float): The hourly parking rate in euros.
        logger (CarParkingLogger): The logger for recording parking actions.
        state_manager (JSONStateManager): The state manager for persisting parked car data.
        parked_cars (dict): A dictionary of currently parked cars.
    """

    def __init__(self, id: str, capacity: int = 10, hourly_rate: float = 2.50) -> None:
        """
        Initializes the CarParkingMachine with an ID, capacity, and hourly rate.

        Args:
            id (str): The unique identifier for the parking machine.
            capacity (int, optional): The maximum capacity. Defaults to 10.
            hourly_rate (float, optional): The hourly parking rate in euros. Defaults to 2.50.
        """
        self.id = id
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.logger = CarParkingLogger(id)
        self.state_manager = JSONStateManager(id)
        self.parked_cars = self.state_manager.load_state()

    def check_in(self, license_plate: str, check_in: datetime = None) -> bool:
        """
        Checks in a car if space is available.

        Args:
            license_plate (str): The license plate of the car.
            check_in (datetime, optional): The check-in timestamp. Defaults to the current time.

        Returns:
            bool: True if the car is successfully checked in, False otherwise.
        """
        if len(self.parked_cars) >= self.capacity:
            return False
        if license_plate in self.parked_cars:
            return True
        check_in = check_in or datetime.now()
        self.parked_cars[license_plate] = ParkedCar(license_plate, check_in)
        self.logger.log_action(license_plate, "check-in")
        self.state_manager.save_state(self.parked_cars)
        return True

    def check_out(self, license_plate: str) -> float:
        """
        Checks out a car and calculates the parking fee.

        Args:
            license_plate (str): The license plate of the car.

        Returns:
            float: The total parking fee in euros, or 0.0 if the car is not found.
        """
        if license_plate not in self.parked_cars:
            print(f"License {license_plate} not found!")
            return 0.0
        fee = self.get_parking_fee(license_plate)
        del self.parked_cars[license_plate]
        self.logger.log_action(license_plate, "check-out", parking_fee=fee)
        self.state_manager.save_state(self.parked_cars)
        return fee

    def get_parking_fee(self, license_plate: str) -> float:
        """
        Calculates the parking fee for a car.

        Args:
            license_plate (str): The license plate of the car.

        Returns:
            float: The calculated parking fee in euros.
        """
        parked_car = self.parked_cars[license_plate]
        parked_duration = datetime.now() - parked_car.check_in
        parked_hours = math.ceil(parked_duration.total_seconds() / 3600)
        parked_hours = min(parked_hours, 24)
        return self.hourly_rate * parked_hours


# Main function
def main():
    """
    Main function to interact with the car parking system via a menu interface.
    """
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
