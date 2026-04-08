import matplotlib.pyplot as plt
from typing import Dict

class Visualizer:

    @staticmethod
    def plot_category_breakdown(breakdown: Dict[str, float]):
        if not breakdown:
            print("No data available to plot.")
            return

        categories = list(breakdown.keys())
        amounts = list(breakdown.values())

        plt.figure(figsize=(10, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Expense Breakdown by Category")
        plt.show()
