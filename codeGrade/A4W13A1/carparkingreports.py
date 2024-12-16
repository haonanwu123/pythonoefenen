from datetime import datetime
import csv
import sqlite3
import os
import sys

# parking_001,01-01-2010,01-01-2030

LOGS_PATH = "carparklog.txt"
CSV_OUTPUT = "reports.csv"


def get_cursor(db_con: sqlite3.Connection):
    """
    Returns a cursor object to interact with the database.
    """
    return db_con.cursor()


def get_con():
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


def input_str_to_date(date: str) -> datetime:
    """
    turn input string into datetime object.

    parameters
    ----------
    'date' a string in format DD-MM-YYYY

    returns
    -------
    datetime object if input string.
    """

    return datetime.strptime(date, "%d-%m-%Y")


def db_str_to_date(date: str) -> datetime:
    """
    turn input string into datetime object.

    parameters
    ----------
    'date' a string in format of logs.

    returns
    -------
    datetime object if input string.
    """
    try:
        return datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
    except (
        ValueError
    ):  # try another format if the first did not work. Codegrade issues.
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")


def cars_in_period(machine: str, start: datetime, end: datetime, return_str=False):
    """
    gets all cars between start and finish and writes them to a CSV.
    if return_str is True the fuction will return report and not write it to CSV.

    parameters
    ----------
    'machine': the CPM to check for cars.
    'start': the start of the scanned period.
    'end': the end of the scanned period.
    'return_str': if True fuction will return report. If false it is written to CSV.
    """
    report_file = f"parkedcars_{machine}_from_{start}_to_{end}.csv"
    start = input_str_to_date(start)
    end = input_str_to_date(end)
    # lines that are still WIP, key = license_plate
    lines = []
    line_format = {"plate": "None", "check_in": "None", "check_out": "None", "fee": 0}
    # None must be wrote as string because otherwise it will become an empty
    # string when writen to file.
    conn = get_con()
    cursor = get_cursor(conn)
    cursor.execute(
        """
                   SELECT *
                   FROM parkings
                   WHERE car_parking_machine = ?
                   ORDER BY check_in DESC""",
        (machine,),
    )
    log = cursor.fetchall()

    for line in log:

        time_str = line[3]
        time_date = db_str_to_date(time_str)
        if not (start <= time_date <= end):  # if time is outside reports range.
            continue

        cpm = line[1]  # if this is another CPM
        if cpm != machine:
            continue

        _, _, plate, check_in, check_out, fee = line

        new_line = line_format.copy()
        new_line["plate"] = plate
        new_line["check_in"] = check_in
        new_line["check_out"] = check_out
        new_line["fee"] = fee

        lines.append(new_line)

    if return_str is True:
        return lines

    with open(
        report_file,
        "w",
        encoding="UTF-8",
        newline="",
    ) as reports:
        writer = csv.writer(reports, delimiter=";")
        writer.writerow(("license_plate", "checked_in", "checked_out", "parking_fee"))
        for cpm in lines:
            writer.writerow(cpm.values())

    print(f"report made and placed in: {report_file}")


def fee_in_period(start: str, end: str, return_str=False):
    """
    gets total fee from all CPM's in a specified period.
    if return_str is True the fuction will return report and not write it to CSV.

    parameters
    ----------
    'start': the start of the scanned period.
    'end': the end of the scanned period.
    'return_str': if True fuction will return report. If false it is written to CSV.
    """
    report_file = f"totalfee_from_{start}_to_{end}.csv"
    start = input_str_to_date(start)
    end = input_str_to_date(end)
    all_cpm = {}
    conn = get_con()
    cursor = get_cursor(conn)
    cursor.execute(
        """
                   SELECT *
                   FROM parkings
                   WHERE check_out IS NOT NULL"""
    )

    log = cursor.fetchall()
    for line in log:

        _, cpm, plate, _, time_str, fee = line

        time_date = db_str_to_date(time_str)
        if not (start <= time_date < end):  # if time is outside reports range.
            continue

        if cpm not in all_cpm:
            all_cpm[cpm] = fee
        else:
            all_cpm[cpm] += fee

    if return_str is True:
        return all_cpm

    with open(report_file, "w", encoding="UTF-8", newline="") as reports:
        writer = csv.writer(reports, delimiter=";")
        writer.writerow(("car_parking_machine", "total_parking_fee"))
        for cpm in all_cpm.items():
            writer.writerow(cpm)

    print(f"report made and placed in: {report_file}")


def fee_from_car(license_plate: str, return_list=False):
    """
    Get all fees collected from a specified car.

    parameters
    ----------
    'license_plate': the license plate of the car to look for.
    'return_str': if True function will return result as list and not write is as csv.
    """
    conn = get_con()
    cursor = get_cursor(conn)
    cursor.execute(
        """
                   SELECT car_parking_machine, check_in, check_out, parking_fee
                   FROM parkings
                   WHERE license_plate = ? AND parking_fee != 0
                   ORDER BY check_in DESC""",
        (license_plate,),
    )
    fee_lines = cursor.fetchall()

    if return_list is True:
        return fee_lines

    report_file = f"all_parkings_for_{license_plate}.csv"
    with open(report_file, "w", encoding="UTF-8", newline="") as reports:
        writer = csv.writer(reports, delimiter=";")
        writer.writerow(("car_parking_machine", "check_in", "check_out", "parking_fee"))
        for line in fee_lines:
            writer.writerow(line)


def main():
    running = True
    while running is True:
        print(
            "[P] Report all parked cars during a parking period for a specific parking machine"
        )
        print(
            "[F] Report total collected parking fee during a parking period for all parking machines"
        )
        print(
            "[C] Report all complete parkings over all parking machines for a specific car"
        )
        print("[Q] Quit program")
        task = input("Task: ").upper()
        match task:
            case "P":
                user_inp = input("Start and end: ")
                user_inp = user_inp.split(",")
                cars_in_period(user_inp[0], user_inp[1], user_inp[2])
            case "F":
                user_inp = input("Start and end: ")
                user_inp = user_inp.split(",")
                fee_in_period(user_inp[0], user_inp[1])
            case "C":
                user_inp = input("Car,start,end: ")
                user_inp = user_inp.split(",")
                fee_from_car(*user_inp)
            case "Q":
                running = False


if __name__ == "__main__":
    main()
