import os
import sqlite3
from datetime import datetime, timedelta
import math


class ParkedCar:
    """
    Represents a car that is currently parked.

    Attributes:
        id (int): The database ID of the parked car record.
        license_plate (str): The license plate of the car.
        check_in (datetime): The timestamp when the car checked in.
        check_out (datetime): The timestamp when the car checked out.
        parking_fee (float): The parking fee charged for the car.
    """

    def __init__(
        self,
        id=None,
        license_plate=None,
        check_in=None,
        check_out=None,
        parking_fee=0.0,
    ):
        self.id = id
        self.license_plate = license_plate
        self.check_in = check_in
        self.check_out = check_out
        self.parking_fee = parking_fee


class CarParkingMachine:
    """
    Represents a car parking machine with parking functionality, backed by an SQLite database.

    Attributes:
        id (str): The unique identifier for the parking machine.
        capacity (int): The maximum number of cars that can be parked.
        hourly_rate (float): The hourly parking rate in euros.
        db_conn (sqlite3.Connection): The connection to the SQLite database.
    """

    def __init__(self, id, capacity=10, hourly_rate=2.5):
        self.id = id
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.db_conn = sqlite3.connect(
            os.path.join(os.getcwd(), "carparkingmachine.db")
        )

        # Create the PARKINGS table if it doesn't exist
        self.db_conn.execute(
            """CREATE TABLE IF NOT EXISTS parkings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_parking_machine TEXT NOT NULL,
                license_plate TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT DEFAULT NULL,
                parking_fee NUMERIC DEFAULT 0
            );"""
        )

    def find_by_id(self, id):
        """Find a parked car by its database row ID."""
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM parkings WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return ParkedCar(
                id=row[0],
                license_plate=row[2],
                check_in=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                check_out=(
                    datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S") if row[4] else None
                ),
                parking_fee=row[5],
            )
        return None

    def find_last_checkin(self, license_plate):
        """Find the last row ID for a given license plate that has not checked out yet."""
        cur = self.db_conn.cursor()
        cur.execute(
            "SELECT id FROM parkings WHERE license_plate = ? AND car_parking_machine = ? AND check_out IS NULL",
            (license_plate, self.id),
        )
        row = cur.fetchone()
        return row[0] if row else None

    def insert(self, parked_car):
        """Insert a new parked car record into the database."""
        cur = self.db_conn.cursor()
        cur.execute(
            "INSERT INTO parkings (car_parking_machine, license_plate, check_in) VALUES (?, ?, ?)",
            (
                self.id,
                parked_car.license_plate,
                parked_car.check_in.strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        self.db_conn.commit()
        parked_car.id = cur.lastrowid
        return parked_car

    def update(self, parked_car):
        """Update an existing parked car record in the database."""
        self.db_conn.execute(
            "UPDATE parkings SET check_out = ?, parking_fee = ? WHERE id = ?",
            (
                parked_car.check_out.strftime("%Y-%m-%d %H:%M:%S"),
                parked_car.parking_fee,
                parked_car.id,
            ),
        )
        self.db_conn.commit()

    def check_in(self, license_plate, check_in=None):
        """Check in a car if space is available."""
        if self.find_last_checkin(license_plate):
            print("Car is already checked in.")
            return False

        cur = self.db_conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM parkings WHERE car_parking_machine = ? AND check_out IS NULL",
            (self.id,),
        )
        count = cur.fetchone()[0]
        if count >= self.capacity:
            print("Parking is full.")
            return False

        check_in = check_in or datetime.now()
        parked_car = ParkedCar(license_plate=license_plate, check_in=check_in)
        self.insert(parked_car)
        print(f"Car {license_plate} checked in.")
        return True

    def check_out(self, license_plate):
        """Check out a car and calculate the parking fee."""
        row_id = self.find_last_checkin(license_plate)
        if not row_id:
            print(f"Car {license_plate} is not checked in.")
            return 0.0

        parked_car = self.find_by_id(row_id)
        parked_car.check_out = datetime.now()
        duration = (parked_car.check_out - parked_car.check_in).total_seconds() / 3600
        parked_car.parking_fee = math.ceil(duration) * self.hourly_rate
        self.update(parked_car)

        print(
            f"Car {license_plate} checked out. Fee: {parked_car.parking_fee:.2f} euro."
        )
        return parked_car.parking_fee


def main():
    """Main function to interact with the car parking system via a menu interface."""
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
                parking_machine.check_in(license_plate)

            elif choice == "O":
                license_plate = input("License: ").strip().upper()
                parking_machine.check_out(license_plate)
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
