class Mine:
    def __init__(self, cost: int, productivity: int):
        self.cost = cost
        self.productivity = productivity

    def r_cost(self):
        return self.cost

    def produce(self):
        return self.productivity

