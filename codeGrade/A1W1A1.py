DAYS_IN_YEAR = 365
MONTHS_IN_YEAR = 12

def calculate_months_days():
    user_input = input("Please enter the number of years in the format 'Years: X' (e.g., 'Years: 5'): ")
    
    try:
        years_str = user_input.split(':')[1].strip()
        years = int(years_str)

        months = years * MONTHS_IN_YEAR
        days = years * DAYS_IN_YEAR

        print(f"Months: {months}, Days: {days}")
    except (IndexError, ValueError):
        print("Invalid input format. Please use the format 'Years: X', where X is a number.")

calculate_months_days()