import random

def arithmetic_operation(arithmetic_type):
    mistakes = []

    for _ in range(10):
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)

        if arithmetic_type == 'summation':
            correct_answer = num1 + num2
            user_answer = int(input(f"{num1} + {num2} = "))
        
        elif arithmetic_type == 'subtraction':
            correct_answer = num1 - num2
            user_answer = int(input(f"{num1} - {num2} = "))
        
        elif arithmetic_type == 'multiplication':
            correct_answer = num1 * num2
            user_answer = int(input(f"{num1} * {num2} = "))
        
        else:
            print("Invalid arithmetic type.")
            return

        if user_answer != correct_answer:
            mistakes.append(f"{num1} {'+' if arithmetic_type == 'summation' else '-' if arithmetic_type == 'subtraction' else '*'} {num2} = {user_answer} (correct: {correct_answer})")

    if mistakes:
        print("\n### MISTAKES ###")
        for mistake in mistakes:
            print(mistake)
    else:
        print("\nGreat job! No mistakes made!")


def main():
    print("Welcome to the Arithmetic Practice Program!")
    arithmetic_type = input("What type of arithmetic do you want to practice? (summation, subtraction, multiplication): ").strip().lower()
    arithmetic_operation(arithmetic_type)


if __name__ == "__main__":
    main()