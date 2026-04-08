from infrastructure.json_repository import JsonExpenseRepository
from use_cases.expense_service import ExpenseService
from presentation.cli import ExpenseCLI

def main():
    repository = JsonExpenseRepository("expenses.json")
    service = ExpenseService(repository)
    app = ExpenseCLI(service)

    app.run()

if __name__ == "__main__":
    main()
