from ia import IdleGeneticProblem

duration = 900
population_size = 20
k = 3
num_gen = 200
prop_cr = 0.8

def main():
    ai = IdleGeneticProblem(population_size, duration)

    _, val = ai.genetic_algorithm(k, num_gen, prop_cr)

    print(f"The best individual is: {val}")

if __name__ == "__main__":
    main()
