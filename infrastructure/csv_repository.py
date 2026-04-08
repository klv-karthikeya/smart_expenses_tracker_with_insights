import csv
import os
from datetime import datetime
from typing import List
from domain.entities import Expense
from domain.repository_interface import IExpenseRepository

class CsvExpenseRepository(IExpenseRepository):

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._initialize_storage()

    def _initialize_storage(self):
        if not os.path.exists(self._file_path):
            os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
            with open(self._file_path, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
                writer.writeheader()

    def save(self, expense: Expense) -> None:
        with open(self._file_path, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
            writer.writerow(expense.to_dict())

    def get_all(self) -> List[Expense]:
        expenses = []
        if not os.path.exists(self._file_path):
            return expenses
        
        with open(self._file_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expenses.append(Expense(
                    date=datetime.fromisoformat(row['date']).date(),
                    category=row['category'],
                    amount=float(row['amount']),
                    description=row['description']
                ))
        return expenses
