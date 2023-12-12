from mine import Mine

class Game:
    def __init__(self):
        """Constructor"""
        self.gold: int = 0
        self.productivity: int = 1

    def increase_gold(self):
        """Increase the gold based on the current productivity"""
        self.gold += self.productivity

    def new_mines(self, mine: Mine, num: int) -> bool:
        """Return if it is possible to buy 'num' 'mine's. If it is, buy them
           and increase the productivity accordingly"""
        if num < 0:
            return False

        cost: int = mine.cost * num
        if self.gold >= cost:
            self.gold -= cost
            self.productivity += mine.produce() * num
            return True
        else:
            return False
