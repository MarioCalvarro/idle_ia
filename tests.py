import multiprocessing
from ia import IdleGeneticProblem

duration = 900
population_size = 20
k = 3
num_gen = 200
prop_cr = 0.8

def worker_function():
    return IdleGeneticProblem(population_size, duration).genetic_algorithm(k, num_gen, prop_cr)[1]

if __name__ == '__main__':
    num_processes = 100

    # Create a Pool of processes
    pool = multiprocessing.Pool()

    # Apply worker function to each number using apply_async()
    results = []
    for i in range(num_processes):
        result = pool.apply_async(worker_function, args=())
        results.append(result)

    # Get the return values from all the processes and do the mean
    final_results = sum([res.get() for res in results]) / num_processes

    # Close the pool
    pool.close()
    pool.join()

    print("Results: ", final_results)
