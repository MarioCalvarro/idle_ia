import random
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
    BASE_RANGE_MUTATION: int = 10

    def __init__(self, seconds: int, initial: bool):
        if initial:
            self.values: list[list[int]] = self.create_new_values(seconds)
        else:
            self.values: list[list[int]] = [[]] * seconds

        self.seconds = seconds
        self.fitness: int = -2


    def create_new_values(self, seconds: int):
        l: list[list[int]] = []
        for i in range(seconds):
            aux: list[int] = []
            for _ in range(len(MINES)):     # One for each type of mine
                number: int = random.randint(0, 1) * i * 1 // seconds   # TODO: CHANGE Initially buy 0 to 2 mines max
                aux.append(number)

            l.append(aux)
        return l


    def mutation(self):
        number_mutations: int = len(self.values) // 10
        to_mutate: list[int] = [] 
        
        for _ in range(number_mutations):
            to_mutate.append(random.randint(0, len(self.values) - 1))
        
        for index in to_mutate:
            self.mutate_index(index)


    def mutate_index(self, index: int):
        new_base_range_mutation: int = self.BASE_RANGE_MUTATION * index // 90 
        for i in range(len(MINES)): 
            new_base_range_mutation //= 2
            prob: float = 1 / (i+1) * 0.5
            if prob > random.uniform(0, 1):
                self.values[index][i] += random.randint(-new_base_range_mutation, new_base_range_mutation)


    def cross(self, other: 'IdleIndividual') -> 'IdleIndividual':
        l: int = len(self.values) # Is equal in both
        new_ind: IdleIndividual = IdleIndividual(self.seconds, False)
        new_ind.values = self.values[0:l//2] + other.values[l//2:l]
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


    def genetic_algorithm(self, num_tour: int, num_gens: int, proportion_cross: float) -> Tuple[IdleIndividual, int]:
        """Return best buying sequence"""
        num_parents = round(self.size * proportion_cross)
        num_parents = int(num_parents if num_parents % 2 == 0 else num_parents - 1)
        num_direct = self.size - num_parents
        for _ in range(num_gens):
            self.population = self.new_generation(num_tour, num_parents, num_direct)

        best_ind: IdleIndividual = max(self.population, key = self.fitness)
        #best = problema_genetico.decodifica(best_cr)
        return best_ind, self.fitness(best_ind)

    def tournament_selection(self, n, k):
        """Selection by tournament of n individuals grouped in sets of k members"""
        selected: list[IdleIndividual] = []
        for _ in range(n):
            participants = random.sample(self.population, k)
            ind_selected = max(participants, key = self.fitness)
            selected.append(ind_selected)
            # poblacion.remove(seleccionado)
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

