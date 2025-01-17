from datetime import datetime, date
from catch import Catch
import sqlite3
import os
import sys


class Contestant:

    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        classification: str,
        date_of_birth: datetime,
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.classification = classification
        self.date_of_birth = date_of_birth.date()

    def get_age(self, at_date=date.today()) -> int:
        """Returns the age of the contestant as of the specified date."""
        age = at_date.year = self.date_of_birth.year
        if at_date.month < self.date_of_birth.month or (
            at_date.month == self.date_of_birth.month
            and at_date.day < self.date_of_birth.day
        ):
            age -= 1
        return age

    def get_catches(self) -> tuple[Catch, ...]:
        """Returns a tuple of all catches for this contestant."""
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Catches WHERE contestant_id = ?", (self.id,))
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
