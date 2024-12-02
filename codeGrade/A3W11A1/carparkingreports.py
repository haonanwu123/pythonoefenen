import csv
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def report_parked_cars(machine_id: str, from_date: str, to_date: str):
    """
    Generates a CSV report of all parked cars during a specified period for a specific parking machine.
    """
    log_file_path = os.path.join(BASE_DIR, "carparklog.txt")
    from_date = datetime.strptime(from_date, "%d-%m-%Y")
    to_date = datetime.strptime(to_date, "%d-%m-%Y")
    output_file = os.path.join(
        BASE_DIR,
        f"parkedcars_{machine_id}_from_{from_date.strftime('%d-%m-%Y')}_to_{to_date.strftime('%d-%m-%Y')}.csv",
    )

    if not os.path.exists(log_file_path):
        print(f"Log file {log_file_path} does not exist!")
        return

    # Temporary storage for parked car data
    parked_cars = {}

    with open(log_file_path, "r") as file:
        for line in file:
            parts = line.strip().split(";")
            if len(parts) < 5:
                continue

            # Parse the log line
            timestamp = parts[0]
            log_date = datetime.strptime(timestamp.split(" ")[0], "%d-%m-%Y")
            cpm_name = parts[1].split("=")[1]
            license_plate = parts[2].split("=")[1]
            action = parts[3].split("=")[1]
            parking_fee = (
                float(parts[4].split("=")[1]) if "parking_fee" in parts[4] else 0.0
            )

            # Filter by machine ID and date range
            if (
                cpm_name.lower() == machine_id.lower()
                and from_date <= log_date <= to_date
            ):
                if license_plate not in parked_cars:
                    parked_cars[license_plate] = []

                parked_cars[license_plate].append((action, timestamp, parking_fee))

    # Write report to CSV
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["license_plate", "checked_in", "checked_out", "parking_fee"])

        for license_plate, events in parked_cars.items():
            check_in = None
            for action, timestamp, fee in events:
                if action == "check-in":
                    check_in = timestamp
                elif action == "check-out" and check_in:
                    writer.writerow([license_plate, check_in, timestamp, round(fee, 2)])
                    check_in = None

            # Handle cases where a car is still parked (no check-out)
            if check_in:
                writer.writerow([license_plate, check_in, "None", 0.0])

    print(f"Report saved to {output_file}")


def report_total_fees(from_date: str, to_date: str):
    """
    Generates a CSV report of total collected parking fees during a specified period for all machines.
    """
    log_file_path = os.path.join(BASE_DIR, "carparklog.txt")
    if not os.path.exists(log_file_path):
        print(f"Log file {log_file_path} does not exist!")
        return

    from_date = datetime.strptime(from_date, "%d-%m-%Y")
    to_date = datetime.strptime(to_date, "%d-%m-%Y")
    output_file = os.path.join(
        BASE_DIR,
        f"totalfee_from_{from_date.strftime('%d-%m-%Y')}_to_{to_date.strftime('%d-%m-%Y')}.csv",
    )

    fees_by_machine = {}

    # Read log file and compute total fees per machine
    with open(log_file_path, "r") as file:
        for line in file:
            parts = line.strip().split(";")
            if len(parts) < 5:
                continue  # Skip invalid log entries

            # Parse the log entry
            timestamp, cpm_name, _, action, fee_part = parts
            log_date = datetime.strptime(timestamp.split(" ")[0], "%d-%m-%Y")
            if from_date <= log_date <= to_date and "check-out" in action:
                machine_name = cpm_name.split("=")[1]
                fee = float(fee_part.split("=")[1])
                fees_by_machine[machine_name] = (
                    fees_by_machine.get(machine_name, 0) + fee
                )

    # Write to the output CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["car_parking_machine", "total_parking_fee"])
        for machine, total_fee in fees_by_machine.items():
            writer.writerow([machine, round(total_fee, 2)])

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
            print(f"Report generated for {machine_id}!")
        elif choice == "F":
            inputs = input(
                "Enter from date (DD-MM-YYYY), to date (DD-MM-YYYY): "
            ).strip()
            from_date, to_date = map(str.strip, inputs.split(","))
            report_total_fees(from_date, to_date)
            print("Total fees report generated!")
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
