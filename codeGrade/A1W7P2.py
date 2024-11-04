import os
import sys
import csv


def load_csv_file(file_name):
    """Loads a CSV file and returns its content as a list of rows."""
    file_content = []
    with open(
        os.path.join(sys.path[0], file_name), newline="", encoding="utf8"
    ) as csv_file:
        file_content = list(csv.reader(csv_file, delimiter=","))
    return file_content


def get_headers(file_content):
    """Returns a list of all column headers from the first row."""
    return file_content[0]


def search_by_type(file_content, show_type):
    """Returns a list of all TV Shows or Movies based on the requested type."""
    return list(filter(lambda x: x[1] == show_type, file_content))


def search_by_director(file_content, director):
    """Returns a list of all TV Shows and Movies that have the specified director."""
    return list(filter(lambda x: director in x[3] if x[3] else False, file_content))


def get_directors(file_content):
    """Returns a set of unique directors from the list."""
    directors_set = set()
    for row in file_content:
        if row[3]:  # Check if director field is not empty
            directors = row[3].split(",")
            for director in directors:
                directors_set.add(director.strip())
    return directors_set


def dou_type_directors(file_content):
    """Returns a list of directors who both of movie and TV show"""
    all_directors = get_directors(file_content)
    dou_directors = []
    for director in all_directors:
        director_works = search_by_director(file_content, director)
        has_movie = any(row[1] == "Movie" for row in director_works)
        has_tv_show = any(row[1] == "TV Show" for row in director_works)

        if has_movie and has_tv_show:
            dou_directors.append(director)
    dou_directors.sort()
    return dou_directors


def shows_and_movies(file_content):
    """Counts the number of TV Shows and Movies."""
    tv_shows = search_by_type(file_content, "TV Show")
    movies = search_by_type(file_content, "Movie")
    return tv_shows, movies


def director_counts(file_content):
    """Returns a list of tuples containing each director's name, number of movies, and number of TV shows."""
    director_dict = {}
    for row in file_content[1:]:
        if row[3]:  # Check if the director field is not empty
            directors = row[3].split(",")
            for director in directors:
                director = director.strip()
                if director not in director_dict:
                    # [movies_count, tv_shows_count]
                    director_dict[director] = [0, 0]
                if row[1] == "Movie":
                    director_dict[director][0] += 1
                elif row[1] == "TV Show":
                    director_dict[director][1] += 1
    return sorted(
        [(name, counts[0], counts[1]) for name, counts in director_dict.items()]
    )


def main():
    file_name = "file/netflix_titles.csv"
    file_content = load_csv_file(file_name)

    print("\nMenu:")
    print("[1] Print the amount of TV Shows")
    print("[2] Print the amount of Movies")
    print(
        "[3] Print the (full) names of directors in alphabetical order who lead both tv shows and movies."
    )
    print(
        "[4] Print the name of each director in alphabetical order, the number of movies and the number of TV shows."
    )
    print("[5] Exit")
    choice = input("Select an option: ")

    if choice == "1":
        tv_show, _ = shows_and_movies(file_content)
        print(f"Amount of TV Shows: {len(tv_show)}")
    elif choice == "2":
        _, movie = shows_and_movies(file_content)
        print(f"Amount of Movies: {len(movie)}")
    elif choice == "3":
        dou_director = dou_type_directors(file_content)
        print(dou_director)
    elif choice == "4":
        directors_info = director_counts(file_content)
        print(directors_info)
    else:
        print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
