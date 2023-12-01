import random

# Representación: Array de arrays. Cada segundo será un vector con 6 elementos.
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

    def __init__(self, seconds: int):
        self.values: list[list[int]] = self.create_new_values(seconds)
        self.fitness: int = -1

    def create_new_values(self, seconds: int):
        l: list[list[int]] = [[]] * seconds # Create list of `seconds` empty lists
        for i in range(seconds):
            for _ in range(6):     # 6 types of mines
                number: int = random.randint(0, 1) * i * 15 // seconds   # Initially buy 0 to 2 mines max
                l[i].append(number)
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
        #Six because we have 6 types of mines
        for i in range(6):
            new_base_range_mutation //= 2
            prob: float = 1 / i * 0.5
            if prob > random.uniform(0, 1):
                self.values[index][i] += random.randint(-new_base_range_mutation, new_base_range_mutation)





class IdleGeneticProblem():
        def __init__(self):
            """Constructor"""
                
        def decodifica(self, genotype):
            """Return the phenotype given a genotype"""

        def muta(self, individual: IdleIndividual):
            """Return a new individual from a previous one with
                a posible mutation"""
            individual.mutation();                

        def cruza(self, individual1, individual2):         
            """Return the cross of two individuals"""

        def fitness(self, individual):    
            """Return the fitness of a given individual"""

        def genetic_algorithm():
            """Return best buying sequence"""
        
        def new_generation():
            """Return a new generation"""

def 
