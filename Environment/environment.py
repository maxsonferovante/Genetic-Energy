import math
import random

from Individual.individual import Individual
from PopulationComputer.PopulationComputer import mergeSort

class Environment(object):
    def __init__(self,population = None, size =100,maxgenerations = 100,
                 crossover_rate = 0.90, mutation_rate = 0.01 ,optimum = 120):

        self.optimum = optimum
        # Size of the population
        self.size = size
        # Initialize the population
        self.population = population or self.__makePopulation()
        # Start the evaluation of the population
        for individual in self.population:
            individual.evaluate()
        # Crossover rate
        self.crossover_rate = crossover_rate
        # Mutation rate
        self.mutation_rate = mutation_rate
        # Max number of generations
        self.maxGenerations = maxgenerations
        # Initialize the generation
        self.generation = 0
        # Report the algorithm running status
        self.report()
        self.__best = self.population[0]

    # Initialize the population (Generate the individuals)
    def __makePopulation(self):
        return [Individual() for individual in range(self.size)]

    # The step-by-step running algorithm
    def run(self):
        while not self.__goal():
            self.step()

    # The conditions to stop the algorithm.
    def __goal(self):
        return (self.generation > self.maxGenerations) or (self.__best.getScore() == self.optimum)
        # The step done by the genetic algorithm


    def step(self):
        # Sort the individuals of the population based on their score
        self.population = mergeSort(self.population)

        if self.__best == None:
            self.__best = self.population[0]

        # Make the crossover
        self.__crossover()
        # Increments the generation
        self.generation += 1
        # Report the current status
        self.report()

    # Selection method of the individuals for crossover
    def __select(self):
        return self.__tournament()

    # sample selection method
    def __tournament(self):
        competitors = []
        total_score = sum([math.ceil(self.population[i].getScore()) for i in range(self.size)])
        for index in range(self.size):
            temp = [index] * int((math.ceil(self.population[index].getScore() / total_score) * 100))
            competitors.extend(temp)
        return self.population[random.choice(competitors)]
        # Crossover proccess

    def __crossover(self):
        # Elistism proccess (best individual is copied to the next generation)
        next_population = [self.__best.copy()]
        while len(next_population) < self.size:
            mate1 = self.__select()
            if random.random() < self.crossover_rate:
                mate2 = self.__select()
                offspring = mate1.crossover(mate2)
            else:
                # make a copy of individual
                offspring = [mate1.copy()]
            for individual in offspring:
                self.__mutate(individual)
                individual.evaluate()
                next_population.append(individual)
        self.population = next_population[:self.size]

    # Mutation method.
    # @param individual: Individual to be mutated.
    def _mutate(self, individual):
        for i in range(32,len(individual.length),64):
            if random.random() < self.mutation_rate:
                individual.mutate()

    # Shows the results report
    def report(self):
        print("generation: ", self.generation)
