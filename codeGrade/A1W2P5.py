def holidays_netherland():
    holidays_list = {
        "New Years Day": "01-01",
        "Easter Sunday": "03-31",
        "Easter Monday": "04-01",
        "Koningsdag": "04-27",
        "Bevrijdingsdag": "05-05",
        "Ascension Day": "05-09",
        "Pentecost": "05-19",
        "Whit Monday": "05-20",
        "Vriendendag": "06-01",
        "Sinterklaas-eve": "12-05",
        "Christmas-eve": "12-24",
        "Christmas Day": "12-25",
        "Boxing Day": "12-26"
    }
    
    user_input = input("Date: Month: X, Day: Y\n").replace(" ", "")
    
    try:
        month_str = user_input.split(",")[0].split(":")[1]
        day_str = user_input.split(",")[1].split(":")[1]
        
        date = f"{month_str.zfill(2)}-{day_str.zfill(2)}"
        
        found_holiday = None
        for holiday, holiday_date in holidays_list.items():
            if holiday_date == date:
                found_holiday = holiday
                break
        
        if found_holiday:
            print(found_holiday)
        else:
            print("No holiday found on given input")
    
    except (IndexError, ValueError):
        print("Invalid input. Please use the format 'Month: X, Day: Y'.")

holidays_netherland()