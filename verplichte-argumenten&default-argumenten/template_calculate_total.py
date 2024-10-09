def calculate_total(price, quantity, discount=0.10):
    # Bereken het totale bedrag zonder korting
    total = price * quantity
    
    # Pas de korting toe
    total_after_discount = total * (1 - discount)
    
    return total_after_discount


def main():
    # Voorbeeld zonder aangepaste korting:
    to_pay = calculate_total(100, 2)
    # Verwachte output: 180.00
    print(f"Te betalen: {to_pay:.2f}")

    # Voorbeeld met aangepaste korting:
    to_pay = calculate_total(50, 3, discount=0.15)
    # Verwachte output: 127.50
    print(f"Te betalen: {to_pay:.2f}")


if __name__ == '__main__':
    main()
