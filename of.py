import os
import sys
import re
from datetime import datetime

valid_lines = []
corrupt_lines = []

'''
The validate_data function will check the students.csv line by line for corrupt data.

- Valid lines should be added to the valid_lines list.
- Invalid lines should be added to the corrupt_lines list.

Example input: 0896801,Kari,Wilmore,1970-06-18,INF
This data is valid and the line should be added to the valid_lines list unchanged.

Example input: 0773226,Junette,Gur_ry,1995-12-05,
This data is invalid and the line should be added to the corrupt_lines list in the following format:

0773226,Junette,Gur_ry,1995-12-05, => INVALID DATA: ['0773226', 'Gur_ry', '']

In the above example the studentnumber does not start with '08' or '09',
the last name contains a special character and the student program is empty.

Don't forget to put the students.csv file in the same location as this file!
'''

def is_student_number_valid(student_number):
    return bool(re.match(r"^0[89]\d{5}$", student_number))

def is_student_name_valid(student_name):
    return bool(re.match(r"^[A-Za-z]+$", student_name))

def is_student_date_of_birth_valid(stundet_date_of_birth):
    try:
        date_of_birth = datetime.strptime(stundet_date_of_birth, "%Y-%m-%d")
        return 1960 <= date_of_birth >= 2004
    except ValueError:
        return False
    
def is_valid_study_program(study_program):
    valid_program = ("INF", "TINF", "CMD", "AI")
    return valid_program in study_program

def validate_data(line):
    # WRITE YOUR SOLUTION HERE:
    fields = line.split(",")

    student_number = fields[0] if len(fields) > 0 else ''
    first_name = fields[1] if len(fields) > 1 else ''
    last_name = fields[2] if len(fields) > 2 else ''
    date_of_birth = fields[3] if len(fields) > 3 else ''
    study_program = fields[4] if len(fields) > 4 else ''

    invalid_fields = []

    if not is_student_number_valid(student_number):
        invalid_fields.append(student_number)
    if not is_student_name_valid(first_name):
        invalid_fields.append(first_name)
    if not is_student_name_valid(last_name):
        invalid_fields.append(last_name)
    if not is_student_date_of_birth_valid(date_of_birth):
        invalid_fields.append(date_of_birth)
    if not is_valid_study_program(study_program):
        invalid_fields.append(study_program)

    if invalid_fields:
        corrupt_lines.append(f"{line} => INVALID DATA: {invalid_fields}")
    else:
        valid_lines.append(line)


def main(csv_file):
    with open(os.path.join(sys.path[0], csv_file), newline='') as csv_file:
        # skip header line
        next(csv_file)

        for line in csv_file:
            validate_data(line.strip())

    print('### VALID LINES ###')
    print("\n".join(valid_lines))
    print('### CORRUPT LINES ###')
    print("\n".join(corrupt_lines))


if __name__ == "__main__":    
    main('students.csv')