from datetime import datetime
import sqlite3
import os
import sys


class Catch:

    def __init__(
        self,
        id: int,
        fish: int,
        contestant: str,
        caught_at: datetime,
        latitude: float,
        longitude: float,
        country_code: str,
        weight: float,
        length: float,
    ) -> None:
        self.id = id
        self.fish = fish
        self.contestant = contestant
        self.caught_at = caught_at
        self.latitude = latitude
        self.longitude = longitude
        self.country_code = country_code
        self.weight = weight
        self.length = length

    def get_contestant(self):
        from contestant import Contestant

        """Returns the contestant who caught the fish in this catch."""
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Contestants WHERE id = ?", (self.contestant,))
        row = dbc.fetchone()

        if row:
            return Contestant(
                id=row[0],
                first_name=row[1],
                last_name=row[2],
                classification=row[3],
                date_of_birth=datetime.strptime(row[4], "%Y-%m-%d"),
            )
        else:
            return None

    def get_fish(self):
        from fish import Fish

        """Returns the fish caught in this catch."""
        db_connection = sqlite3.connect(os.path.join(sys.path[0], "catches.db"))
        dbc = db_connection.cursor()
        dbc.execute("SELECT * FROM Fishes WHERE taxon_key = ?", (self.fish,))
        row = dbc.fetchone()

        if row:
            return Fish(
                taxon_key=row[0], species=row[1], scientific_name=row[2], kingdom=row[3]
            )
        else:
            return None

    def get_weight_in_local_units(self) -> str:
        """Returns the mass of the catch in the local unit of mass based on the country code."""
        conversions = {
            "US": ("Pound", 453.592, "Ounce", 28.3495),
            "LR": ("Pound", 453.592, "Ounce", 28.3495),
            "MM": ("Viss", 1600, "Pound", 453.592),
            "CA": ("Pound", 453.592, "Ounce", 28.3495),
            "GB": ("Stone", 6350.29, "Pound", 453.592),
            "AU": ("Pound", 453.592, "Ounce", 28.3495),
            "BS": ("Pound", 453.592, "Ounce", 28.3495),
            "FJ": ("Pound", 453.592, "Ounce", 28.3495),
            "JM": ("Pound", 453.592, "Ounce", 28.3495),
            "PG": ("Pound", 453.592, "Ounce", 28.3495),
            "TO": ("Pound", 453.592, "Ounce", 28.3495),
            "IN": ("Pound", 453.592, "Kilogram", 1000),
            "KH": ("Pound", 453.592, "Kilogram", 1000),
            "TZ": ("Pound", 453.592, "Kilogram", 1000),
            "PH": ("Pound", 453.592, "Kilogram", 1000),
            "LK": ("Pound", 453.592, "Kilogram", 1000),
        }

        unit_a = "Gram"
        value_a = self.weight
        unit_b = "Kilogram"
        value_b = self.weight / 1000

        if self.country_code in conversions:
            unit_a, conv_a, unit_b, conv_b = conversions[self.country_code]
            value_a = self.weight / conv_a
            value_b = self.weight / conv_b

        return f"{value_a:.2f} {unit_a}, {value_b:.2f} {unit_b}"

    def get_day_part(self) -> str:
        """Returns the part of the day when the catch was made."""
        hour = self.caught_at.hour
        if 0 <= hour < 6:
            return "Night"
        elif 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 18:
            return "Afternoon"
        else:
            return "Evening"

    def get_season(self) -> str:
        """Returns the season when the catch was made based on the northern hemisphere's meteorological seasons."""
        month = self.caught_at.month
        if 3 <= month <= 5:
            return "Spring"
        elif 6 <= month <= 8:
            return "Summer"
        elif 9 <= month <= 11:
            return "Autumn"
        else:
            return "Winter"

    def get_weight_category(self) -> str:
        """Returns the weight category of the fish based on expected weight."""
        a = 0.0123
        b = 3.1
        expected_weight = a * (self.length**b)

        weight_diff = (self.weight - expected_weight) / weight_diff * 100

        if weight_diff > 2:
            return "heavy"
        elif weight_diff < -2:
            return "light"
        else:
            return "average"

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]),
        )
