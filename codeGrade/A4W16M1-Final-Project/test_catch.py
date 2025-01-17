import pytest
from datetime import datetime
from catch import Catch


# Test for get_weight_in_local_units()
@pytest.mark.parametrize(
    "country_code, expected_output",
    [
        ("US", "661.39 Pound, 29.97 Ounce"),  # Weight 300g -> 0.3kg
        ("IN", "300.00 Gram, 0.30 Kilogram"),  # Weight 300g -> 0.3kg
        ("GB", "1.00 Stone, 14.00 Pound"),  # Weight 300g -> 0.3kg
        ("AU", "661.39 Pound, 29.97 Ounce"),  # Weight 300g -> 0.3kg
    ],
)
def test_get_weight_in_local_units(country_code, expected_output):
    # Create a sample Catch instance
    catch = Catch(
        id=None,
        fish_id=1,
        contestant_id="contestant_1",
        caught_at=datetime(2023, 3, 4, 23, 59, 18),
        latitude=-6.416667,
        longitude=20.783333,
        country_code=country_code,
        weight=0.3,  # 300 grams
        length=2.74,
    )

    assert catch.get_weight_in_local_units() == expected_output


# Test for get_day_part()
@pytest.mark.parametrize(
    "datetime_input, expected_day_part",
    [
        (datetime(2023, 3, 4, 5, 30, 0), "Night"),  # 5:30 AM -> Night
        (datetime(2023, 3, 4, 9, 30, 0), "Morning"),  # 9:30 AM -> Morning
        (datetime(2023, 3, 4, 15, 30, 0), "Afternoon"),  # 3:30 PM -> Afternoon
        (datetime(2023, 3, 4, 19, 30, 0), "Evening"),  # 7:30 PM -> Evening
    ],
)
def test_get_day_part(datetime_input, expected_day_part):
    # Create a sample Catch instance with a specified datetime
    catch = Catch(
        id=None,
        fish_id=1,
        contestant_id="contestant_1",
        caught_at=datetime_input,
        latitude=-6.416667,
        longitude=20.783333,
        country_code="US",
        weight=0.3,
        length=2.74,
    )

    assert catch.get_day_part() == expected_day_part


# Test for get_season()
@pytest.mark.parametrize(
    "datetime_input, expected_season",
    [
        (datetime(2023, 3, 4, 5, 30, 0), "Spring"),  # March -> Spring
        (datetime(2023, 6, 4, 5, 30, 0), "Summer"),  # June -> Summer
        (datetime(2023, 9, 4, 5, 30, 0), "Autumn"),  # September -> Autumn
        (datetime(2023, 12, 4, 5, 30, 0), "Winter"),  # December -> Winter
    ],
)
def test_get_season(datetime_input, expected_season):
    catch = Catch(
        id=None,
        fish_id=1,
        contestant_id="contestant_1",
        caught_at=datetime_input,
        latitude=-6.416667,
        longitude=20.783333,
        country_code="US",
        weight=0.3,
        length=2.74,
    )

    assert catch.get_season() == expected_season


# Test for get_weight_category()
@pytest.mark.parametrize(
    "weight, length, expected_category",
    [
        (0.3, 10, "light"),  # Light weight (0.3kg compared to expected)
        (1.5, 20, "average"),  # Average weight (1.5kg compared to expected)
        (2.5, 20, "heavy"),  # Heavy weight (2.5kg compared to expected)
    ],
)
def test_get_weight_category(weight, length, expected_category):
    catch = Catch(
        id=None,
        fish_id=1,
        contestant_id="contestant_1",
        caught_at=datetime(2023, 3, 4, 23, 59, 18),
        latitude=-6.416667,
        longitude=20.783333,
        country_code="US",
        weight=weight,
        length=length,
    )

    assert catch.get_weight_category() == expected_category
