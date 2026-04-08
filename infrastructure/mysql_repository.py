import mysql.connector
from datetime import date
from typing import List
from domain.entities import Expense
from domain.repository_interface import IExpenseRepository

class MySqlExpenseRepository(IExpenseRepository):

    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self._initialize_db()

    def _initialize_db(self):
        conn = mysql.connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
        conn.close()

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                category VARCHAR(100) NOT NULL,
                amount DOUBLE NOT NULL,
                description TEXT
            )
        """)
        conn.close()

    def _get_connection(self):
        return mysql.connector.connect(**self.config)

    def save(self, expense: Expense) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (expense.date, expense.category, expense.amount, expense.description))
        conn.commit()
        conn.close()

    def get_all(self) -> List[Expense]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, category, amount, description FROM expenses")
        rows = cursor.fetchall()
        expenses = [Expense(row[0], row[1], row[2], row[3]) for row in rows]
        conn.close()
        return expenses
