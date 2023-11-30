from game import Game

class Mine:
    def __init__(self, game: Game, cost: int, productivity: int):
        self.game = game
        self.cost = cost
        self.productivity = productivity

    def produce(self):
        return self.productivity

