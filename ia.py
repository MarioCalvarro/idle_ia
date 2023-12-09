import random
import math
from mine import Mine
from game import Game

MINES: list[Mine] = [Mine(15, 1), Mine(100, 5), Mine(300, 20), Mine(2000, 100), Mine(15000, 700), Mine(250000, 10000)]

# Representación: Array de arrays. Cada segundo será un vector con len(MINES) elementos (6 por defecto).
#                 Cada elemento es un entero que representa el número de minas de ese
#                 tipo que se compran en ese segundo
#
# Población inicial: Aleatoria con crecimiento exponencial
# Función de evaluación: Si intenta comprar algo imposible -> lo hacemos posible, pero 
#                       añadimos un multiplicador que disminuya el fitness al final
#                        Al llegar al final -> el total de oro que tenga al final
# Operadores:
#  * Selección: Por torneo probabilística
#  * Cruze: Dividir cada vector de la matriz en tres y elegir que padre tendrá cada tercio
#  * Mutación: Elegir un 0.2% de los segundos y sobre cada mutar con una probabilidad cada cantidad
#              multiplicando por 0.5.

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
        """Construct the initial list of values of the individual"""        
        l: list[list[int]] = []
        for i in range(self.seconds - 20):
            aux: list[int] = []
            for ii in range(len(MINES)):     # One for each type of mine
                number: int = int(random.randint(0, 1) * 1.045 **(i-90))
                number = round(number * 3**(-6.5*ii))
                aux.append(number)

            l.append(aux)
        for i in range(20):
            aux = [0] * 6
            l.append(aux)

        return l


    def mutation(self):
        prop_mut = 0.002
        number_mutations: int = round(len(self.values) * prop_mut)
        to_mutate: list[int] = []
        
        for _ in range(number_mutations):
            to_mutate.append(random.randint(0, len(self.values) - 15))
     
        for index in to_mutate:
            self.mutate_index(index)


    def mutate_index(self, index: int):
        for i in range(len(MINES)):
            prob: float = (1 - 1.005 ** (-index)) / 5**i

            if prob > random.uniform(0, 1):
                self.values[index][i] += round(self.values[index][i] * 0.5)

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
        mult: float = 1;
        for i, second_array in enumerate(self.values):
            game.increase_gold()
            for ii, num_mines in enumerate(second_array):
                valid: tuple[int, bool] = game.new_mines(MINES[ii], num_mines)
                if not valid[0]:
                    mult *= 0.9 # Invalids have worse fitness
                    self.values[i][ii] = valid[1]


        self.fitness = int(game.gold * mult)
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


    def genetic_algorithm(self, num_tour: int, num_gens: int, proportion_cross: float) -> tuple[IdleIndividual, int]:
        """Return best buying sequence"""
        num_parents = round(self.size * proportion_cross)
        num_parents = round(num_parents if num_parents % 2 == 0 else num_parents - 1)
        num_direct = self.size - num_parents
        for _ in range(num_gens):
            best_ind: IdleIndividual = max(self.population, key = self.fitness)
            self.best_before = best_ind
            # if(best_ind.fitness > 0):
            #     print(f"{math.log(best_ind.fitness, 10)}")
            # else:
            #     print (best_ind.fitness)
            self.population = self.new_generation(num_tour, num_parents, num_direct)

        best_ind: IdleIndividual = max(self.population, key = self.fitness)
        return best_ind, self.fitness(best_ind)

    def tournament_selection(self, n, k):
        """Selection by tournament of n individuals grouped in sets of k members"""
        selected: list[IdleIndividual] = []
        for _ in range(n):
            participants = random.sample(self.population, k)
            ind_selected = max(participants, key = self.fitness)
            
            selected.append(ind_selected)
        return selected  

    def cross_parents(self, parents: list[IdleIndividual]):
        l = []
        for i in range(len(parents)//2):    #asumimos que la población de la que partimos tiene tamaño par
            desc = self.cross(parents[2*i], parents[2*i + 1])   #El cruce se realiza con la función de cruce proporcionada por el propio problema genético

            l.append(desc[0]) #La población resultante se obtiene de cruzar el padre[0] con padre[1], padre[2] con padre[3]...
            l.append(desc[1]) #y añadir cada par de descendientes a la nueva población
        return l

    def mutate_ind(self, generation: list[IdleIndividual]):
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
        for _ in range(self.size):  #Añadimos a la población size individuos
            l.append(IdleIndividual(self.seconds, True)) 
        return l

