from typing import List, Dict
from datetime import date
from domain.entities import Expense
from domain.repository_interface import IExpenseRepository

class ExpenseService:

    def __init__(self, repository: IExpenseRepository):
        self._repository = repository

    def add_expense(self, date_val: date, category: str, amount: float, description: str) -> None:
        expense = Expense(date_val, category, amount, description)
        self._repository.save(expense)

    def get_all_expenses(self) -> List[Expense]:
        return self._repository.get_all()

    def get_monthly_summary(self, month: int, year: int) -> float:
        expenses = self._repository.get_all()
        return sum(e.amount for e in expenses if e.date.month == month and e.date.year == year)

    def get_category_breakdown(self) -> Dict[str, float]:
        expenses = self._repository.get_all()
        breakdown = {}
        for e in expenses:
            breakdown[e.category] = breakdown.get(e.category, 0.0) + e.amount
        return breakdown

    def get_insights(self) -> Dict[str, any]:
        breakdown = self.get_category_breakdown()
        if not breakdown:
            return {"highest_spending_category": None, "highest_amount": 0.0}
        
        highest_cat = max(breakdown, key=breakdown.get)
        return {
            "highest_spending_category": highest_cat,
            "highest_amount": breakdown[highest_cat]
        }
