import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from codeGrade.A3W10A1 import ParkedCar, CarParkingMachine, CarParkingLogger
from datetime import datetime, timedelta


# Test for a normal check-in with correct result (True)
def test_check_in_capacity_normal():
    cpm = CarParkingMachine(
        id="TestCPM", capacity=10, hourly_rate=4.0
    )  # Provide an 'id'
    assert cpm.check_in("AB-123-CD") == True
    assert "AB-123-CD" in cpm.parked_cars


# Test for a check-in with maximum capacity reached (False)
def test_check_in_capacity_reached():
    cpm = CarParkingMachine(
        id="TestCPM", capacity=1, hourly_rate=4.0
    )  # Provide an 'id'
    cpm.check_in("AB-123-CD")
    assert cpm.check_in("AB-456-CD") == False


# Test for checking the correct parking fees
def test_parking_fee():
    cpm = CarParkingMachine(id="TestCPM", hourly_rate=4.0)  # Provide an 'id'

    # Assert that parking time 1h, gives correct parking fee
    cpm.check_in("AB-123-CD", datetime.now())
    assert cpm.get_parking_fee("AB-123-CD") == 4.0  # Rounding up to 1 hours


# Test for validating check-out behaviour
def test_check_out():
    cpm = CarParkingMachine(id="TestCPM", hourly_rate=4.0)  # Provide an 'id'
    cpm.check_in("AB-123-CD", datetime.now())

    # Assert that {license_plate} is in parked_cars
    assert "AB-123-CD" in cpm.parked_cars

    # Assert that correct parking fee is provided when checking-out {license_plate}
    fee = cpm.check_out("AB-123-CD")
    assert fee == 4.0

    # Assert that {license_plate} is no longer in parked_cars
    assert "AB-123-CD" not in cpm.parked_cars


# Test for re-checking a car that's already checked in
def test_re_check_in():
    cpm = CarParkingMachine(
        id="TestCPM", capacity=2, hourly_rate=4.0
    )  # Provide an 'id'
    cpm.check_in("AB-123-CD")

    # Assert re-checking the same car returns True and does not duplicate
    assert cpm.check_in("AB-123-CD") == True


# Test for logging behaviour in the CarParkingLogger
def test_logging_behaviour():
    log_file = "test_log.txt"

    # Ensure we clean up any old log file before running the test
    if os.path.exists(log_file):
        os.remove(log_file)

    # Initialize the parking machine with a custom logger pointing to our test log file
    cpm = CarParkingMachine(id="TestCPM", hourly_rate=3.0)  # Provide an 'id'
    cpm.logger = CarParkingLogger(cpm.id, log_file)

    # Perform some actions
    cpm.check_in("LOG-123")
    cpm.check_out("LOG-123")

    # Validate the log file
    with open(log_file, "r") as f:
        lines = f.readlines()

    # Ensure there are exactly 2 log entries
    assert len(lines) == 2
    assert "action=check-in" in lines[0]
    assert "action=check-out" in lines[1]

    # Clean up
    os.remove(log_file)


# Test for empty parking machine
def test_empty_machine():
    cpm = CarParkingMachine(
        id="TestCPM", capacity=10, hourly_rate=2.5
    )  # Provide an 'id'

    # Attempting to check-out a car that doesn't exist
    fee = cpm.check_out("NO-CAR")
    assert fee == 0.0


def main():
    test_check_in_capacity_normal()
    test_check_in_capacity_reached()
    test_parking_fee()
    test_check_out()
    test_re_check_in()
    test_logging_behaviour()
    test_empty_machine()
    print("All tests passed!")


if __name__ == "__main__":
    main()
