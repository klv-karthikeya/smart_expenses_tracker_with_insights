import os
from datetime import datetime
from typing import List
from use_cases.expense_service import ExpenseService
from presentation.visualizer import Visualizer

class ExpenseCLI:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"

    def __init__(self, service: ExpenseService):
        self._service = service

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_menu(self):
        print(f"\n{self.CYAN}{self.BOLD}================================")
        print(f"   SMART EXPENSE TRACKER v1.0")
        print(f"================================{self.END}")
        print(f"{self.GREEN}1.{self.END} Log New Expense")
        print(f"{self.GREEN}2.{self.END} Monthly Summary")
        print(f"{self.GREEN}3.{self.END} Category Pie Chart")
        print(f"{self.GREEN}4.{self.END} Spending Insights")
        print(f"{self.RED}5.{self.END} Exit System")
        print(f"{self.CYAN}--------------------------------{self.END}")

    def run(self):
        while True:
            self._print_menu()
            choice = input(f"{self.BOLD}Select an option > {self.END}")

            if choice == '1':
                self._add_expense_flow()
            elif choice == '2':
                self._view_summary_flow()
            elif choice == '3':
                self._view_chart_flow()
            elif choice == '4':
                self._view_insights_flow()
            elif choice == '5':
                print(f"\n{self.YELLOW}Shutting down systems... Goodbye!{self.END}")
                break
            else:
                print(f"\n{self.RED}Invalid choice, try again.{self.END}")

    def _add_expense_flow(self):
        try:
            print(f"\n{self.CYAN}--- NEW ENTRY ---{self.END}")
            date_str = input("Date (YYYY-MM-DD) [blank for today]: ")
            if not date_str:
                date_val = datetime.now().date()
            else:
                date_val = datetime.strptime(date_str, "%Y-%m-%d").date()

            category = input("Category (Food, Travel, etc.): ").strip()
            amount = float(input("Amount: "))
            description = input("Description: ").strip()

            self._service.add_expense(date_val, category, amount, description)
            print(f"\n{self.GREEN}{self.BOLD}>> SUCCESS: Expense recorded!{self.END}")
        except Exception as e:
            print(f"\n{self.RED}{self.BOLD}!! ERROR: {e}{self.END}")

    def _view_summary_flow(self):
        try:
            print(f"\n{self.CYAN}--- SUMMARY QUERY ---{self.END}")
            month = int(input("Month (1-12): "))
            year = int(input("Year (YYYY): "))
            total = self._service.get_monthly_summary(month, year)
            print(f"\n{self.YELLOW}{self.BOLD}TOTAL SPENDING ({month}/{year}): ${total:.2f}{self.END}")
        except Exception as e:
            print(f"\n{self.RED}{self.BOLD}!! ERROR: {e}{self.END}")

    def _view_chart_flow(self):
        breakdown = self._service.get_category_breakdown()
        if not breakdown:
            print(f"\n{self.YELLOW}No data available for visualization.{self.END}")
            return
        
        try:
            print(f"\n{self.GREEN}Initializing graphics sequence...{self.END}")
            Visualizer.plot_category_breakdown(breakdown)
        except Exception as e:
            print(f"\n{self.RED}!! Graphics failed. Ensure Matplotlib is installed.{self.END}")

    def _view_insights_flow(self):
        insights = self._service.get_insights()
        if not insights["highest_spending_category"]:
            print(f"\n{self.YELLOW}No data found for insights.{self.END}")
        else:
            print(f"\n{self.CYAN}--- SPENDING INSIGHTS ---{self.END}")
            print(f"{self.BOLD}Highest Category:{self.END} {insights['highest_spending_category']}")
            print(f"{self.BOLD}Total Amount:   {self.END} ${insights['highest_amount']:.2f}")
