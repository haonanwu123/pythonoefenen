# Pizza types and slicing options
VEGETARIAN_PIZZAS = ["Margherita", "Quatro Formaggi", "Hawaii"]
NON_VEGETARIAN_PIZZAS = ["Pepperoni", "Quatro Stagioni", "Al Tonno"]

def distribute_slices(total_slices, num_people):
    slices_per_person = total_slices // num_people
    leftover_slices = total_slices % num_people
    return slices_per_person, leftover_slices

def get_pizza_preferences(num_people):
    preferences = {}
    for i in range(1, num_people+1):
        print(f"\nEnter pizza preferences for person {i}: (up to 3 types)")
        is_vegetarian = input("Does this person eat only vegetarian pizzas? (yes/no): ").strip().lower() == 'yes'
        
        available_pizzas = VEGETARIAN_PIZZAS if is_vegetarian else VEGETARIAN_PIZZAS + NON_VEGETARIAN_PIZZAS
        print(f"Available pizzas: {', '.join(available_pizzas)}")
        
        person_prefs = []
        for j in range(3):
            pizza_pref = input(f"Enter preference {j+1} (or press Enter to skip): ").strip()
            if pizza_pref == "":
                break
            if pizza_pref in available_pizzas:
                person_prefs.append(pizza_pref)
            else:
                print(f"Invalid preference! Choose from the available pizzas.")
        
        preferences[f"Person {i}"] = person_prefs
    return preferences

def main():
    # Input: number of people and pizzas
    num_people = int(input("Enter the number of people in the group: "))
    num_pizzas = int(input("Enter the number of pizzas ordered: "))
    
    # Input: slices per pizza
    slices_per_pizza = int(input("How many slices does each pizza have? (e.g., 4, 6, 8, or 12): "))
    
    # Input: number of vegetarian and non-vegetarian pizzas
    veg_pizzas = int(input("Enter the number of vegetarian pizzas: "))
    non_veg_pizzas = num_pizzas - veg_pizzas  # Non-veg pizzas is the remaining amount
    
    # Calculate total slices
    total_slices = num_pizzas * slices_per_pizza
    veg_slices = veg_pizzas * slices_per_pizza
    non_veg_slices = non_veg_pizzas * slices_per_pizza

    # Distribute slices equally among people
    slices_per_person, leftover_slices = distribute_slices(total_slices, num_people)
    
    # Collect pizza preferences from each person
    preferences = get_pizza_preferences(num_people)
    
    # Display the results
    print("\nPizza Distribution Results:")
    print(f"Each person can have {slices_per_person} slices.")
    print(f"There are {leftover_slices} leftover slices.")
    
    print("\nPizza Preferences per Person:")
    for person, prefs in preferences.items():
        print(f"{person}: Preferences - {', '.join(prefs) if prefs else 'No preferences'}")
    
    print(f"\nTotal pizzas: {num_pizzas} (Vegetarian: {veg_pizzas}, Non-vegetarian: {non_veg_pizzas})")
    print(f"Total slices: {total_slices} (Vegetarian slices: {veg_slices}, Non-veg slices: {non_veg_slices})")

if __name__ == "__main__":
    main()
