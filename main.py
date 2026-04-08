from infrastructure.mysql_repository import MySqlExpenseRepository
from use_cases.expense_service import ExpenseService
from presentation.cli import ExpenseCLI

def main():
    repository = MySqlExpenseRepository(
        host='localhost',
        user='root',
        password='root',
        database='smart_expense_tracker'
    )
    service = ExpenseService(repository)
    app = ExpenseCLI(service)

    app.run()

if __name__ == "__main__":
    main()
