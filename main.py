import math
from ia import IdleGeneticProblem

def main():
    duration = 900
    population_size = 20

    ai = IdleGeneticProblem(population_size, duration)

    ind, val = ai.genetic_algorithm(4, 100, 0.9)

    with open('pruebas.txt', 'a') as file:
        file.write(f"The best ind has val {val} {math.log(val, 10)}\n")

if __name__ == "__main__":
    main()
