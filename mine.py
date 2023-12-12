class Mine:
    def __init__(self, cost: int, productivity: int):
        """Constructor"""
        self.cost = cost
        self.productivity = productivity

    def r_cost(self):
        """Return the cost of the mine"""
        return self.cost

    def produce(self):
        """Return the productivity of the mine"""
        return self.productivity

