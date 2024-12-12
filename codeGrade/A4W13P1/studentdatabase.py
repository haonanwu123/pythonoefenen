import os
import sys
import sqlite3
from datetime import datetime


def add_new_student(con):
    """
    Adds a new student to the database.

    Prompts the user for first name, last name, city, date of birth, and an optional class.
    Validates the date format before saving the student record.
    """
    try:
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        city = input("Enter city: ").strip()
        date_of_birth = input("Enter date of birth (DD-MM-YYYY): ").strip()
        class_name = input("Enter the class: ").strip()

        datetime.strptime(date_of_birth, "%d-%m-%Y")

        cursor = con.cursor()
        cursor.execute(
            """INSERT INTO students (first_name, last_name, city, date_of_birth, class)
               VALUES (?, ?, ?, ?, ?)""",
            (first_name, last_name, city, date_of_birth, class_name),
        )
        con.commit()
        print(
            f"Student added successfully. Assigned student number: {cursor.lastrowid}"
        )
    except Exception as e:
        print(f"Error: {e}")


def assign_student_to_class(con):
    """
    Assigns a student to a class.

    Prompts the user for the student number and the class name.
    Updates the student's class if the student number exists, otherwise displays an error.
    """
    try:
        studentnumber = input("Enter student number: ").strip()
        class_name = input("Enter class name: ").strip()

        cursor = con.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE studentnumber = ?", (studentnumber,)
        )
        student = cursor.fetchone()

        if not student:
            print(f"Could not find student with number: {studentnumber}")
            return

        cursor.execute(
            "UPDATE students SET class = ? WHERE studentnumber = ?",
            (class_name, studentnumber),
        )
        con.commit()
        print(f"Student {studentnumber} has been assigned to class {class_name}.")
    except Exception as e:
        print(f"Error: {e}")


def list_all_students(con):
    """
    Lists all students in the database.

    Fetches and displays all student records sorted by class in descending order.
    If no students are found, informs the user.
    """
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM students ORDER BY class DESC")
        students = cursor.fetchall()

        if not students:
            print("No students found.")
            return

        print("\nAll Students:")
        for student in students:
            print(student)
    except Exception as e:
        print(f"Error: {e}")


def list_students_in_class(con):
    """
    Lists all students in a specified class.

    Prompts the user for a class name, fetches all students in that class,
    and displays them sorted by student number in ascending order.
    """
    try:
        class_name = input("Enter class name: ").strip()

        cursor = con.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE class = ? ORDER BY studentnumber ASC",
            (class_name,),
        )
        students = cursor.fetchall()

        if not students:
            print(f"No students found in class {class_name}.")
            return

        print(f"\nStudents in class {class_name}:")
        for student in students:
            print(student)
    except Exception as e:
        print(f"Error: {e}")


def search_student(con):
    """
    Searches for a student in the database.

    Prompts the user for a search term, then searches for it in the first name, last name, or city fields.
    Displays the first match found or informs the user if no match is found.
    """
    try:
        search_term = input("Enter search term: ").strip()

        cursor = con.cursor()
        cursor.execute(
            """SELECT * FROM students WHERE first_name LIKE ? OR last_name LIKE ? OR city LIKE ?LIMIT 1""",
            (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"),
        )
        student = cursor.fetchone()

        if not student:
            print(f"No student found matching search term: {search_term}")
            return

        print(f"\nFound Student: {student}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    con = sqlite3.connect(os.path.join(sys.path[0], "studentdatabase.db"))
    con.execute(
        '''CREATE TABLE IF NOT EXISTS students (
           studentnumber INTEGER PRIMARY KEY AUTOINCREMENT,first_name TEXT NOT NULL,
           last_name TEXT NOT NULL,city TEXT NOT NULL,date_of_birth DATE NOT NULL,class TEXT DEFAULT NULL );'''
    )

    while True:
        print("\nDefault Menu:")
        print("[A] Add new student")
        print("[C] Assign student to class")
        print("[D] List all students")
        print("[L] List all students in class")
        print("[S] Search student")
        print("[Q] Quit program")

        choice = input("Select an option: ").strip().upper()

        if choice == "A":
            add_new_student(con)
        elif choice == "C":
            assign_student_to_class(con)
        elif choice == "D":
            list_all_students(con)
        elif choice == "L":
            list_students_in_class(con)
        elif choice == "S":
            search_student(con)
        elif choice == "Q":
            print("Goodbye!")
            con.close()
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
