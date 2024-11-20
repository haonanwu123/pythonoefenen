import json
import sys


class MenuManager:
    def __init__(self, file_path):
        """
        Initializes the MenuManager with the provided file path.
        """
        self.menu_data = self.load_menu(file_path)

    def load_menu(self, file_path):
        """
        Loads the menu data from the specified file.
        """
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file {file_path} is not a valid JSON file.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
        return None

    def display_meal_items(self, meal_time):
        """
        Displays the meal items for the specified meal time.
        """
        # Normalize the meal_time to lowercase for case-insensitive comparison
        meal_time = meal_time.lower()

        # Check if the meal time is valid
        valid_meal_times = ["breakfast", "lunch", "dinner"]
        if meal_time not in valid_meal_times:
            print(
                f"Invalid meal time '{meal_time}'. Please choose from 'breakfast', 'lunch', or 'dinner'."
            )
            return

        # Check if menu_data was successfully loaded
        if not self.menu_data:
            print("Error: Menu data could not be loaded.")
            return

        # Check if the selected meal time exists in the menu data
        if meal_time in self.menu_data["menu"]:
            items = self.menu_data["menu"][meal_time]["items"]
            print(f"\n{meal_time.capitalize()} Menu:")
            for item in items:
                print(f"{item['name']}: ${item['price']:.2f}")
        else:
            print(f"No menu found for {meal_time.capitalize()}.")


def main():
    """
    Main function to run the program, accepting the file path and meal time.
    """
    # Default file path (can be overridden by command-line arguments)
    file_path = "json-file-fix/menu_data.json"

    # If a file path is provided via command-line argument, use that
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    menu_manager = MenuManager(file_path)

    # Prompt user for meal time input
    user_input = input("Enter the meal time (breakfast, lunch, or dinner): ")
    menu_manager.display_meal_items(user_input)


if __name__ == "__main__":
    main()
