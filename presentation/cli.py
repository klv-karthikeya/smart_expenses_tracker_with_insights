import os
from datetime import datetime
from typing import List
from use_cases.expense_service import ExpenseService
from presentation.visualizer import Visualizer

class ExpenseCLI:

    def __init__(self, service: ExpenseService):
        self._service = service

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_menu(self):
        print("\n--- Smart Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Monthly Summary")
        print("3. View Category Breakdown (Chart)")
        print("4. Get Spending Insights")
        print("5. Exit")

    def run(self):
        while True:
            self._print_menu()
            choice = input("Select an option: ")

            if choice == '1':
                self._add_expense_flow()
            elif choice == '2':
                self._view_summary_flow()
            elif choice == '3':
                self._view_chart_flow()
            elif choice == '4':
                self._view_insights_flow()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    def _add_expense_flow(self):
        try:
            date_str = input("Enter date (YYYY-MM-DD) [Leave blank for today]: ")
            if not date_str:
                date_val = datetime.now().date()
            else:
                date_val = datetime.strptime(date_str, "%Y-%m-%d").date()

            category = input("Enter category (e.g. Food, Travel, Bills): ").strip()
            amount = float(input("Enter amount: "))
            description = input("Enter description: ").strip()

            self._service.add_expense(date_val, category, amount, description)
            print("Expense added successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def _view_summary_flow(self):
        try:
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year (YYYY): "))
            total = self._service.get_monthly_summary(month, year)
            print(f"\nTotal expenses for {month}/{year}: ${total:.2f}")
        except Exception as e:
            print(f"Error: {e}")

    def _view_chart_flow(self):
        breakdown = self._service.get_category_breakdown()
        if not breakdown:
            print("No expenses found.")
            return
        
        try:
            print("Generating chart...")
            Visualizer.plot_category_breakdown(breakdown)
        except Exception as e:
            print("\nError generating chart. Ensure matplotlib is installed.")
            print(f"Breakdown: {breakdown}")

    def _view_insights_flow(self):
        insights = self._service.get_insights()
        if not insights["highest_spending_category"]:
            print("No data available for insights.")
        else:
            print("\n--- Spending Insights ---")
            print(f"Highest Spending Category: {insights['highest_spending_category']}")
            print(f"Amount Spent: ${insights['highest_amount']:.2f}")
