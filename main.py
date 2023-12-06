from ia import IdleGeneticProblem

def main():
    duration = 900
    population_size = 10
    
    ai = IdleGeneticProblem(population_size, duration)

    ind, val = ai.genetic_algorithm(3, 1000, 0.7)

    print("The best val is {}", val)

if __name__ == "__main__":
    main()
