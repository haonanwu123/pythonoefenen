import re
from datetime import datetime, timedelta

def is_input_valid(inp_date):
    regex_pattern = '^\\d{4}-\\d{2}-\\d{2}$'
    # regx_pattern = r'^\d{4}-\d{2}-\d{2}$' raw string, \ do not exchange to \\
    return bool(re.match(regex_pattern, inp_date))

def get_next_day(date_str):
    date_format = "%Y-%m-%d"
    try:
        current_date = datetime.strptime(date_str,date_format)
        next_day = current_date + timedelta(days=1)
        return next_day.strftime(date_format)
    except ValueError:
        print("Date calculation error.")

def main():
    user_input = input("Input Date: ")

    if is_input_valid(user_input):
        nex_date = get_next_day(user_input)
        print(f"Next Date: {nex_date}")
    else:
        print("Input format Error. Correct Format: YYYY-MM-DD")

main()