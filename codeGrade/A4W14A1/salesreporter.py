from databasemanager import DatabaseManager


class SalesReporter:
    def __init__(self, databasemanager: DatabaseManager) -> None:
        self.db = databasemanager

    def sales_amount(self) -> int:
        query = "SELECT COUNT(*) FROM sales"
        result_backup = self.db.fetchone(query)
        return result_backup[0]

    def total_sales(self) -> float:
        query = "SELECT SUM(quantity * price) FROM sales"
        result_backup = self.db.fetchone(query)
        return round(result_backup[0], 2) if result_backup[0] else 0.0

    def sales_by_product(self) -> str:
        query = """
            SELECT p.name, SUM(s.quantity), SUM(s.quantity * s.price)
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.id
        """
        rows = self.db.fetchall(query)
        rows = [
            (product_name, quantity, round(sales, 2))
            for product_name, quantity, sales in rows
        ]
        headers = ["Product", "Quantity", "Sales"]
        return self.display_table(headers, rows)

    def sales_by_customer(self) -> str:
        query = """
            SELECT c.name, SUM(s.quantity), SUM(s.quantity * s.price)
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            GROUP BY c.id
        """
        rows = self.db.fetchall(query)
        rows = [
            (customer_name, quantity, round(sales, 2))
            for customer_name, quantity, sales in rows
        ]
        headers = ["Customer", "Quantity", "Sales"]
        return self.display_table(headers, rows)

    def sales_over_time(self) -> str:
        query = """
            SELECT s.date, SUM(s.quantity * s.price)
            FROM sales s
            GROUP BY s.date
        """
        rows = self.db.fetchall(query)
        rows = [(date, round(sales, 2)) for date, sales in rows]
        headers = ["Date", "Sales"]
        return self.display_table(headers, rows)

    def top_selling_products(self, amount: int = 5) -> str:
        query = f"""
            SELECT p.name, SUM(s.quantity)
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.id
            ORDER BY SUM(s.quantity) DESC
            LIMIT {amount}
        """
        rows = self.db.fetchall(query)
        headers = ["Product", "Quantity"]
        return self.display_table(headers, rows)

    def top_customers(self, amount: int = 5) -> str:
        query = f"""
            SELECT c.name, SUM(s.quantity * s.price)
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            GROUP BY c.id
            ORDER BY SUM(s.quantity * s.price) DESC
            LIMIT {amount}
        """
        rows = self.db.fetchall(query)
        rows = [(customer_name, round(sales, 2)) for customer_name, sales in rows]
        headers = ["Customer", "Sales"]
        return self.display_table(headers, rows)

    def display_table(self, headers: list[str], rows: list[tuple]) -> str:
        column_widths: list = [
            max(len(str(item)) for item in column)
            for column in zip(*([headers] + rows))
        ]
        row_format: str = " | ".join(
            ["{{:<{}}}".format(width) for width in column_widths]
        )
        table: list = list()

        table.append(row_format.format(*headers))
        table.append("-+-".join(["-" * width for width in column_widths]))

        for row in rows:
            table.append(row_format.format(*row))

        return "\n".join(table)
