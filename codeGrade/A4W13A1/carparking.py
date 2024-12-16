from datetime import datetime, timedelta
import math
import sqlite3
import os
import sys


def str_to_datetime(date: str) -> datetime:
    """
    Converts a string to a datetime object. Tries two conversion methods.
    """
    try:
        return datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
    except (
        ValueError
    ):  # try another format if the first did not work. Codegrade issues.
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")


class CarParkingMachine:
    """
    Handels all logic related to proccesing the parking area.

    Methods
    -------
    '__init__()'
    'check_in()'
    'check_out()'
    'add_car()'
    'del_car()'
    'get_parked_cars()'
    'get_parking_fee()'
    'get_status()'
    'reboot_self()'
    """

    def __init__(
        self, id: str = "parking_001", capacity: int = 10, hourly_rate: float = 2.5
    ) -> None:
        """
        set attributes
        also automaticly finds parked cars as defined by the logs.
        """
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.parked_cars = {}
        self.id = id
        self.db_acces = ParkingDBAcces(self)
        self.reboot_self()

    def check_in(self, license_plate: str, check_in: datetime = None) -> bool:
        """
        Handels all logic for a car entering the parking. Logs car if check in was succesfull.

        Creates new ParkedCar object and places it in the 'parked_cars' dict with
        license_plate as it's key.

        Parameters
        ----------
        'license_plate': The license plate of the car as a string.
        'check_in_time': default = system time. The time the car checks in.

        Returns
        -------
        bool: if check_in was succesfull
        """
        if not check_in:
            check_in = datetime.now()

        # check if car is allowed to check in
        if self.db_acces.find_last_checkin(license_plate):
            print("That Car is already parked somewhere")
            return False
        if len(self.parked_cars) >= self.capacity:
            return False

        # add car to database and parked cars.
        car = ParkedCar(license_plate, check_in)
        car = self.db_acces.insert(car)
        self.parked_cars[license_plate] = car

        return True

    def check_out(self, license_plate: str, check_out: datetime = None) -> float:
        """
        Checks out a car

        Removes car from 'parked_cars' and returns the parking fee.

        parameters
        ----------
        'license_plate': the license plate to check out. if no matching plate is found function returns.
        'check_out': time the car leaves garage. None will get current time.

        returns
        -------
        'fee' the cost of parking.
        OR
        nothing is returned if the license plate is not in 'parked_cars'
        """
        if check_out is None:
            check_out = datetime.now()
        if license_plate not in self.parked_cars:
            print(
                f"Error car: {license_plate} not found. origin: check_out() in CarParkingMachine"
            )
            return

        fee = self.get_parking_fee(license_plate, check_out)

        # update car object
        car = self.parked_cars[license_plate]
        car.check_out = check_out
        car.fee = fee

        # apply changed car
        self.db_acces.update(car)
        del self.parked_cars[license_plate]

        return fee

    def get_parked_cars(self) -> dict:
        """
        Returns the parked car dictionary. key = license_plate, value = ParkedCar object.
        """
        return self.parked_cars

    def get_parking_fee(self, license_plate, check_out_time=None) -> float:
        """
        Calculates the parking fee for a car

        parameters
        ----------
        'license_plate': of the car that the fee should be calculated for.
        'check_out_time': time  parking fee will be calculated for. Start time
        is stored in ParkedCar object.

        returns
        -------
        parking fee as float. No rounding
        """
        if check_out_time is None:
            check_out_time = datetime.now()

        if license_plate not in self.parked_cars:
            print(
                f"Error car: {license_plate} not found. origin: get_parking_fee() in CarParkingMachine"
            )
            return None
        car: ParkedCar = self.parked_cars[license_plate]  # gets ParkedCar object

        differance: timedelta = check_out_time - car.check_in  # calculate parking time
        hours = differance.total_seconds() / 60 / 60
        parking_hours = math.ceil(hours)

        if parking_hours < 24:  # cost rises until 24 hours plateau is reaced
            parking_fee: float = parking_hours * self.hourly_rate
        elif parking_hours >= 24:
            parking_fee: float = self.hourly_rate * 24

        return parking_fee

    def get_status(self):
        """
        Returns
        -------
        Maximum capacity: int,
        The cars in garage: int,
        All parked cars: dict key = license_plate, value = ParkedCar object,
        """
        return self.capacity, len(self.parked_cars), self.parked_cars

    def reboot_self(self):
        """
        starts reboot.
        Calls 'reboot_parked_cars' in logger.
        """
        parked_id = self.db_acces.get_not_checked_out()
        for car_id in parked_id:
            car = self.db_acces.find_by_id(car_id)
            car_plate = car.get_license_plate()
            self.parked_cars[car_plate] = car
            car.id = car_id


