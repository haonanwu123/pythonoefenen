import re

def is_name_valid(name: str) -> bool:
    return bool(re.match(r'^[A-Z][a-z]{0,20}$', name))

def is_title_valid(title: str) -> bool:
    return len(title) >= 1 and not any(char.isdigit() for char in title)

def is_salary_valid(salary: str) -> bool:
    try:
        salary_value = float(salary.replace('.', '').replace(',', '.'))
        return 20000.00 <= salary_value <= 80000.00
    except ValueError:
        return False

def is_date_valid(date: str) -> bool:
    try:
        year, month, day = map(int, date.split('-'))
        return year in (2021, 2022) and 1 <= month <= 12 and 1 <= day <= 31
    except ValueError:
        return False

def generate_job_offer(first_name, last_name, title, salary, start_date):
    return f"""
Here is the final letter to send:
Dear {first_name} {last_name},
After careful evaluation of your application for the position of {title},
we are glad to offer you the job. Your salary will be {salary} euro annually.
Your start date will be on {start_date}. Please do not hesitate to contact us with any questions.
Sincerely,
HR Department of XYZ
"""

def generate_rejection(first_name, last_name, title, feedback, feedback_statement):
    feedback_text = ""
    if feedback == "Yes":
        feedback_text = f"Here we would like to provide you our feedback about the interview.\n{feedback_statement}\n"
    
    return f"""
Here is the final letter to send:
Dear {first_name} {last_name},
After careful evaluation of your application for the position of {title},
at this moment we have decided to proceed with another candidate.
{feedback_text}We wish you the best in finding your future desired career. Please do not hesitate to contact us with any questions.
Sincerely,
HR Department of XYZ
"""

def main():
    while True:
        more_letters = input("More Letters? (Yes or No) ").strip().capitalize()
        if more_letters not in ["Yes", "No"]:
            print("Input error")
            continue
        
        if more_letters == "No":
            break
        
        job_type = input("Job Offer or Rejection? ")
        if job_type not in ["Job Offer", "Rejection"]:
            print("Input error")
            continue
        
        while True:
            first_name = input("First Name? ").strip()
            last_name = input("Last Name? ").strip()
            if is_name_valid(first_name) and is_name_valid(last_name):
                break
            else:
                print("Input error")
        
        while True:
            title = input("Job Title? ").strip()
            if is_title_valid(title):
                break
            else:
                print("Input error")
        
        if job_type == "Job Offer":
            while True:
                salary = input("Annual Salary? ").strip()
                if is_salary_valid(salary):
                    break
                else:
                    print("Input error")
            
            while True:
                start_date = input("Start Date?(YYYY-MM-DD) ").strip()
                if is_date_valid(start_date):
                    break
                else:
                    print("Input error")
            
            print(generate_job_offer(first_name, last_name, title, salary, start_date))
        
        elif job_type == "Rejection":
            while True:
                feedback = input("Feedback? (Yes or No) ").strip().capitalize()
                if feedback in ["Yes", "No"]:
                    break
                else:
                    print("Input error")
            
            feedback_statement = ""
            if feedback == "Yes":
                while True:
                    feedback_statement = input("Enter your Feedback (One Statement): ").strip()
                    if feedback_statement:
                        break
                    else:
                        print("Input error")
            
            print(generate_rejection(first_name, last_name, title, feedback, feedback_statement))

if __name__ == "__main__":
    main()