import random
import math
import threading
from typing import Tuple
from mine import Mine
from game import Game

MINES: list[Mine] = [Mine(15, 1), Mine(100, 5), Mine(300, 20), Mine(2000, 100), Mine(15000, 700), Mine(250000, 10000)]

# TODO: Change numbers to constants

# Representación: Array de arrays. Cada segundo será un vector con len(MINES) elementos (6 por defecto).
#                 Cada elemento es un entero que representa el número de minas de ese
#                 tipo que se compran en ese segundo
#
# Población inicial: Aleatoria con valores bajos
# Función de evaluación: Si intenta comprar algo imposible -> -1
#                        Si llega al final -> el total de oro que tenga al final
# Operadores:
#  * Selección: Por torneo probabilística
#  * Cruze: Dividir cada vector de la matriz en dos y elegir que padre tendrá la primera mitad de dicha particición
#  * Mutación: Elegir un 10% de los segundos y sobre cada uno sumar o restar a cada mina una cantidad
#              que dependa de su coste (las minas baratas tendrán más variabilidad)

class IdleIndividual():
    BASE_RANGE_MUTATION = 1.04

    def __init__(self, seconds: int, initial: bool):
        self.seconds = seconds
        self.fitness: int = -2
        if initial:
            self.values: list[list[int]] = self.create_new_values()
        else:
            self.values: list[list[int]] = [[]] * seconds



    def create_new_values(self):
        l: list[list[int]] = []
        for i in range(self.seconds - 20):
            aux: list[int] = []
            for ii in range(len(MINES)):     # One for each type of mine
                #number: int = int(random.randint(0, 1) * 1.4 ** (0.07 * (i-100)))
                number: int = int(random.randint(0, 1) * 1.04 ** (i-70))
                number = round(number * 2**(-20*ii))
                aux.append(number)

            l.append(aux)
        for i in range(20):
            aux = [0] * 6
            l.append(aux)

        return l


    def mutation(self):
        prop_mut = 0.01
        if 0.01 > random.uniform(0, 1):
            prop_mut = 0.5
        number_mutations: int = round(len(self.values) * prop_mut)
        to_mutate: list[int] = []
        
        for _ in range(number_mutations):
            to_mutate.append(random.randint(0, len(self.values) - 20))
        
        for index in to_mutate:
            self.mutate_index(index)


    def mutate_index(self, index: int):
        #new_base_range_mutation: int = round(self.BASE_RANGE_MUTATION ** (0.072 * index))
        #new_base_range_mutation: int = round(self.BASE_RANGE_MUTATION ** (index))
        if 0.99 > random.uniform(0, 1):
            for i in range(len(MINES)):
                prob: float = (1 - 2 ** (-index)) / 2**(100*(i+1))
                if prob > random.uniform(0, 1):
                    self.values[index][i] += round(self.values[index][i] * 0.5);
                    # ra: int = random.randint(-new_base_range_mutation, new_base_range_mutation)
                    # #print(f"{prob} {index} {i} {new_base_range_mutation} {ra}")
                    # self.values[index][i] += ra
                    # self.values[index][i] = max(0, self.values[index][i])

                # new_base_range_mutation = round(new_base_range_mutation / (2 ** (20*(i+1))))
        else:
            self.values = [[0, 0, 0, 0, 0, 0]] * self.seconds

    def cross(self, other: 'IdleIndividual') -> 'IdleIndividual':
        l: int = len(self.values) # Is equal in both
        new_ind: IdleIndividual = IdleIndividual(self.seconds, False)
        for i in range(self.seconds):
            if 0.5 > random.uniform(0, 1):
                new_ind.values[i] = self.values[i][0:l//3] + other.values[i][l//3:2*l//3] + self.values[i][2*l//3:l]
            else:
                new_ind.values[i] = other.values[i][0:l//3] + self.values[i][l//3:2*l//3] + other.values[i][2*l//3:l]
        return new_ind


    def evaluation(self) -> int:
        if self.fitness != -2:
            return self.fitness

        game: Game = Game()
        for second_array in self.values:
            game.increase_gold()
            for i, num_mines in enumerate(second_array):
                valid: bool = game.new_mines(MINES[i], num_mines)
                if not valid:
                    self.fitness = -1
                    return -1

        self.fitness = game.gold
        return self.fitness





class IdleGeneticProblem():
    def __init__(self, size: int, seconds: int):
        """Constructor"""
        self.size = size    # Size of the population
        self.seconds = seconds
        self.population = self.starting_generation()
        self.best_before = IdleIndividual(seconds, True)

    def decode(self):
        """Return the phenotype given a genotype"""


    def mutate(self, individual: IdleIndividual):
        """Return a new individual from a previous one with
            a posible mutation"""
        individual.mutation();


    def cross(self, individual1: IdleIndividual, individual2: IdleIndividual) -> list[IdleIndividual]:
        """Return the cross of two individuals"""
        return [individual1.cross(individual2), individual2.cross(individual1)]


    def fitness(self, individual: IdleIndividual) -> int:
        """Return the fitness of a given individual"""
        return individual.evaluation()


    def evaluate_population(self):
        """Parallel evaluation of population"""
        threads = []
        for ind in self.population:
            thread = threading.Thread(target=ind.evaluation, args=())
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join() 


    def genetic_algorithm(self, num_tour: int, num_gens: int, proportion_cross: float) -> Tuple[IdleIndividual, int]:
        """Return best buying sequence"""
        num_parents = round(self.size * proportion_cross)
        num_parents = round(num_parents if num_parents % 2 == 0 else num_parents - 1)
        num_direct = self.size - num_parents
        for i in range(num_gens):
            best_ind: IdleIndividual = max(self.population, key = self.fitness)
            self.best_before = best_ind
            print(f"Best from {i} generation: {best_ind.values}")
            print(f"{math.log(best_ind.fitness, 10)}")
            self.population = self.new_generation(num_tour, num_parents, num_direct)
            self.evaluate_population()

        best_ind: IdleIndividual = max(self.population, key = self.fitness)
        #best = problema_genetico.decodifica(best_cr)
        return best_ind, self.fitness(best_ind)

    def tournament_selection(self, n, k):
        """Selection by tournament of n individuals grouped in sets of k members"""
        selected: list[IdleIndividual] = []
        for _ in range(n):
            participants = random.sample(self.population, k)
            if 0.8 > random.uniform(0, 1):
                ind_selected = max(participants, key = self.fitness)
                if ind_selected.fitness == -1 and 0.2 > random.uniform(0, 1):
                    ind_selected = IdleIndividual(self.seconds, True) # if the ind is invalid, we create a new one
            else:
                ind_selected = min(participants, key = self.fitness)
            selected.append(ind_selected)
        return selected  

    def cross_parents(self, parents: list[IdleIndividual]):
        l = []
        for i in range(len(parents)//2):# asumimos que la población de la que partimos tiene tamaño par
            desc = self.cross(parents[2*i], parents[2*i + 1]) # El cruce se realiza con la función de cruce  
                                                                         # proporcionada por el propio problema genético
            l.append(desc[0]) # La población resultante se obtiene de cruzar el padre[0] con padre[1], padre[2] con padre[3]...
            l.append(desc[1]) # y añadir cada par de descendientes a la nueva población
        return l

    def mutate_ind(self, generation: list[IdleIndividual]):
        # problema_genetico.muta(x,prob) para todos los individuos de la poblacion.
        l = []
        for i in generation:
            self.mutate(i)
            l.append(i)
        return l

    def new_generation(self, num_tour: int, num_parents: int, num_direct: int) -> list[IdleIndividual]:
        parents = self.tournament_selection(num_parents, num_tour) 
        directs = self.tournament_selection(num_direct, num_tour)
        cruces =  self.cross_parents(parents)
        generation = directs + cruces
        result_mut = self.mutate_ind(generation)
        return result_mut


    def starting_generation(self):
        """Return a new generation"""
        l: list[IdleIndividual] = [] 
        for _ in range(self.size): # añadimos a la población size individuos
            l.append(IdleIndividual(self.seconds, True)) 
        return l

