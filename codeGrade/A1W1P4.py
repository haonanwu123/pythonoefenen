def calculate_total_weight():
    WIDGET_WEIGHT = 75
    GIZMO_WEIGHT = 112

    try:
        num_widgets = int(input("Number of widgets: "))
        num_gizmos = int(input("Number of gizmos: "))

        total_weight = (num_widgets * WIDGET_WEIGHT) + (num_gizmos * GIZMO_WEIGHT)

        print(f"The Total Weight of the Order: {total_weight} grams")
    
    except ValueError:
        print("Invalid input. Please enter numeric values for the number of widgets and gizmos.")

calculate_total_weight()