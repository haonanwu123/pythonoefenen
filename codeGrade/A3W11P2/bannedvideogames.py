import csv
import os
import sys


def count_banned_games_in_israel(data):
    """
    Count how many games are banned in Israel.

    Args:
        data (list): List of dictionaries containing game information.

    Returns:
        int: The number of games banned in Israel.
    """
    return sum(1 for row in data if row["Country"].lower() == "israel")


def country_with_most_bans(data):
    """
    Find the country with the highest number of banned games.

    Args:
        data (list): List of dictionaries containing game information.

    Returns:
        str: The name of the country with the most bans.
    """
    country_bans = {}
    for row in data:
        country = row["Country"]
        country_bans[country] = country_bans.get(country, 0) + 1
    return max(country_bans, key=country_bans.get)


def count_assassins_creed_bans(data):
    """
    Count how many unique Assassin's Creed games are banned.

    Args:
        data (list): List of dictionaries containing game information.

    Returns:
        int: The number of unique Assassin's Creed games banned.
    """
    banned_games = set()
    for row in data:
        if "Assassin's Creed" in row["Series"]:
            banned_games.add(row["Game"].lower())
    return len(banned_games)


def games_banned_in_germany(data):
    """
    Get details of all games banned in Germany.
    """
    return [
        {"Game": row["Game"], "Details": row["Details"]}
        for row in data
        if row["Country"].lower() == "germany"
    ]


def countries_banning_red_dead_redemption(data):
    """
    Get details of all countries where Red Dead Redemption is banned.
    """
    return [
        {"Country": row["Country"], "Details": row["Details"]}
        for row in data
        if "Red Dead Redemption" in row["Game"]
    ]


def modify_file(data, filename):
    """
    Apply specific modifications to the dataset and save it back to the file.

    - Remove all records for Germany.
    - Rename 'Silent Hill VI' to 'Silent Hill Remastered'.
    - Change the status of 'Bully' in Brazil to 'Ban Lifted'.
    - Change the genre of 'Manhunt II' from 'Stealth' to 'Action'.

    Args:
        data (list): List of dictionaries containing game information.
        filename (str): Path to the CSV file to save the modified data.
    """

    modified_data = []
    for row in data:
        if row["Country"].lower() == "germany":
            continue  # Remove Germany records
        if row["Game"].lower() == "silent hill vi":
            row["Game"] = "Silent Hill Remastered"
        if row["Game"].lower() == "bully" and row["Country"].lower() == "brazil":
            row["Ban Status"] = "Ban Lifted"
        if row["Game"].lower() == "manhunt ii":
            row["Genre"] = "Action"
        modified_data.append(row)

    with open(
        os.path.join(sys.path[0], filename), mode="w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(modified_data)


def add_new_game(data, filename):
    """
    Add a new game record to the dataset and save it back to the file.

    Args:
        data (list): List of dictionaries containing game information.
        filename (str): Path to the CSV file to save the updated data.
    """
    keys = [
        "Id",
        "Game",
        "Series",
        "Country",
        "Details",
        "Ban Category",
        "Ban Status",
        "Wikipedia Profile",
        "Image",
        "Summary",
        "Developer",
        "Publisher",
        "Genre",
        "Homepage",
    ]
    new_game = {}
    for key in keys:
        new_game[key] = input(f"{key}: ")
    data.append(new_game)
    with open(
        os.path.join(sys.path[0], filename), mode="w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def overview_of_banned_games(data):
    """
    Display an overview of banned games per country.

    Args:
        data (list): List of dictionaries containing game information.

    Returns:
        None
    """
    country_games = {}
    for row in data:
        country = row["Country"]
        if country not in country_games:
            country_games[country] = []
        country_games[country].append(row["Game"])

    for country, games in country_games.items():
        print(f"{country} - {len(games)}")
        for game in games:
            print(f"- {game}")


def search_by_country(data):
    """
    Search and display all games banned in a specific country.

    Args:
        data (list): List of dictionaries containing game information.

    Returns:
        None
    """
    country = input("Enter country name: ").strip().lower()
    results = [row for row in data if row["Country"].lower() == country]
    for row in results:
        print(f"{row['Game']} - {row['Details']}")


def main(filename: str) -> None:
    """
    Main function to display the menu and handle user interactions.
    """
    with open(os.path.join(sys.path[0], filename), mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        information = list(reader)

    while True:
        print("[I] Print request info from assignment")
        print("[M] Make modification based on assignment")
        print("[A] Add new game to list")
        print("[O] Overview of banned games per country")
        print("[S] Search the dataset by country")
        print("[Q] Quit program")

        choice = input("Enter your choice: ").strip().upper()

        if choice == "I":
            print(
                "How many games got banned in Israel:",
                count_banned_games_in_israel(information),
            )
            print(
                "Which country got the most games banned:",
                country_with_most_bans(information),
            )
            print(
                "How many games within the Assassin's Creed series are currently banned:",
                count_assassins_creed_bans(information),
            )
            print("Show all games banned in Germany:")
            for game in games_banned_in_germany(information):
                print(game)
            print("Show all countries the game Red Dead Redemption got banned in:")
            for game in countries_banning_red_dead_redemption(information):
                print(game)

        elif choice == "M":
            modify_file(information, filename)
            print("Modifications applied.")

        elif choice == "A":
            add_new_game(information, filename)

        elif choice == "O":
            overview_of_banned_games(information)

        elif choice == "S":
            search_by_country(information)

        elif choice == "Q":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main("bannedvideogames.csv")
