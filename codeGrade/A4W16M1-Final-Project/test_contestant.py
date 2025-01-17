import pytest
from datetime import datetime
from contestant import Contestant


@pytest.mark.parametrize(
    "date_of_birth, current_date, expected_age",
    [
        (
            datetime(1990, 5, 15),
            datetime(2023, 3, 4),
            32,
        ),  # May 15, 1990 -> Age 32 on March 4, 2023
        (
            datetime(2000, 12, 31),
            datetime(2023, 3, 4),
            22,
        ),  # December 31, 2000 -> Age 22 on March 4, 2023
        (
            datetime(1975, 1, 1),
            datetime(2023, 3, 4),
            48,
        ),  # January 1, 1975 -> Age 48 on March 4, 2023
        (
            datetime(2010, 7, 5),
            datetime(2023, 3, 4),
            12,
        ),  # July 5, 2010 -> Age 12 on March 4, 2023
    ],
)
def test_get_age(date_of_birth, current_date, expected_age):
    contestant = Contestant(
        id="contestant_1",
        first_name="John",
        last_name="Doe",
        classification="Pro",
        date_of_birth=date_of_birth,
    )
    contestant.get_age = lambda: (current_date - contestant.date_of_birth).days // 365

    assert contestant.get_age() == expected_age
