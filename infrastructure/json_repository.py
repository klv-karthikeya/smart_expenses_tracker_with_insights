import json
import os
from datetime import datetime
from typing import List
from domain.entities import Expense
from domain.repository_interface import IExpenseRepository

class JsonExpenseRepository(IExpenseRepository):

    def __init__(self, file_path: str):
        self._file_path = file_path

    def save(self, expense: Expense) -> None:
        expenses = self.get_all()
        expenses.append(expense)
        with open(self._file_path, 'w') as f:
            json.dump([e.to_dict() for e in expenses], f, indent=4)

    def get_all(self) -> List[Expense]:
        if not os.path.exists(self._file_path):
            return []
        
        with open(self._file_path, 'r') as f:
            try:
                data = json.load(f)
                return [Expense(
                    date=datetime.fromisoformat(item['date']).date(),
                    category=item['category'],
                    amount=item['amount'],
                    description=item['description']
                ) for item in data]
            except json.JSONDecodeError:
                return []