class ParkedCar:
    """
    One car that is somewhere in a parking area.
    """

    def __init__(self, license_plate: str, check_in: datetime = datetime.now()) -> None:
        self.license_plate = license_plate
        self.check_in: datetime = check_in
        self.id: int = None
        self.check_out: datetime = None
        self.parking_fee: float = 0

    def get_license_plate(self) -> str:
        """
        returns the cars license plate
        """
        return self.license_plate


class ParkingDBAcces:
    """
    All comunications to the DB of a CPM are handeld with this class.
    """

    def __init__(self, parent_cpm: CarParkingMachine) -> None:
        self.db_con: sqlite3.Connection = None
        self.parent_cpm = parent_cpm
        self.test_attr = 0

        self.db_con = self._get_con()

    def _get_con(self):
        """
        Make conection to the db all parkings use.
        """
        connection = sqlite3.connect(os.path.join(sys.path[0], "carparkingmachine.db"))
        connection.execute(
            """CREATE TABLE IF NOT EXISTS parkings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_parking_machine TEXT NOT NULL,
                license_plate TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT DEFAULT NULL,
                parking_fee NUMERIC DEFAULT 0
            );"""
        )
        return connection

    def _get_cursor(self):
        """
        Returns a cursor object to interact with the database.
        """
        return self.db_con.cursor()

    def find_by_id(self, id) -> ParkedCar:
        """
        Search for a parked_car in the database based on the row ID an
        return a ParkedCar object with the data

        parameters
        ----------
        'id': the primairy key to look for.

        returns
        -------
        a parked car object with all attributes of the log line.
        """

        # get row from db
        cursor = self._get_cursor()
        cursor.execute(
            """
                       SELECT *
                       FROM parkings
                       WHERE id = ?""",
            (id,),
        )
        row = cursor.fetchone()

        # turn dates into datetime objects if they exist
        id, cpm, plate, check_in, check_out, fee = row
        if check_in:
            check_in = str_to_datetime(check_in)
        if check_out:
            check_out = str_to_datetime(check_out)

        car = ParkedCar(plate, check_in)
        return car

    def find_last_checkin(self, license_plate) -> int:
        """
        Search for the last row for a given license_plate that
        has NOT checked-out yet (return row ID if found)
        """
        cursor = self._get_cursor()
        cursor.execute(
            """
                       SELECT id
                       FROM parkings
                       WHERE license_plate = ? AND check_out IS NULL
                       """,
            (license_plate,),
        )
        all_occurance = cursor.fetchall()
        try:
            last_occurance = all_occurance[-1][
                0
            ]  # fetchall returns nested list[tuple] structure
            return last_occurance
        except IndexError:
            return None

    def insert(self, parked_car: ParkedCar) -> ParkedCar:
        """
        Insert details of a created ParkedCar object and put the new row ID
        (from database) on the object, return the object with this new row ID

        parameters
        ----------
        'parked_car': parked car object that will be appended in the db.

        returns
        -------
        a parked car with ID.
        """
        car = parked_car  # Keeping method declarations intact for codegrade.

        # prep variables for sql.
        cpm = self.parent_cpm.id
        plate = car.license_plate
        check_in = car.check_in
        check_out = car.check_out
        fee = car.parking_fee

        if check_in:
            check_in = datetime.strftime(check_in, "%d-%m-%Y %H:%M:%S")
        if check_out:
            check_out = datetime.strftime(check_out, "%d-%m-%Y %H:%M:%S")

        # insert into db
        cursor = self._get_cursor()
        cursor.execute(
            """
                       INSERT INTO parkings (car_parking_machine, license_plate, check_in, check_out, parking_fee)
                       VALUES (?, ?, ?, ?, ?)""",
            (cpm, plate, check_in, check_out, fee),
        )
        self.db_con.commit()
        parked_car.id = cursor.lastrowid

        self.db_con.commit()
        return parked_car

    def update(self, parked_car: ParkedCar) -> None:
        """
        Update details of a ParkedCar object inside the database
        (update based on ParkedCar.id <- Datbase Row ID)

        parameters
        ----------
        'parked_car': car that will be writen to the database.
        """
        car = parked_car  # Keeping method declarations intact for codegrade.

        # prep variables for sql.
        car_id = car.id
        plate = car.license_plate
        check_in = car.check_in
        check_out = car.check_out
        fee = car.fee

        if check_in:
            check_in = datetime.strftime(check_in, "%d-%m-%Y %H:%M:%S")
        if check_out:
            check_out = datetime.strftime(check_out, "%d-%m-%Y %H:%M:%S")

        cursor = self._get_cursor()
        cursor.execute(
            """
                       UPDATE parkings
                       SET license_plate = ?, check_in = ?, check_out = ?, parking_fee = ?
                       WHERE id = ?""",
            (plate, check_in, check_out, fee, car_id),
        )
        self.db_con.commit()

    def get_not_checked_out(self) -> list:
        """
        Finds all cars that are checked in but not checked out at the parent parking.

        returns
        -------
        the id of the cars that aren't checked out.
        """
        print(self.parent_cpm.id)
        cursor = self._get_cursor()
        cursor.execute(
            """
                       SELECT id
                       FROM parkings
                       WHERE car_parking_machine = ? AND check_out IS NULL""",
            (self.parent_cpm.id,),
        )
        tuples_list = cursor.fetchall()
        id_list = [tup[0] for tup in tuples_list]
        return id_list


