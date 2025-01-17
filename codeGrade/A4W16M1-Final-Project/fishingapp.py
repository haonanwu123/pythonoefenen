import json
import sqlite3
import os
import sys
from datetime import datetime
from contestant import Contestant
from fish import Fish
from catch import Catch


def has_data_been_imported(db_connection) -> bool:
    """Checks if the data has already been imported by looking for an existing catch."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Catches")
    count = cursor.fetchone()[0]
    return count > 0


def import_data_from_json(json_file_path, db_connection):
    """Imports data from the provided JSON file into the catches.db database."""
    with open(json_file_path, "r", encoding="utf-8") as file:
        catches_data = json.load(file)

    cursor = db_connection.cursor()
    for entry in catches_data:
        # fish data
        fish_data = entry["fish"]
        fish = Fish(
            fish_data["taxon_key"],
            fish_data["species"],
            fish_data["scientific_name"],
            fish_data["kingdom"],
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO Fishes (taxon_key, species, scientific_name, kingdom)
            VALUES (?, ?, ?, ?)
        """,
            (fish.taxon_key, fish.species, fish.scientific_name, fish.kingdom),
        )

        # contestant data
        contestant_data = entry["candidate"]
        contestant = Contestant(
            contestant_data["id"],
            contestant_data["first_name"],
            contestant_data["last_name"],
            contestant_data["classification"],
            datetime.strptime(contestant_data["date_of_birth"], "%Y-%m-%d"),
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO Contestants (id, first_name, last_name, classification, date_of_birth)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                contestant.id,
                contestant.first_name,
                contestant.last_name,
                contestant.classification,
                contestant.date_of_birth,
            ),
        )

        # catch data
        from typing import List

        coordinate: str = entry["coordinate"]
        coordinate_list: List[str] = coordinate.split(",")

        latitude, longitude = map(float, coordinate_list)

        if len(coordinate_list) != 2:
            raise ValueError(f"Invalid coordinate format: {coordinate}")

        latitude: float = float(coordinate_list[0])
        longitude: float = float(coordinate_list[1])

        catch = Catch(
            id=None,  # Assuming auto-increment in the database
            fish=fish_data["taxon_key"],
            contestant=contestant_data["id"],
            caught_at=datetime.strptime(entry["datetime"], "%Y-%m-%d %H:%M:%S"),
            latitude=latitude,
            longitude=longitude,
            country_code=entry["country_code"],
            weight=entry["weight"],
            length=entry["length"],
        )

        cursor.execute(
            """
            INSERT INTO Catches (fish_id, contestant_id, caught_at, latitude, longitude, country_code, weight, length)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                catch.fish,
                catch.contestant,
                catch.caught_at,
                catch.latitude,
                catch.longitude,
                catch.country_code,
                catch.weight,
                catch.length,
            ),
        )

    db_connection.commit()


def main():
    db_path = os.path.join(sys.path[0], "catches.db")
    json_file_path = os.path.join(sys.path[0], "catches.json")

    print(f"Database path: {db_path}")

    db_connection = sqlite3.connect(db_path)
    if not has_data_been_imported(db_connection):
        print("Importing data...")
        import_data_from_json(json_file_path, db_connection)
        print("Data import completed!")
    else:
        print("Data has already been imported.")


if __name__ == "__main__":
    main()
