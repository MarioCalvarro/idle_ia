from game import Game
from ia import IdleGeneticProblem

def main():
    duration = 90
    game = Game()
    
    ai = IdleGeneticProblem

    player = ai.genetic_algorithm()
    
    print("{}", player.value)

if __name__ == "__main__":
    main()
