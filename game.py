from mine import Mine

class Game:
    def __init__(self):
        self.mines: list = [] #TODO: Tal vez no necesario
        self.gold: int = 0
        self.productivity: int = 1

    def increase_gold(self):
        self.gold += self.productivity

    def new_mines(self, mine: Mine, num: int) -> bool:
        if num < 0:
            return False

        cost: int = mine.cost * num
        if self.gold >= cost:
            self.gold -= cost
            self.productivity += mine.produce() * num
            return True
        else:
            return False
