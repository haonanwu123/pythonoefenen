from datetime import date
from catch import Catch
from fish import Fish
from contestant import Contestant


class Reporter:

    def total_amount_of_fish(self) -> int:
        """
        Returns the total number of fish recorded in the database.
        """
        raise NotImplementedError

    def biggest_catch(self) -> Catch:
        """
        Returns the catch with the highest weight recorded in the database.
        """
        raise NotImplementedError

    def longest_and_shortest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the longest and shortest catches recorded in the database.
        """
        raise NotImplementedError

    def heaviest_and_lightest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the heaviest and lightest catches by weight recorded in the database.
        """
        raise NotImplementedError

    def contestant_with_most_catches(self) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the most catches recorded in the database.
        """
        raise NotImplementedError

    def fish_with_most_catches(self) -> tuple[Fish, ...]:
        """
        Returns a tuple containing the fish species with the most catches recorded in the database.
        """
        raise NotImplementedError

    def contestant_with_first_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the first catch of a specified fish type.
        """
        raise NotImplementedError

    def contestant_with_last_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the last catch of a specified fish type.
        """
        raise NotImplementedError

    def contestants_fished_between(
        self, fish: Fish, start: date, end: date, to_csv: bool = False
    ) -> tuple[Contestant, ...]:
        """
        If to_csv is False, returns a tuple containing the contestants who fished a specified fish species between two dates.
        If to_csv is True, the results are written to a CSV file.
        """
        raise NotImplementedError

    def fish_caught_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Fish, ...]:
        """
        If to_csv is False, returns a tuple containing the fish species caught in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        raise NotImplementedError

    def contestants_fished_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Contestant, ...]:
        """
        If to_csv is False, returns a tuple containing the contestants who fished in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        raise NotImplementedError
