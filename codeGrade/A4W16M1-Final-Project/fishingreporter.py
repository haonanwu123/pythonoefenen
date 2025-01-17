from datetime import datetime, date
from catch import Catch
from fish import Fish
from contestant import Contestant
import os
import sys
import sqlite3
import csv


class Reporter:
    def total_amount_of_fish(self) -> int:
        """
        Returns the total number of fish recorded in the database.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT COUNT(*) FROM Fishes")
        fish_amount = dbc.fetchone()
        return fish_amount[0] if fish_amount else 0

    def biggest_catch(self) -> Catch:
        """
        Returns the catch with the highest weight recorded in the database.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Catches ORDER BY weight DESC LIMIT 1")
        row = dbc.fetchone()
        if row:
            return Catch(
                id=row[0],
                fish=row[1],
                contestant=row[2],
                caught_at=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                latitude=row[4],
                longitude=row[5],
                country_code=row[6],
                weight=row[7],
                length=row[8],
            )
        return None

    def longest_and_shortest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the longest and shortest catches recorded in the database.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Catches ORDER BY length DESC LIMIT 1")
        longest = dbc.fetchone()

        dbc.execute("SELECT * FROM Catches ORDER BY length ASC LIMIT 1")
        shortest = dbc.fetchone()

        longest_catch = (
            Catch(
                id=longest[0],
                fish=longest[1],
                contestant=longest[2],
                caught_at=datetime.strptime(longest[3], "%Y-%m-%d %H:%M:%S"),
                latitude=longest[4],
                longitude=longest[5],
                country_code=longest[6],
                weight=longest[7],
                length=longest[8],
            )
            if longest
            else None
        )

        shortest_catch = (
            Catch(
                id=shortest[0],
                fish=shortest[1],
                contestant=shortest[2],
                caught_at=datetime.strptime(shortest[3], "%Y-%m-%d %H:%M:%S"),
                latitude=shortest[4],
                longitude=shortest[5],
                country_code=shortest[6],
                weight=shortest[7],
                length=shortest[8],
            )
            if shortest
            else None
        )

        return (longest_catch, shortest_catch)

    def heaviest_and_lightest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the heaviest and lightest catches by weight recorded in the database.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Catches ORDER BY weight DESC LIMIT 1")
        heaviest = dbc.fetchone()

        dbc.execute("SELECT * FROM Catches ORDER BY weight ASC LIMIT 1")
        lightest = dbc.fetchone()

        heaviest_catch = (
            Catch(
                id=heaviest[0],
                fish=heaviest[1],
                contestant=heaviest[2],
                caught_at=datetime.strptime(heaviest[3], "%Y-%m-%d %H:%M:%S"),
                latitude=heaviest[4],
                longitude=heaviest[5],
                country_code=heaviest[6],
                weight=heaviest[7],
                length=heaviest[8],
            )
            if heaviest
            else None
        )

        lightest_catch = (
            Catch(
                id=lightest[0],
                fish=lightest[1],
                contestant=lightest[2],
                caught_at=datetime.strptime(lightest[3], "%Y-%m-%d %H:%M:%S"),
                latitude=lightest[4],
                longitude=lightest[5],
                country_code=lightest[6],
                weight=lightest[7],
                length=lightest[8],
            )
            if lightest
            else None
        )

        return (heaviest_catch, lightest_catch)

    def contestant_with_most_catches(self) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the most catches recorded in the database.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Catches")
        rows = dbc.fetchall()

        if not rows:
            return ()

        catch_count = {}
        for row in rows:
            contestant = row[2]
            contestant_id = contestant
            catch_count[contestant_id] = catch_count.get(contestant_id, 0) + 1

        max_catches = max(catch_count.values())

        top_contestant_ids = [
            contestant_id
            for contestant_id, count in catch_count.items()
            if count == max_catches
        ]

        contestants = []
        for contestant_id in top_contestant_ids:
            temp_catch = Catch(
                id=None,
                fish=None,
                contestant=contestant_id,
                caught_at=None,
                latitude=None,
                longitude=None,
                country_code=None,
                weight=None,
                length=None,
            )
            contestant = temp_catch.get_contestant()
            if contestant:
                contestants.append(contestant)

        return tuple(contestants)

    def fish_with_most_catches(self) -> tuple[Fish, ...]:
        """
        Returns a tuple containing the fish species with the most catches recorded in the database.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Catches")
        rows = dbc.fetchall()

        if not rows:
            return ()

        catched_fishes_count = {}
        for row in rows:
            fish = row[1]
            fish_id = fish
            catched_fishes_count[fish_id] = catched_fishes_count.get(fish_id, 0) + 1

        max_catched = max(catched_fishes_count.values())

        top_fish_ids = [
            fish_id
            for fish_id, count in catched_fishes_count.items()
            if count == max_catched
        ]

        fishes = []
        for fish_id in top_fish_ids:
            temp_catch = Catch(
                id=None,
                fish=fish_id,
                contestant=None,
                caught_at=None,
                latitude=None,
                longitude=None,
                country_code=None,
                weight=None,
                length=None,
            )
            fish = temp_catch.get_fish()
            if fish:
                fishes.append(fish)

        return tuple(fishes)

    def contestant_with_first_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the first catch of a specified fish type.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Fishes WHERE species = ?", (species,))
        fish_row = dbc.fetchone()
        if not fish_row:
            return ()

        fish = Fish(
            taxon_key=fish_row[0],
            species=fish_row[1],
            scientific_name=fish_row[2],
            kingdom=fish_row[3],
        )

        catches = fish.get_catches()
        if not catches:
            return ()

        first_catch = min(catches, key=lambda catch: catch.caught_at)

        contestant = first_catch.get_contestant()
        return (contestant,) if contestant else ()

    def contestant_with_last_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the last catch of a specified fish type.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Fishes WHERE species = ?", (species,))
        fish_row = dbc.fetchone()
        if not fish_row:
            return ()

        fish = Fish(
            taxon_key=fish_row[0],
            species=fish_row[1],
            scientific_name=fish_row[2],
            kingdom=fish_row[3],
        )

        catches = fish.get_catches()
        if not catches:
            return ()

        first_catch = max(catches, key=lambda catch: catch.caught_at)

        contestant = first_catch.get_contestant()
        return (contestant,) if contestant else ()

    def contestants_fished_between(
        self, fish: Fish, start: date, end: date, to_csv: bool = False
    ) -> tuple[Contestant, ...]:
        """
        If to_csv is False, returns a tuple containing the contestants who fished a specified fish species between two dates.
        If to_csv is True, the results are written to a CSV file.
        """
        catches = fish.get_catches()

        if not catches:
            return ()

        seen_ids = set()
        unique_contestants = []

        for catch in catches:
            contestant = catch.get_contestant()
            if (
                contestant
                and catch.fish == fish.taxon_key
                and start <= catch.caught_at.date() <= end
            ):
                if contestant.id not in seen_ids:
                    seen_ids.add(contestant.id)
                    unique_contestants.append(contestant)

        unique_contestants.sort(key=lambda contestant: str(contestant.id))

        if to_csv:
            csv_file = f"Contestant fishing between {start} and {end}.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                wirter = csv.writer(file)
                wirter.writerow(
                    ["id", "first_name", "last_name", "date_of_birth", "classification"]
                )

                for contestant in unique_contestants:
                    wirter.writerow(
                        [
                            contestant.id,
                            contestant.first_name,
                            contestant.last_name,
                            contestant.date_of_birth.strftime("%Y-%m-%d"),
                            contestant.classification,
                        ]
                    )
                print(f"Results written to {csv_file}")
        return tuple(unique_contestants)

    def fish_caught_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Fish, ...]:
        """
        If to_csv is False, returns a tuple containing the fish species caught in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()

        dbc.execute(
            """
            SELECT DISTINCT f.taxon_key, f.species, f.scientific_name, f.kingdom
            FROM Catches c
            JOIN Fishes f ON c.fish_id = f.taxon_key
            WHERE c.country_code = ?
            ORDER BY f.taxon_key
        """,
            (country_code,),
        )

        rows = dbc.fetchall()

        if not rows:
            return ()

        fishes = []
        for row in rows:
            fishes.append(
                Fish(
                    taxon_key=row[0],
                    species=row[1],
                    scientific_name=row[2],
                    kingdom=row[3],
                )
            )

        if to_csv:
            csv_file = f"Fishes in country {country_code}.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["taxon_key", "species", "kingdom", "scientific_name"])
                for fish in fishes:
                    writer.writerow(
                        [
                            fish.taxon_key,
                            fish.species,
                            fish.kingdom,
                            fish.scientific_name,
                        ]
                    )

                print(f"Results written to {csv_file}")

        return tuple(fishes)

    def contestants_fished_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Contestant, ...]:
        """
        If to_csv is False, returns a tuple containing the contestants who fished in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()

        dbc.execute(
            """
            SELECT DISTINCT co.id, co.first_name, co.last_name, co.classification, co.date_of_birth
            FROM Catches c
            JOIN Contestants co ON c.contestant_id = co.id
            WHERE c.country_code = ?
            ORDER BY co.id
        """,
            (country_code,),
        )

        rows = dbc.fetchall()

        if not rows:
            return ()

        contestants = []

        for row in rows:
            contestants.append(
                Contestant(
                    id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    classification=row[3],
                    date_of_birth=datetime.strptime(row[4], "%Y-%m-%d"),
                )
            )

        if to_csv:
            csv_file = f"Contestants fished in country {country_code}.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["id", "first_name", "last_name", "date_of_birth", "classification"]
                )
                for contestant in contestants:
                    writer.writerow(
                        [
                            contestant.id,
                            contestant.first_name,
                            contestant.last_name,
                            contestant.date_of_birth,
                            contestant.classification,
                        ]
                    )

                print(f"Results written to {csv_file}")

        return tuple(contestants)
