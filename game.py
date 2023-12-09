from mine import Mine

class Game:
    def __init__(self):
        self.gold: int = 0
        self.productivity: int = 1

    def increase_gold(self):
        self.gold += self.productivity

    def new_mines(self, mine: Mine, num: int) -> tuple[int, bool]:
        """Return the max number of mines that can be bought and if it was valid"""
        if num < 0:
            return 0, False

        cost: int = mine.cost * num
        if self.gold >= cost:
            self.gold -= cost
            self.productivity += mine.produce() * num
            return num, True
        else:
            buyed = self.gold // mine.cost
            self.gold = self.gold % mine.cost
            return num - buyed, False
