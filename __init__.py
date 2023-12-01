from ia import IdleGeneticProblem
from mine import Mine

MINES: list[Mine] = [Mine(15, 1), Mine(100, 5), Mine(300, 20), Mine(2000, 100), Mine(15000, 700), Mine(250000, 10000)]

def main():
    duration = 90
    population_size = 10
    
    ai = IdleGeneticProblem(population_size, duration)
    
    #print("{}", player.value)

if __name__ == "__main__":
    main()
