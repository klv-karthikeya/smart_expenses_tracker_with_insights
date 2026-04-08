class Expense:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }
