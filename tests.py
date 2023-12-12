import multiprocessing
import math
from ia import IdleGeneticProblem

# Parameters of the algorithm
duration = 900
population_size = 20
k = 3
num_gen = 200
prop_cr = 0.8

def worker_function():
    return IdleGeneticProblem(population_size, duration).genetic_algorithm(k, num_gen, prop_cr)[1]

def main():
    """Execute paralelly a number of instances of the genetic algorithm"""
    # Multiproceso
    num_ej = 100    # Number of executions

    # Create a Pool of processes
    pool = multiprocessing.Pool()

    # Apply worker function to each number using apply_async()
    results = []
    for _ in range(num_ej):
        result = pool.apply_async(worker_function, args=())
        results.append(result)

    # Get the return values from all the processes and do the mean
    final_results = sum([res.get() for res in results]) / num_ej

    # Close the pool
    pool.close()
    pool.join()

    print(f"Results: {math.log(final_results, 10)}")

if __name__ == '__main__':
    main()
