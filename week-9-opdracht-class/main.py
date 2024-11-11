class Person:
    def __init__(self, age: int, name: str) -> None:
        self.age = age
        self.name = name

    def celebrate_birthday(self) -> int:
        self.age += 1
        print(f"Happy birthday {self.name}! You are now {self.age} years old.")


class BankAccount:
    def __init__(
        self, balance: float, account_number: str, account_holder: str
    ) -> None:
        self.balance = balance
        self.account_number = account_number
        self.account_holder = account_holder

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance is ${self.balance}")
        else:
            print("Invalid deposit amount. Please enter a positive number.")

    def withdraw(self, amount: float) -> float:
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                print(f"Withdrew ${amount}. New balance is ${self.balance}")
            else:
                print("Insufficient funds.")
        else:
            print("Invalid withdrawal amount. Please enter a positive number.")


class Book:
    def __init__(self, title: str, author: str, price: float) -> None:
        self.title = title
        self.author = author
        self.price = price

    def apply_discount(self, discount: int) -> int:
        if discount > 0:
            self.price = self.price - (self.price * discount / 100)
            print(
                f"Discount applied. New price of {self.title} from {self.author} is ${self.price}"
            )
        else:
            print("Discount must be a positive number")


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        if self.width > 0 and self.height > 0:
            area = self.width * self.height
            print(f"Area of the rectangle is {area} square units.")
        else:
            print("Width and height must be positive numbers.")

    def perimeter(self) -> float:
        if self.width > 0 and self.height > 0:
            perimeter = 2 * (self.width + self.height)
            print(f"Perimeter of the rectangle is {perimeter} units.")
        else:
            print("Width and height must be positive numbers.")


class Car:
    def __init__(self, brand: str, model: str, mileage: int) -> None:
        self.brand = brand
        self.model = model
        self.mileage = mileage

    def drive(self, kilometers: int) -> int:
        if kilometers > 0:
            self.mileage += kilometers
            print(
                f"You have driven {kilometers} kilometers with your {self.brand} model {self.model}. Total mileage is now {self.mileage} km."
            )
        else:
            print("You must drive a positive number of kilometers.")


class Student:
    def __init__(self, name: str, student_id: int, grades: list) -> None:
        self.name = name
        self.student_id = student_id
        self.grades = grades

    def calculate_average(self) -> float:
        if self.grades:
            average = sum(self.grades) / len(self.grades)
            round(average, 2)
            print(f"Average grade of {self.name} id {self.student_id} is {average}.")
        else:
            print("This student has not grades yet.")


class Library:
    def __init__(self) -> None:
        self.books = []

    def add_book(self, book: str) -> str:
        if book in self.books:
            print(f"Book {book} is already in the library.")
        else:
            self.books.append(book)
            print(f"'{book}' has added from the library.")

    def remove_book(self, book: str) -> str:
        if book in self.books:
            self.books.remove(book)
            print(f"'{book}' has removed from the library.")
        else:
            print(f"'{book}' is not in the library.")

    def list_books(self) -> list:
        if self.books:
            print("Books are in library:")
            for book in self.books:
                print(f"- {book}")
        else:
            print("the library is empty.")


class Employee:
    def __init__(self, name: str, position: str, salary: float) -> None:
        self.name = name
        self.position = position
        self.salary = salary

    def promote(self, salary_increase: float) -> float:
        if salary_increase > 0:
            self.salary += salary_increase
            print(
                f"name: {self.name}  position: {self.position}  increased salary: {salary_increase}  new salary: {self.salary}"
            )
        else:
            print("Salary increase must be positive.")


class ShoppingCart:
    def __init__(self) -> None:
        self.items = []

    def add_item(self, item: dict) -> None:
        self.items.append(item)
        print(f"Item added: {item['name']} - ${item['price']}")

    def remove_item(self, item_name: str) -> None:
        found = False
        for item in self.items:
            if item["name"] == item_name:
                self.items.remove(item)
                print(f"Item removed: {item_name}")
                found = True
                break
        if not found:
            print(f"Item not find: {item_name}")

    def calculate_total(self) -> None:
        total = sum(item["price"] for item in self.items)
        print(f"Total: ${total:.2f}")

    def list_items(self) -> None:
        if self.items:
            print("Items in shoppingcarts:")
            for item in self.items:
                print(f"- {item['name']}: ${item['price']}")
        else:
            print("the shoppingcarts is empty.")


class Ticket:
    def __init__(self, event_name: str, seat_number: str, price: float) -> None:
        self.event_name = event_name
        self.seat_number = seat_number
        self.price = price

    def apply_discount(self, discount_percentage: float) -> None:
        if 0 <= discount_percentage <= 100:
            discount_amount = self.price * (discount_percentage / 100)
            self.price -= discount_amount
            print(
                f"Discount from {discount_percentage}% is added. New price is ${self.price:.2f}"
            )
        else:
            print("Discount number must between 0 and 100")

    def __str__(self) -> str:
        return f"Event: {self.event_name}, Seat: {self.seat_number}, Price: ${self.price:.2f}"


def main():
    print(f"question1:")
    person = Person(20, "Martin")
    person.celebrate_birthday()

    print(f"\nquestion2:")
    account = BankAccount(1000, "NL01BANK0123456789", "Alice")
    account.deposit(200)
    account.withdraw(500)
    account.withdraw(800)

    print(f"\nquestion3:")
    book = Book("Python Programming", "John Smith", 50.0)
    book.apply_discount(10)

    print(f"\nquestion4:")
    rectangle = Rectangle(5.0, 10.0)
    rectangle.area()
    rectangle.perimeter()

    print(f"\nquestion5:")
    car = Car("Toyota", "Camry", 20)
    car.drive(50)

    print(f"\nquestion6:")
    student = Student("John Doe", 12345, [90, 80, 70, 100])
    student.calculate_average()

    print(f"\nquestion7:")
    library = Library()
    library.add_book("Python Programming")
    library.add_book("1987")
    library.add_book("Three Days to See")
    library.list_books()
    library.remove_book("Python Programming")
    library.list_books()

    print(f"\nquesiton8:")
    employee = Employee("Jan Jansen", "Junior Developer", 3500)
    employee.promote(500)

    print(f"\nquestion9:")
    cart = ShoppingCart()
    cart.add_item({"name": "Laptop", "price": 1000})
    cart.add_item({"name": "Smartphone", "price": 600})
    cart.add_item({"name": "Muis", "price": 30})
    cart.list_items()
    cart.calculate_total()
    cart.remove_item("Smartphone")
    cart.list_items()
    cart.calculate_total()

    print(f"\nquestion10:")
    ticket = Ticket("Concert", "A12", 100.0)
    print(ticket)
    ticket.apply_discount(15)
    print(ticket)
    ticket.apply_discount(120)


if __name__ == "__main__":
    main()
