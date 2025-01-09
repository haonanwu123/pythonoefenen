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
        result.id = self.dbc.lastrowid
        self.conn.commit()
        return True

    def get_results_by_student(self, student_id, only_last=True):
        if only_last:
            query = """
                SELECT student_id, course_id, MAX(mark) as mark, achieved
                FROM results
                WHERE student_id = ?
                GROUP BY course_id
            """
        else:
            query = """
                SELECT student_id, course_id, mark, achieved FROM results WHERE student_id = ?
            """

        self.dbc.execute(
            query,
            (student_id,),
        )
        return self.dbc.fetchall()

    def get_results_by_course(self, course_id, only_last=True):
        if only_last:
            query = """
                SELECT student_id, course_id, MAX(mark) as mark, achieved
                FROM results
                WHERE student_id = ?
                GROUP BY student_id
            """
        else:
            query = """
                SELECT student_id, course_id , mark, achieved FROM results WHERE course_id = ?
            """

        self.dbc.execute(
            query,
            (course_id,),
        )
        return self.dbc.fetchall()

    def close(self):
        self.conn.close()
