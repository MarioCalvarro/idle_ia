from mine import Mine

class Game:
    def __init__(self):
        self.mines: list = [] #TODO: Tal vez no necesario
        self.gold: int = 0
        self.productivity: int = 1

    def increase_gold(self):
        self.gold += self.productivity

    def new_mine(self, mine: Mine):
        self.mines.append(mine)
        self.productivity += mine.produce()
