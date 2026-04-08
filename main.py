from infrastructure.csv_repository import CsvExpenseRepository
from use_cases.expense_service import ExpenseService
from presentation.cli import ExpenseCLI

def main():
    DATA_FILE = "data/expenses.csv"

    repository = CsvExpenseRepository(DATA_FILE)
    service = ExpenseService(repository)
    app = ExpenseCLI(service)

    app.run()

if __name__ == "__main__":
    main()
