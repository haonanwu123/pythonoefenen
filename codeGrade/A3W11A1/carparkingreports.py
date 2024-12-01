import csv
from datetime import datetime
from carparking import CarParkingLogger


def report_parked_cars(machine_id: str, from_date: str, to_date: str):
    """
    Generates a CSV report of all parked cars during a specified period for a specific parking machine.
    """
    logger = CarParkingLogger(machine_id)
    from_date = datetime.strptime(from_date, "%d-%m-%Y")
    to_date = datetime.strptime(to_date, "%d-%m-%Y")

    output_file = f"{machine_id}_parked_cars_report.csv"
    with open(logger.log_file, "r") as file, open(
        output_file, "w", newline=""
    ) as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["license_plate", "check-in", "check-out", "parking_fee"])
        for line in file:
            parts = line.strip().split(";")
            if len(parts) < 5:
                continue
            timestamp, cpm_name, license_plate, action, fee_part = parts
            log_date = datetime.strptime(timestamp.split(" ")[0], "%d-%m-%Y")
            if (
                machine_id.lower() == cpm_name.split("=")[1].lower()
                and from_date <= log_date <= to_date
            ):
                license_plate = license_plate.split("=")[1]
                action = action.split("=")[1]
                fee = fee_part.split("=")[1] if "parking_fee" in fee_part else ""
                writer.writerow(
                    [license_plate, timestamp if action == "check-in" else "", "", fee]
                )


def report_total_fees(from_date: str, to_date: str):
    """
    Generates a CSV report of total collected parking fees during a specified period for all machines.
    """
    log_file = "carparklog.txt"
    from_date = datetime.strptime(from_date, "%d-%m-%Y")
    to_date = datetime.strptime(to_date, "%d-%m-%Y")

    output_file = "total_fees_report.csv"
    fees_by_machine = {}
    with open(log_file, "r") as file:
        for line in file:
            parts = line.strip().split(";")
            if len(parts) < 5:
                continue
            timestamp, cpm_name, _, action, fee_part = parts
            log_date = datetime.strptime(timestamp.split(" ")[0], "%d-%m-%Y")
            if from_date <= log_date <= to_date and action.split("=")[1] == "check-out":
                machine_name = cpm_name.split("=")[1]
                fee = float(fee_part.split("=")[1])
                fees_by_machine[machine_name] = (
                    fees_by_machine.get(machine_name, 0) + fee
                )

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["car_parking_machine", "total_parking_fee"])
        for machine, fee in fees_by_machine.items():
            writer.writerow([machine, round(fee, 2)])


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
