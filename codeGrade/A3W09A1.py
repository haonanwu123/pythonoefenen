from datetime import datetime, timedelta
import math


# ParkedCar class to store information of parked cars
class ParkedCar:
    def __init__(self, license_plate: str, check_in: datetime) -> None:
        self.license_plate = license_plate
        self.check_in = check_in


# CarParkingMachine class to manage the car park operations
class CarParkingMachine:
    def __init__(self, capacity: int = 10, hourly_rate: float = 2.50) -> None:
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.parked_cars = {}

    def check_in(
        self,
        license_plate: str,
        check_in: datetime = None,
    ) -> bool:
        if len(self.parked_cars) >= self.capacity:
            print("Capacity reached!")
            return False
        check_in = check_in or datetime.now()
        self.parked_cars[license_plate] = ParkedCar(license_plate, check_in)
        print("License registered")
        return True

    def check_out(self, license_plate: str) -> float:
        if license_plate not in self.parked_cars:
            print(f"License {license_plate} not found!")
            return 0.0
        fee = self.get_parking_fee(license_plate)
        del self.parked_cars[license_plate]  # Remove car from the lot
        print(f"Parking fee: {fee:.2f} euro")
        return fee

    def get_parking_fee(self, license_plate: str) -> float:
        parked_car = self.parked_cars[license_plate]
        parked_duration = datetime.now() - parked_car.check_in
        parked_hours = math.ceil(parked_duration.total_seconds() / 3600)
        parked_hours = min(parked_hours, 24)  # Max fee is 24 hours
        return self.hourly_rate * parked_hours


# Main function for the command-line menu
def main():
    parking_machine = CarParkingMachine()

    while True:
        choice = (
            input(
                "[I] Check-in car by license plate\n[O] Check-out car by license plate\n[Q] Quit program\n"
            )
            .strip()
            .upper()
        )

        if choice == "I":
            license_plate = input("License: ").strip().upper()
            parking_machine.check_in(license_plate)

        elif choice == "O":
            license_plate = input("License: ").strip().upper()
            parking_machine.check_out(license_plate)

        elif choice == "Q":
            print("Exiting program.")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
