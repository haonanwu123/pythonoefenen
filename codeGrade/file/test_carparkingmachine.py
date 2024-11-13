import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from codeGrade.A3W09A1 import ParkedCar, CarParkingMachine
from datetime import datetime, timedelta


# Test for a normal check-in with correct result (True)
def test_check_in_capacity_normal():
    cpm = CarParkingMachine(capacity=2, hourly_rate=4.0)
    assert cpm.check_in("AB-123-CD") == True
    assert "AB-123-CD" in cpm.parked_cars


# Test for a check-in with maximum capacity reached (False)
def test_check_in_capacity_reached():
    cpm = CarParkingMachine(capacity=1, hourly_rate=4.0)
    cpm.check_in("AB-123-CD")
    assert cpm.check_in("AB-456-CD") == False


# Test for checking the correct parking fees
def test_parking_fee():
    cpm = CarParkingMachine(hourly_rate=4.0)

    # Assert that parking time 2h10m, gives correct parking fee
    cpm.check_in("AB-123-CD", datetime.now() - timedelta(hours=2, minutes=10))
    assert cpm.get_parking_fee("AB-123-CD") == 12.0  # Rounding up to 3 hours

    # Assert that parking time 24h, gives correct parking fee
    cpm.check_in("AB-456-CD", datetime.now() - timedelta(hours=24))
    assert cpm.get_parking_fee("AB-456-CD") == 24 * 4.0

    # Assert that parking time 30h == 24h max, gives correct parking fee
    cpm.check_in("AB-789-CD", datetime.now() - timedelta(hours=30))
    assert cpm.get_parking_fee("AB-789-CD") == 24 * 4.0


# Test for validating check-out behaviour
def test_check_out():
    cpm = CarParkingMachine(hourly_rate=4.0)
    cpm.check_in("AB-123-CD", datetime.now() - timedelta(hours=2))

    # Assert that {license_plate} is in parked_cars
    assert "AB-123-CD" in cpm.parked_cars

    # Assert that correct parking fee is provided when checking-out {license_plate}
    fee = cpm.check_out("AB-123-CD")
    assert fee == 12.0

    # Aseert that {license_plate} is no longer in parked_cars
    assert "AB-123-CD" not in cpm.parked_cars


def main():
    test_check_in_capacity_normal()
    test_check_in_capacity_reached()
    test_parking_fee()
    test_check_out()


if __name__ == "__main__":
    main()
