from databasemanager import DatabaseManager


class SalesManager:
    def __init__(self, databasemanager: DatabaseManager) -> None:
        self.db = databasemanager

    def get_sale(self, sale_id: int) -> tuple:
        query = "SELECT * FROM sales WHERE id = ?;"
        return self.db.fetchone(
            query,
            (sale_id,),
        )

    def add_sale(
        self, date: str, product_id: int, customer_id: int, quantity: int, price: float
    ) -> int:
        query = "INSERT INTO sales (date, product_id, customer_id, quantity, price) VALUES (?,?,?,?,?)"
        return self.db.insert(
            query,
            (
                date,
                product_id,
                customer_id,
                quantity,
                price,
            ),
        )

    def update_sale(
        self,
        sale_id: int,
        date: str,
        product_id: int,
        customer_id: int,
        quantity: int,
        price: float,
    ) -> bool:
        query = "UPDATE sales SET date = ?, product_id = ?, customer_id = ?, quantity = ?, price = ? WHERE id = ?"
        return self.db.update(
            query, (date, product_id, customer_id, quantity, price, sale_id)
        )

    def delete_sale(self, sale_id: int) -> bool:
        query = "DELETE FROM sales WHERE id = ?"
        return self.db.delete(query, (sale_id,))

    def get_customer(self, customer_id: int) -> tuple:
        query = "SELECT * FROM customers WHERE id = ?"
        return self.db.fetchone(query, (customer_id,))

    def add_customer(self, name: str, email: str) -> int:
        query = "INSERT INTO customers (name, email) VALUES (?, ?)"
        return self.db.insert(query, (name, email))

    def update_customer(self, customer_id: int, name: str, email: str) -> bool:
        query = "UPDATE customers SET name = ?, email = ? WHERE id = ?"
        return self.db.update(query, (name, email, customer_id))

    def delete_customer(self, customer_id: int) -> bool:
        query = "DELETE FROM customers WHERE id = ?"
        return self.db.delete(query, (customer_id,))

    def get_product(self, product_id: int) -> tuple:
        query = "SELECT * FROM products WHERE id = ?"
        return self.db.fetchone(query, (product_id,))

    def add_product(self, name: str, category: str) -> int:
        query = "INSERT INTO products (name, category) VALUES (?, ?)"
        return self.db.insert(query, (name, category))

    def update_product(self, product_id: int, name: str, category: str) -> bool:
        query = "UPDATE products SET name = ?, category = ? WHERE id = ?"
        return self.db.update(query, (name, category, product_id))

    def delete_product(self, product_id: int) -> bool:
        query = "DELETE FROM products WHERE id = ?"
        return self.db.delete(query, (product_id,))