def main():
    curr_parking = CarParkingMachine("parking_001")

    running = True
    while running is True:
        print(
            """-----------------------------------
[I] Check-in car by license plate
[O] Check-out car by license plate
[Q] Quit program
[P] Print parking status (admin only)
[R] Reboots all parkings (admin only)"""
        )
        task = input("enter task: ").upper()
        match task:
            case "I":  # check in

                license_plate = input("license plate: ")
                check_in_succes = curr_parking.check_in(license_plate)

                if check_in_succes is True:  # handel result
                    print("You are checked in.")
                    print("License registered")
                else:
                    print("This garage is full.")
                    print("Capacity reached")

            case "O":  # check out
                license_plate = input("license_plate: ")
                parking_fee = curr_parking.check_out(license_plate)
                parking_fee = "%.2f" % round(parking_fee, 2)  # round parking fee

                print(f"parking fee: {parking_fee} EUR")
                print("Thank you for your stay.")

            case "Q":  # quit program

                running = False
                print("program closing")

            case "P":  # print all cars
                capactiy, amount_cars, cars = curr_parking.get_status()
                print(f"capacity:\n{capactiy}")
                print(f"cars:\n{amount_cars}")
                print(f"occupation:\n{amount_cars / capactiy * 100}%")
                print("these are all cars in this parking:")
                for car in cars:
                    print(car)

            case "R":  # reboot parked cars from logs.
                print(f"reboot started on parking {curr_parking}")
                curr_parking.reboot_self()
                print("reboot finished")

            case _:  # for undefined input
                print("input not defined. Program will coninue like normal")


if __name__ == "__main__":
    main()
