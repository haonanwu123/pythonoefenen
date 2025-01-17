from catch import Catch
from datetime import datetime
import os
import sys
import sqlite3


class Fish:

    def __init__(
        self, taxon_key: int, species: str, scientific_name: str, kingdom: str
    ) -> None:
        self.taxon_key = taxon_key
        self.species = species
        self.scientific_name = scientific_name
        self.kingdom = kingdom

    def get_catches(self) -> tuple[Catch, ...]:
        """Return a tuple of all catches taht contains this kind of fish"""
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Catches WHERE fish_id = ?", (self.taxon_key,))
        rows = dbc.fetchall()

        catches = []
        if rows:
            for row in rows:
                catch = Catch(
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
                catches.append(catch)
            return tuple(catches)
        else:
            return None

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]),
        )
