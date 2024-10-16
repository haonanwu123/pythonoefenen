tip_rate = 0.15
tax_rate = 0.21

def cal_meal_amount():
    user_input = input("Please enter the cost(format'Cost of the meal: xy.wz'):")

    try:
        amount_str = user_input.split(":")[1].strip()
        amount_cost = float(amount_str)

        tip_cost = amount_cost * tip_rate
        tax_cost = amount_cost * tax_rate
        total_cost = tip_cost + tax_cost + amount_cost

        print(f"Tax: {tax_cost:.3f}, Tip: {tip_cost:.3f}, Total: {total_cost:.3f}")
    
    except (IndexError, ValueError):
        print("Invalid input format. Please enter the cost in the format 'Cost of the meal: xy.wz'.")

cal_meal_amount()