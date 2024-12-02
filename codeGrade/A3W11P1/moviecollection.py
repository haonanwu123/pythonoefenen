import os
import sys
import json


def load_movie():
    """
    Load the movie data from the 'movies.json' file.

    Returns:
        list: A list of dictionaries where each dictionary represents a movie.
    """
    try:
        with open(os.path.join(sys.path[0], "movies.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: The 'movies.json' file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_movie(movies):
    """
    Save the updated movie data back to the 'movies.json' file.

    Args:
        movies (list): A list of movie dictionaries to be saved.
    """
    try:
        with open(os.path.join(sys.path[0], "movies.json"), "w") as file:
            json.dump(movies, file, indent=4)
    except FileNotFoundError:
        print("Error: The 'movies.json file was not found.")
    except Exception as e:
        print(f"An error occureed: {e}")


def count_movies_2004(movies):
    """
    Count the number of movies released in the year 2004.

    Args:
        movies (list): A list of movie dictionaries.

    Returns:
        int: The number of movies released in 2004.
    """
    count = 0
    for movie in movies:
        if movie["year"] == 2004:
            count += 1
    return count


def count_movies_sf(movies):
    """
    Count the number of Science Fiction movies.
    Args:
        movies (list): A list of movie dictionaries.

    Returns:
        int: The number of movies released Science Fiction genre.
    """
    count = 0
    for movie in movies:
        if "Science Fiction" in movie["genres"]:
            count += 1
    return count


def movies_with_actor(movies, actor_name):
    """
    List all movies that feature a specific actor.

    Args:
        movies (list): A list of movie dictionaries.
        actor_name (str): The name of the actor to search for.

    Returns:
        list: A list of movies where the actor appears in the cast.
    """
    return [movie for movie in movies if actor_name in movie["cast"]]


def movies_with_sylvester_stallone(movies):
    """
    List all movies with Sylvester Stallone that were released between 1995 and 2005.

    Args:
        movies (list): A list of movie dictionaries.

    Returns:
        list: A list of movies with Sylvester Stallone released between 1995 and 2005.
    """
    return [
        movie
        for movie in movies
        if "Sylvester Stallone" in movie["cast"] and 1995 <= movie["year"] <= 2005
    ]


def modify_gladiator_year(movies):
    """
    Change the release year of the movie 'Gladiator' from 2000 to 2001.

    Args:
        movies (list): A list of movie dictionaries.
    """
    for movie in movies:
        if movie["title"] == "Gladiator":
            movie["year"] = 2001
    save_movie(movies)


def adjust_oldest_movie_year(movies):
    """
    Adjust the release year of the oldest movie by one year earlier.

    Args:
        movies (list): A list of movie dictionaries.
    """
    oldest_movie = min(movies, key=lambda x: x["year"])
    oldest_movie["year"] -= 1
    save_movie(movies)


def change_actor_name(movies, old_name, new_name):
    """
    Change the name of an actor in all movies they appear in.

    Args:
        movies (list): A list of movie dictionaries.
        old_name (str): The actor's current name.
        new_name (str): The new name for the actor.
    """
    for movie in movies:
        if old_name in movie["cast"]:
            movie["cast"] = [
                new_name if actor == old_name else actor for actor in movie["cast"]
            ]
    save_movie(movies)


def remove_actor(movies, actor_name):
    """
    Remove an actor from the cast of all movies they appear in.

    Args:
        movies (list): A list of movie dictionaries.
        actor_name (str): The name of the actor to remove.
    """
    for movie in movies:
        if actor_name in movie["cast"]:
            movie["cast"].remove(actor_name)
    save_movie(movies)


def search_movie(movies, title):
    """
    Search for a movie by its title.

    Args:
        movies (list): A list of movie dictionaries.
        title (str): The title of the movie to search for.

    Returns:
        dict or None: The movie dictionary if found, or None if not found.
    """
    return next(
        (movie for movie in movies if movie["title"].lower() == title.lower()), None
    )


def modify_movie(movies, title, new_title, new_year):
    """
    Modify a movie's title and/or release year by searching for the movie's title.

    Args:
        movies (list): A list of movie dictionaries.
        title (str): The current title of the movie to modify.
        new_title (str): The new title for the movie.
        new_year (int): The new release year for the movie.

    Returns:
        dict or None: The modified movie dictionary if found, or None if not found.
    """
    for movie in movies:
        if movie["title"].lower() == title.strip().lower():
            movie["title"] = new_title
            movie["year"] = new_year
            save_movie(movies)
            return movie
    return None


# We created the menu layout for you
# Only given imports are allowed
def main():
    movies = load_movie()

    while True:
        print("[I] Movie information overview")
        print("[M] Make modification based on assignment")
        print("[S] Search a movie title ")
        print("[C] Change title and/or release year by search on title")
        print("[Q] Quit program")

        choice = input("Choose an option: ").strip().upper()

        if choice == "I":
            print(f"Movies released in 2004: {count_movies_2004(movies)}")
            print(f"Movies in Science Fiction genre: {count_movies_sf(movies)}")
            print(
                f"Movies with Keanu Reeves: {movies_with_actor(movies, 'Keanu Reeves')}"
            )
            print(
                f"Movies with Sylvester Stallone (1995-2005): {movies_with_sylvester_stallone(movies)}"
            )

        elif choice == "M":
            print("Making modifications...")
            modify_gladiator_year(movies)
            adjust_oldest_movie_year(movies)
            change_actor_name(movies, "Natalie Portman", "Nat Portman")
            remove_actor(movies, "Kevin Spacey")
            print("Modifications have been applied.")

        elif choice == "S":
            title = input("Enter movie title to search: ").strip()
            movie = search_movie(movies, title)
            if movie:
                print(movie)
            else:
                print("Movie not found.")

        elif choice == "C":
            title = input("Enter the current movie title to modify: ").strip()
            new_title = input("Enter the new title: ").strip()
            new_year = int(input("Enter the new release year: ").strip())
            modified_movie = modify_movie(movies, title, new_title, new_year)
            if modified_movie:
                print(modified_movie)
            else:
                print("Movie not found.")

        elif choice == "Q":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

    # Implement rest of functionality


if __name__ == "__main__":
    main()
