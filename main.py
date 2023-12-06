from ia import IdleGeneticProblem

def main():
    duration = 90
    population_size = 100
    
    ai = IdleGeneticProblem(population_size, duration)

    ind, val = ai.genetic_algorithm(3, 100, 0.7)

    print("The best val is", val)

if __name__ == "__main__":
    main()
