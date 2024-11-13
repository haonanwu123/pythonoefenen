# Base class for common functionality between Car and Motorcycle
class Vehicle:
    def __init__(self, brand: str, model: str, color: str, price: float) -> None:
        self.brand = brand
        self.model = model
        self.color = color
        self.price = price
        self.sold = False
        self.sold_to = None

    def sell(self, customer: "Customer") -> None:
        self.sold = True
        self.sold_to = customer

    def print(self) -> None:
        print(f"Brand: {self.brand}")
        print(f"Model: {self.model}")
        print(f"Color: {self.color}")
        print(f"Price: {self.price}")
        if self.sold:
            print(f"Sold to: {self.sold_to.name}")
        else:
            print("Not sold yet")


# Car class inherits from Vehicle
class Car(Vehicle):
    pass


# Motorcycle class inherits from Vehicle
class Motorcycle(Vehicle):
    pass


# Customer class
class Customer:
    def __init__(self, name: str) -> None:
        self.name = name

    def print(self) -> None:
        print(f"Name: {self.name}")


def main():
    pass


if __name__ == "__main__":
    main()
