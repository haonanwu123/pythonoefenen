def add_book(books: dict) -> str:
    book_details = input(
        "Book details (example: book title, book author, publisher, publication date): "
    )

    title, author, publisher, publication_date = [
        x.strip() for x in book_details.split(",")
    ]

    for book in books:
        if book["title"].lower() == title.lower():
            print(f"The book is already added.")
            break

    new_book = {
        "title": title,
        "author": author,
        "publisher": publisher,
        "pub_date": publication_date,
    }

    books.append(new_book)
    print("new book has been added.")


def search_book(books, term) -> bool:
    term = term.lower()

    for book in books:
        if (
            term == book["title"]
            or term == book["author"]
            or term == book["publisher"]
            or term == book["pub_date"]
        ):
            print(f"Book found for: {term} (available)")
            return True

    print(f"Can not foud the book.")
    return False


def display_books(books) -> list:
    for book in books:
        print(book)


def main():
    books = []

    while True:
        print("[A] Add a book")
        print("[S] Search a book")
        print("[E] Exit (and print)")

        choice = input("Enter a upper letter to choice: ").strip().upper()

        if choice == "A":
            add_book(books)
        elif choice == "S":
            term = input("Enter a term to search: ").strip().lower()
            search_book(books, term)
        elif choice == "E":
            print("Exiting and printing all books:")
            display_books(books)
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
