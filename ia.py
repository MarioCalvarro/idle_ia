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

class IdleGeneticProblem(object):
        def __init__(self):
            """Constructor"""
                
        def decodifica(self, genotype):
            """Return the phenotype given a genotype"""

        def muta(self, individual, prob):
            """Return a new individual from a previous one with 
                a posible mutation"""   

        def cruza(self, individual1, individual2):         
            """Return the cross of two individuals"""

        def fitness(self, individual):    
            """Return the fitness of a given individual"""

        def genetic_algorithm():
            """Return best buying sequence"""
        
        def new_generation():
            """Return a new generation"""

def 
