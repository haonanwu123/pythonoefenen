import os
import sys
import json
import sqlite3

from datetime import datetime
from transaction import Transaction


class FinanceApp:
    def __init__(self, db_name="finance.db"):
        self.connection = sqlite3.connect(os.path.join(sys.path[0], db_name))
        self.cursor = self.connection.cursor()

    def build_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS transactions")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            description TEXT,
                            category TEXT,
                            amount REAL)"""
        )
        self.connection.commit()

    def load_transactions_from_json(self, json_file):
        with open(os.path.join(sys.path[0], json_file), "r", encoding="utf-8") as file:
            json_data = json.load(file)

            for entry in json_data:
                try:
                    date = datetime.strptime(entry["date"], "%d-%m-%Y").date()
                except ValueError:
                    print(f"Invalid date format for ID {entry['ID']}: {entry['date']}")
                    continue  # Skip the current entry if the date is invalid

                description = entry["description"]
                category = entry["category"]
                amount = entry["amount"]

                self.cursor.execute(
                    "INSERT INTO transactions (date, description, category, amount) VALUES (?, ?, ?, ?)",
                    (date, description, category, amount),
                )

                self.connection.commit()

    def add_transaction(self, date, description, category, amount) -> Transaction:
        self.cursor.execute(
            "INSERT INTO transactions (date, description,category, amount) VALUES (?,?,?,?)",
            (date, description, category, amount),
        )
        self.connection.commit()
        transcations_id = self.cursor.lastrowid
        return Transaction(transcations_id, date, description, category, amount)

    def update_transaction(
        self, transaction_id, date, description, category, amount
    ) -> bool:
        update_parts = []
        params = []

        # Add parts to update query only if the field is provided
        if date:
            update_parts.append("date = ?,")
            params.append(date)
        if description:
            update_parts.append("description = ?,")
            params.append(description)
        if category:
            update_parts.append("category = ?,")
            params.append(category)
        if amount is not None:  # Ensure amount is not None before adding
            update_parts.append("amount = ?,")
            params.append(amount)

        # If no fields to update, return False
        if not update_parts:
            print("No fields to update.")
            return False

        # Remove trailing comma from the query
        update_parts = [part.rstrip(",") for part in update_parts]

        # Append transaction ID for WHERE clause
        params.append(transaction_id)

        # Construct the final query
        query = f"UPDATE transactions SET {', '.join(update_parts)} WHERE id = ?"

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            # Print the error for debugging
            print(f"SQLite error: {e}")
            return False

    def delete_transaction(self, transaction_id) -> bool:
        try:
            self.cursor.execute(
                "DELETE FROM transactions WHERE id = ?", (transaction_id,)
            )
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def search_transactions(self, term: str) -> list[Transaction]:
        self.cursor.execute(
            "SELECT * FROM transactions WHERE description LIKE ? OR category LIKE ?",
            ("%" + term + "%", "%" + term + "%"),
        )
        transactions = self.cursor.fetchall()
        return [Transaction(*t) for t in transactions]

    def get_transactions(self, year: int | None = None) -> list[Transaction]:
        if year:
            self.cursor.execute(
                "SELECT * FROM transactions WHERE strftime('%Y', date) = ?",
                (str(year),),
            )
        else:
            self.cursor.execute("SELECT * FROM transactions")
        transactions = self.cursor.fetchall()
        return [Transaction(*t) for t in transactions]

    def get_expenses(self, transactions: list[Transaction]) -> list[tuple[str, float]]:
        expense_dict = {}
        for trans in transactions:
            if trans.category != "Work" and trans.category != "Savings":
                expense_dict[trans.category] = expense_dict.get(trans.category, 0) + trans.amount

        sorted_expences = sorted(expense_dict.items(), key=lambda x: x[1], reverse=True)
        total_expences = sum(amount for _, amount in sorted_expences)

        return sorted_expences, total_expences

    def get_savings(self, transactions: list[Transaction]) -> list[tuple[str, float]]:
        return sum(t.amount for t in transactions if t.category == "Savings")

    def count_transactions(self, year: int | None = None) -> int:
        if year:
            self.cursor.execute(
                "SELECT COUNT(*) FROM transactions WHERE strftime('%Y', date) = ?",
                (str(year),),
            )
        else:
            self.cursor.execute("SELECT COUNT(*) FROM transactions")
        return self.cursor.fetchone()[0]

    def get_report(self, year: int | None = None) -> dict[str, float]:

        transactions = self.get_transactions(year)

        income = sum(t.amount for t in transactions if t.category == "Work")
        _, expenses = self.get_expenses(transactions)
        savings = -self.get_savings(transactions)

        total = income + savings + expenses

        report = {
            "transactions": len(transactions),
            "income": round(income, 2),
            "expenses": round(expenses, 2),
            "savings": round(savings, 2),
            "total": round(total, 2),
        }

        return report
