from carparking import CarParkingMachine
import carparkingreports as reporter
from datetime import datetime, timedelta
import time


# Test for a normal check-in with correct result (True)
def test_check_in_capacity_normal():
    parking = CarParkingMachine("parking_003", 5)
    parking.check_in("11-AAA-11")
    assert "11-AAA-11" in parking.parked_cars
    print("Good: normal check_in")


# Test for a check-in with maximum capacity reached (False)
def test_check_in_capacity_reached():
    parking = CarParkingMachine("parking_004", 5)
    parking.check_in("11-VVV-11")
    parking.check_in("22-BBB-22")
    parking.check_in("22-CCC-66")
    parking.check_in("22-DDD-22")
    assert parking.check_in("44-EEE-88") is True
    print("Good: last car under capacity can check in")
    assert parking.check_in("22-FFF-22") is False
    print("Good: first car over capactiy can't check in")


# Test extra checks for to prevent errors in carparking.
def test_safety_checks():
    parking = CarParkingMachine("parking_004", 5)
    parking.check_in("11-AAA-1")
    assert parking.check_in("11-AAA-1") is False
    print("Good: two cars with same number plate can't check in")
    assert parking.get_parking_fee("888888-AAAAAAA-777777") == None
    print("Good: non existent number plate isn't charged")


# Test for checking the correct parking fees
def test_parking_fee():
    parking = CarParkingMachine("parking_005",5 , hourly_rate=2)
    base_time = datetime.now()
    parking.check_in("11-ZZZ-1", base_time - timedelta(minutes=40))
    assert parking.get_parking_fee("11-ZZZ-1") == 2
    print("Good: fee for parking 40 minutes")
    parking.check_in("11-AAA-1", base_time - timedelta(hours=2, minutes=10))
    assert parking.get_parking_fee("11-AAA-1") == 6
    print("Good: fee for parking 2:10 hours")
    parking.check_in("11-BBB-1", base_time - timedelta(hours=24))
    assert parking.get_parking_fee("11-BBB-1") == 48
    print("Good: fee for parking 24 hours")
    parking.check_in("11-CCC-1", base_time - timedelta(hours=30))
    assert parking.get_parking_fee("11-CCC-1") == 48
    print("Good: fee for parking 30 hours")


# Test for validating check-out behaviour
def test_check_out():
    parking = CarParkingMachine("parking_006", 5, hourly_rate=10)
    parking.check_in("11-NLE-22", datetime(2020, 2, 2 , 1, 1, 1,))
    assert "11-NLE-22" in parking.parked_cars
    print("Good: car is added to parked_car dict")
    #time.sleep(1)
    assert parking.check_out("11-NLE-22", datetime(2020, 2, 2 , 1, 10, 1)) == 10
    print("Good: correct fee is returend by check_out()")
    parking.check_out("11-NLE-22", datetime(2020, 2, 2 , 1, 10, 1))
    assert "11-NLE-22" not in parking.parked_cars

# test reboot, reboots parking from test: 'test_check_in_capacity_normal()'
def test_reboot():
    def setup():
        parking1 = CarParkingMachine("parking_011",5)
        parking1.check_in("tyty")

    def test_adding():  # functions cause program to need to reboot from memory
        parking1 = CarParkingMachine("parking_011", 5)
        assert "tyty" in parking1.parked_cars
        parking1.check_out("tyty")

    def test_removing():
        parking1 = CarParkingMachine("parking_011", 5)
        assert "tyty" not in parking1.parked_cars
        parking2 = CarParkingMachine("parking_012", 5)
        assert parking2.check_in("tyty") is True
    setup()
    test_adding()
    test_removing()
    print("Good: saving and loading")

# test is report can be made on the cpm from test check_out
def test_reports():
    parking_010 = CarParkingMachine("parking_010", hourly_rate=10)
    parking_010.check_in("YYYTTT" , datetime(1060, 4, 4, 4, 4, 4))
    parking_010.check_out("YYYTTT", datetime(1060, 4, 4, 4, 10, 4))

    report = reporter.cars_in_period("parking_010", "03-04-1060", "05-04-1060", return_str=True)
    assert report == [{'plate': 'YYYTTT', 'check_in': '04-04-1060 04:04:04', 'check_out': '04-04-1060 04:10:04', 'fee': 10.0}]
    report = reporter.fee_in_period("03-04-1060", "05-04-1060", return_str=True)
    assert report == {'parking_010': 10.0}
    print("Good: reports")

def main():
    test_check_in_capacity_normal()
    test_check_in_capacity_reached()
    test_safety_checks()
    test_parking_fee()
    test_check_out()
    test_reboot()
    test_reports()
    print("Unit test over")


if __name__ == '__main__':
    main()