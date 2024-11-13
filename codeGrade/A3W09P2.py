class Product:
    def __init__(self, name: str, amount: int, price: float) -> None:
        self.name = name
        self.amount = amount
        self.price = price

    def get_price(self, quantity: int) -> float:
        if quantity < 10:
            discount_rate = 0
        elif 10 <= quantity < 100:
            discount_rate = 0.10
        else:
            discount_rate = 0.20

        total_cost = quantity * self.price * (1 - discount_rate)
        return round(total_cost, 2)

    def make_purchase(self, quantity: int) -> bool:
        if quantity > self.amount:
            print("Purchase failed: Insufficient stock.")
            return False
        else:
            self.amount -= quantity
            print(f"Purchase successful. Remaining stock: {self.amount}")
            return True


def main():
    pass


if __name__ == "__main__":
    main()
