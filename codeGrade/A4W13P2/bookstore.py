import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta


def sync_database(con):
    """
    Synchronizes the database with the JSON file.
    Adds missing books from the JSON file to the database.
    """
    json_file = os.path.join(sys.path[0], "books.json")
    with open(json_file, "r") as file:
        books = json.load(file)

    cursor = con.cursor()

    for book in books:
        cursor.execute("""SELECT COUNT(*) FROM books WHERE isbn = ?""", (book["isbn"],))
        exists = cursor.fetchone()[0]

        if not exists:
            cursor.execute(
                """INSERT INTO books (isbn, title, author, pages, year)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    book["isbn"],
                    book["title"],
                    book["author"],
                    book["pages"],
                    book["year"],
                ),
            )

    con.commit()
    print("Database synchronized with JSON file.")


def borrow_book(con):
    """
    Allows a user to borrow a book if it is available.
    Calculates the return date based on the duration.
    """
    try:
        book_identifier = input("Enter the book ID or ISBN: ").strip()
        duration = int(input("Enter the duration in days: ").strip())
        cursor = con.cursor()

        cursor.execute(
            '''SELECT * FROM books WHERE (id = ? OR isbn = ?) AND status = "AVAILABLE"''',
            (book_identifier, book_identifier),
        )
        book = cursor.fetchone()

        if not book:
            print("Book  is not available or does not exist.")
            return

        return_date = (datetime.now() + timedelta(days=duration)).strftime("%d-%m-%Y")

        cursor.execute(
            """UPDATE books SET status = "BORROWED", return_date = ? where id = ?""",
            (return_date, book[0]),
        )
        con.commit()

        print(f"Book borrowed successfully! Return by {return_date}.")
    except Exception as e:
        print(f"error:{e}")


def return_book(con):
    """
    Allows a user to return a borrowed book.
    Calculates and displays any late return fine.
    """
    try:
        book_identifier = input("Enter the book ID or ISBN: ").strip()
        cursor = con.cursor()

        cursor.execute(
            '''SELECT * FROM books WHERE (id = ? OR isbn = ?) AND status = "BORROWED"''',
            (book_identifier, book_identifier),
        )
        book = cursor.fetchone()

        if not book:
            print("Book  is not available or does not exist.")
            return

        return_date = datetime.strptime(book[7], "%d-%m-%Y") if book[7] else None
        current_date = datetime.now()

        if return_date and current_date > return_date:
            days_late = (current_date - return_date).days
            fine = days_late * 0.50
            print(f"Book is returend late. Fine to py: {fine:.2f} EUR.")
        else:
            print("Book returend on time, no fine.")

        cursor.execute(
            """UPDATE books SET status = "AVAILABLE", return_date = NULL WHERE id = ?""",
            (book[0],),
        )
        con.commit()

        print("Book returned successfully.")
    except Exception as e:
        print(f"error:{e}")


def search_book(con):
    """
    Searches for a book by title, ISBN, or author.
    Displays the book information and its status.
    """
    try:
        search_term = input("Enter search term: ").strip()
        cursor = con.cursor()

        cursor.execute(
            """SELECT * FROM books WHERE title LIKE ? OR isbn LIKE ? OR author LIKE ?""",
            (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"),
        )
        book = cursor.fetchone()

        if not book:
            print("No book found matching the search term.")
            return

        book_info = {
            "id": book[0],
            "isbn": book[1],
            "title": book[2],
            "author": book[3],
            "pages": book[4],
            "year": book[5],
            "status": book[6],
            "return_date": book[7],
        }
        print(book_info)
    except Exception as e:
        print(f"Error: {e}")


def main():
    con = sqlite3.connect(os.path.join(sys.path[0], "bookstore.db"))
    con.execute(
        """CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            year TEXT NOT NULL,
            status TEXT DEFAULT "AVAILABLE",
            return_date DATE DEFAULT NULL
        );"""
    )

    sync_database(con)

    while True:
        print("\nDefault Menu:")
        print("[B] Borrow book")
        print("[R] Return book")
        print("[S] Search book")
        print("[Q] Quit program")

        choice = input("Select an option: ").strip().upper()

        if choice == "B":
            borrow_book(con)
        elif choice == "R":
            return_book(con)
        elif choice == "S":
            search_book(con)
        elif choice == "Q":
            print("Goodbye!")
            con.close()
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
