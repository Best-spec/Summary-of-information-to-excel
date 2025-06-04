# Example model, extend as needed
class Summary:
    def __init__(self, users, sales, growth):
        self.users = users
        self.sales = sales
        self.growth = growth

    def to_dict(self):
        return {
            "users": self.users,
            "sales": self.sales,
            "growth": self.growth
        }
