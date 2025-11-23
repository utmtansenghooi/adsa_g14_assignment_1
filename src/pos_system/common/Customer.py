from datetime import datetime

class Customer:
    def __init__(self, customer_id, name, loyalty_points=0, tier="Bronze", join_date=None):
        self.customer_id = customer_id
        self.name = name
        self.loyalty_points = loyalty_points
        self.tier = tier
        self.join_date = join_date or datetime.now().strftime("%Y-%m-%d")
    
    def __str__(self):
        return f"{self.customer_id}: {self.name}, Points={self.loyalty_points}, Tier={self.tier}"
    
