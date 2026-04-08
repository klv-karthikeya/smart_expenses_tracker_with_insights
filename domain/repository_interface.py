from abc import ABC, abstractmethod
from typing import List
from domain.entities import Expense

class IExpenseRepository(ABC):
    
    @abstractmethod
    def save(self, expense: Expense) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Expense]:
        pass
