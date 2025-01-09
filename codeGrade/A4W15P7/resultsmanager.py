import os
import sys
import sqlite3

from result import Result
from student import Student
from course import Course


class ResultsManager:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(sys.path[0], "studentresults.db"))
        self.dbc = self.conn.cursor()

    def create_tables(self):
        self.dbc.execute(
            """CREATE TABLE IF NOT EXISTS courses
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          points INTEGER NOT NULL);"""
        )

        self.dbc.execute(
            """CREATE TABLE IF NOT EXISTS students
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          first_name TEXT NOT NULL,
                          last_name TEXT NOT NULL,
                          date_of_birth DATE NOT NULL,
                          class_code TEXT NULL);"""
        )

        self.dbc.execute(
            """CREATE TABLE IF NOT EXISTS results
                         (student_id INTEGER NOT NULL,
                          course_id INTEGER NOT NULL,
                          mark INTEGER NOT NULL,
                          achieved DATE NOT NULL,
                          PRIMARY KEY(student_id, course_id, mark));"""
        )

        self.conn.commit()

    def get_course(self, course_id) -> Course:
        self.dbc.execute(
            "SELECT * FROM courses WHERE id = ?",
            (course_id,),
        )
        row = self.dbc.fetchone()
        return Course(*row[1:], id=row[0]) if row else None

    def add_course(self, course: Course) -> Course:
        self.dbc.execute(
            "INSERT INTO courses (name, points) VALUES (?, ?)",
            (
                course.name,
                course.points,
            ),
        )
        course.id = self.dbc.lastrowid
        self.conn.commit()
        return course

    def get_student(self, student_id) -> Student:
        self.dbc.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        )
        row = self.dbc.fetchone()
        return Student(*row[1:], id=row[0]) if row else None

    def add_student(self, student: Student) -> Student:
        self.dbc.execute(
            "INSERT INTO students (first_name, last_name, date_of_birth, class_code) Values (?, ?, ?, ?)",
            (
                student.first_name,
                student.last_name,
                student.date_of_birth,
                student.class_code,
            ),
        )
        student.id = self.dbc.lastrowid
        self.conn.commit()
        return student

    def add_result(self, result: Result) -> bool:
        self.dbc.execute(
            "SELECT MAX(mark) FROM results WHERE student_id = ? and course_id = ?",
            (
                result.student_id,
                result.course_id,
            ),
        )
        max_mark = self.dbc.fetchone()[0]

        if max_mark is not None and result.mark <= max_mark:
            return False

        self.dbc.execute(
            "INSERT INTO results (student_id, course_id, mark, achieved) VALUES (?, ?, ?, ?)",
            (
                result.student_id,
                result.course_id,
                result.mark,
                result.achieved,
            ),
        )
        self.conn.commit()
        return True

    def get_results_by_student(self, student_id, only_last=True):
        student = self.get_student(student_id)
        if not student:
            return []

        if only_last:
            query = """
                SELECT c.id, c.name, c.points, r.mark, r.achieved
                FROM results r
                JOIN courses c ON r.course_id = c.id
                WHERE r.student_id = ?
                AND r.mark = (
                    SELECT MAX(r2.mark)
                    FROM results r2
                    WHERE r2.student_id = r.student_id AND r2.course_id = r.course_id
                )
                 ORDER BY r.achieved ASC
              """
        else:
            query = """
                SELECT c.id, c.name, c.points, r.mark, r.achieved
                FROM results r
                JOIN courses c ON r.course_id = c.id
                WHERE r.student_id = ?
                ORDER BY c.id ASC, r.achieved ASC
             """

        self.dbc.execute(query, (student_id,))
        results = self.dbc.fetchall()

        result_dict = {}
        for course_id, course_name, course_points, mark, achieved in results:
            if course_id not in result_dict:
                result_dict[course_id] = {
                    "id": course_id,
                    "name": course_name,
                    "points": course_points,
                    "results": [],
                }
            result_dict[course_id]["results"].append(
                {"mark": mark, "achieved": achieved}
            )

        for course in result_dict.values():
            course["results"].sort(key=lambda x: x["achieved"], reverse=True)

        return list(result_dict.values())

    def get_results_by_course(self, course_id, only_last=True):
        course = self.get_course(course_id)
        if not course:
            return []

        if only_last:
            query = """
                SELECT r.student_id, r.mark, r.achieved, s.first_name, s.last_name, s.date_of_birth
                FROM results r
                JOIN students s ON r.student_id = s.id
                WHERE r.course_id = ?
                AND r.mark = (
                    SELECT MAX(r2.mark)
                    FROM results r2
                    WHERE r2.student_id = r.student_id AND r2.course_id = r.course_id
                )
                ORDER BY r.achieved DESC
             """
        else:
            query = """
                SELECT r.student_id, r.mark, r.achieved, s.first_name, s.last_name, s.date_of_birth
                FROM results r
                JOIN students s ON r.student_id = s.id
                WHERE r.course_id = ?
                ORDER BY r.student_id ASC, r.achieved ASC
             """

        self.dbc.execute(query, (course_id,))
        results = self.dbc.fetchall()

        result_dict = {}
        for student_id, mark, achieved, first_name, last_name, date_of_birth in results:
            full_name = f"{first_name} {last_name}"
            if student_id not in result_dict:
                result_dict[student_id] = {
                    "id": student_id,
                    "name": full_name,
                    "date_of_birth": date_of_birth,
                    "results": [],
                }
            result_dict[student_id]["results"].append(
                {"mark": mark, "achieved": achieved}
            )

        for student in result_dict.values():
            student["results"].sort(key=lambda x: x["achieved"], reverse=True)

        return list(result_dict.values())

    def get_remaining_students(self):
        students = []
        self.dbc.execute("SELECT * FROM students")
        students_rows = self.dbc.fetchall()

        for row in students_rows:
            student_id, first_name, last_name, date_of_birth, class_code = row
            total_points = 0
            courses = []

            query = """
                SELECT c.id, r.mark, r.achieved, c.name, c.points
                FROM results r
                JOIN courses c ON r.course_id = c.id
                WHERE r.student_id = ?
             """
            self.dbc.execute(query, (student_id,))
            results = self.dbc.fetchall()

            for course_id, mark, achieved, course_name, course_points in results:
                passed = mark >= 55
                if passed:
                    total_points += course_points
                courses.append(
                    {
                        "id": course_id,
                        "name": course_name,
                        "points": course_points,
                        "passed": passed,
                        "mark": mark,
                        "achieved": achieved,
                    }
                )

            if total_points < 60:
                students.append(
                    {
                        "id": student_id,
                        "name": f"{first_name} {last_name}",
                        "date_of_birth": date_of_birth,
                        "total_points": total_points,
                        "courses": courses,
                    }
                )

        return students

    def close(self):
        self.conn.close()
