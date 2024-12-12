import sqlite3
import os
import csv
from datetime import datetime


def report_parked_cars(machine_id, from_date, to_date):
    conn = sqlite3.connect(
        os.path.join(os.path.dirname(__file__), "carparkingmachine.db")
    )
    cur = conn.cursor()
    from_date = datetime.strptime(from_date, "%d-%m-%Y")
    to_date = datetime.strptime(to_date, "%d-%m-%Y")

    cur.execute(
        """
        SELECT license_plate, check_in, check_out, parking_fee
        FROM parkings
        WHERE car_parking_machine = ? AND date(check_in) BETWEEN ? AND ?
        """,
        (machine_id, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")),
    )

    rows = cur.fetchall()
    output_file = f'parkedcars_{machine_id}_from_{from_date.strftime("%d-%m-%Y")}_to_{to_date.strftime("%d-%m-%Y")}.csv'
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["license_plate", "check_in", "check_out", "parking_fee"])
        for row in rows:
            writer.writerow(row)
    print(f"Report saved to {output_file}")


def report_total_fees(from_date, to_date):
    conn = sqlite3.connect(
        os.path.join(os.path.dirname(__file__), "carparkingmachine.db")
    )
    cur = conn.cursor()
    from_date = datetime.strptime(from_date, "%d-%m-%Y")
    to_date = datetime.strptime(to_date, "%d-%m-%Y")

    cur.execute(
        """
        SELECT car_parking_machine, SUM(parking_fee)
        FROM parkings
        WHERE date(check_out) BETWEEN ? AND ?
        GROUP BY car_parking_machine
        """,
        (from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")),
    )

    rows = cur.fetchall()
    output_file = f'totalfees_from_{from_date.strftime("%d-%m-%Y")}_to_{to_date.strftime("%d-%m-%Y")}.csv'
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["car_parking_machine", "total_parking_fee"])
        for row in rows:
            writer.writerow(row)
    print(f"Total fees report saved to {output_file}")


def main():
    while True:
        print(
            "[P] Report all parked cars during a parking period for a specific parking machine\n"
            "[F] Report total collected parking fee during a parking period for all parking machines\n"
            "[Q] Quit program"
        )
        choice = input("> ").strip().upper()

        if choice == "Q":
            print("Exiting program.")
            break
        elif choice == "P":
            inputs = input(
                "Enter machine ID, from date (DD-MM-YYYY), to date (DD-MM-YYYY): "
            ).strip()
            machine_id, from_date, to_date = map(str.strip, inputs.split(","))
            report_parked_cars(machine_id, from_date, to_date)
        elif choice == "F":
            inputs = input(
                "Enter from date (DD-MM-YYYY), to date (DD-MM-YYYY): "
            ).strip()
            from_date, to_date = map(str.strip, inputs.split(","))
            report_total_fees(from_date, to_date)
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
