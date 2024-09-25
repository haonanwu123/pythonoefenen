# Pizza types and slicing options
VEGETARIAN_PIZZAS = ["Margherita", "Quatro Formaggi", "Hawaii"]
NON_VEGETARIAN_PIZZAS = ["Pepperoni", "Quatro Stagioni", "Al Tonno"]

def distribute_slices(total_slices, num_people):
    slices_per_person = total_slices // num_people
    leftover_slices = total_slices % num_people
    return slices_per_person, leftover_slices

def get_pizza_preferences(num_people):
    preferences = {}
    vegetarian_people = 0
    for i in range(1, num_people + 1):
        print(f"\nEnter pizza preferences for person {i}: (up to 3 types)")
        is_vegetarian = input("Does this person eat only vegetarian pizzas? (yes/no): ").strip().lower() == 'yes'
        
        available_pizzas = VEGETARIAN_PIZZAS if is_vegetarian else VEGETARIAN_PIZZAS + NON_VEGETARIAN_PIZZAS
        print(f"Available pizzas: {', '.join(available_pizzas)}")
        
        person_prefs = []
        for j in range(3):
            while True:  # Loop until we get a valid input or the user skips
                pizza_pref = input(f"Enter preference {j + 1} (or press Enter to skip): ").strip()
                if pizza_pref == "":
                    break  # Exit the loop if the user chooses to skip
                if pizza_pref in available_pizzas:
                    person_prefs.append(pizza_pref)
                    break  # Exit the loop after a valid preference
                else:
                    print(f"Invalid preference! Choose from the available pizzas.")  # Prompt for re-entry
        
        preferences[f"Person {i}"] = person_prefs
        if is_vegetarian:
            vegetarian_people += 1  # Count vegetarian people

    return preferences, vegetarian_people

def distribute_pizzas(preferences, veg_slices, non_veg_slices, vegetarian_people, veg_pizzas, non_veg_pizzas):
    total_people = len(preferences)
    pizza_distribution = {person: [] for person in preferences}  # Track distribution
    pizza_count = {pizza: 0 for pizza in VEGETARIAN_PIZZAS + NON_VEGETARIAN_PIZZAS}  # Track how many of each pizza type is distributed

    # Distribute preferred pizzas first
    for person, prefs in preferences.items():
        if prefs:  # If they have preferences
            for pref in prefs:
                if pref in VEGETARIAN_PIZZAS and vegetarian_people > 0 and veg_slices > 0 and pizza_count[pref] < veg_pizzas:
                    pizza_distribution[person].append(pref)
                    veg_slices -= 1
                    pizza_count[pref] += 1  # Increment the count of this pizza
                elif pref in NON_VEGETARIAN_PIZZAS and non_veg_slices > 0 and pizza_count[pref] < non_veg_pizzas:
                    pizza_distribution[person].append(pref)
                    non_veg_slices -= 1
                    pizza_count[pref] += 1  # Increment the count of this pizza

    # After preferred pizzas have been distributed, handle leftovers
    remaining_people = total_people - len([p for p in preferences if preferences[p]])  # Those without preferences

    if remaining_people > 0:
        # Distribute remaining vegetarian pizzas
        if vegetarian_people > 0 and veg_slices > 0:
            remaining_veg_people = vegetarian_people
            slices_per_veg_person, leftover_veg_slices = distribute_slices(veg_slices, remaining_veg_people)
            for person in pizza_distribution:
                if not preferences[person]:  # No preferences
                    pizza_distribution[person].extend([VEGETARIAN_PIZZAS[0]] * slices_per_veg_person)  # Give them a default vegetarian pizza
                    veg_slices -= slices_per_veg_person  # Decrease the available slices

        # Distribute remaining non-vegetarian pizzas
        remaining_non_veg_people = remaining_people
        if non_veg_slices > 0:
            slices_per_non_veg_person, leftover_non_veg_slices = distribute_slices(non_veg_slices, remaining_non_veg_people)
            for person in pizza_distribution:
                if not preferences[person]:  # No preferences
                    pizza_distribution[person].extend([NON_VEGETARIAN_PIZZAS[0]] * slices_per_non_veg_person)  # Give them a default non-vegetarian pizza
                    non_veg_slices -= slices_per_non_veg_person  # Decrease the available slices

    return pizza_distribution, veg_slices, non_veg_slices

def main():
    num_people = int(input("Enter the number of people in the group: "))
    num_pizzas = int(input("Enter the number of pizzas ordered: "))
    
    slices_per_pizza = int(input("How many slices does each pizza have? (e.g., 4, 6, 8, or 12): "))
    
    veg_pizzas = int(input("Enter the number of vegetarian pizzas: "))
    non_veg_pizzas = num_pizzas - veg_pizzas
    
    total_slices = num_pizzas * slices_per_pizza
    veg_slices = veg_pizzas * slices_per_pizza
    non_veg_slices = non_veg_pizzas * slices_per_pizza

    # Get pizza preferences and the number of vegetarian-only people
    preferences, vegetarian_people = get_pizza_preferences(num_people)
    
    # Distribute pizzas based on preferences
    pizza_distribution, leftover_veg_slices, leftover_non_veg_slices = distribute_pizzas(preferences, veg_slices, non_veg_slices, vegetarian_people, veg_pizzas, non_veg_pizzas)
    
    # Display results
    print("\nPizza Distribution Results:")
    for person, pizzas in pizza_distribution.items():
        pizza_count = {pizza: pizzas.count(pizza) for pizza in set(pizzas)}  # Count each type of pizza for the person
        print(f"{person}: Received - {', '.join([f'{pizza} ({count} slices)' for pizza, count in pizza_count.items()])}")

    print(f"\nTotal vegetarian slices left: {leftover_veg_slices}")
    print(f"Total non-vegetarian slices left: {leftover_non_veg_slices}")

    # Show preferences for each person
    print("\nPizza Preferences per Person:")
    for person, prefs in preferences.items():
        print(f"{person}: Preferences - {', '.join(prefs) if prefs else 'No preferences'}")

    print(f"\nTotal pizzas: {num_pizzas} (Vegetarian: {veg_pizzas}, Non-vegetarian: {non_veg_pizzas})")
    print(f"Total slices: {total_slices} (Vegetarian slices: {veg_slices}, Non-veg slices: {non_veg_slices})")

if __name__ == "__main__":
    main()
