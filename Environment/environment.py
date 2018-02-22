import math
import random

import time

from Individual.individual import Individual
from PopulationComputer import PopulationComputer

class Environment(object):
    def __init__(self,population = None, size =500,maxgenerations = 100,
                 crossover_rate = 0.87, mutation_rate = 0.01 ,optimum = 120):

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

        self.best = random.choice(self.population)
        # Report the algorithm running statu
        self.report()

    # Initialize the population (Generate the individuals)
    def __makePopulation(self):
        return [Individual() for individual in range(self.size)]

    # The step-by-step running algorithm
    def run(self):
        while not self.__goal():
            self.step()

    # The conditions to stop the algorithm.
    def __goal(self):
        return (self.generation >= self.maxGenerations)
        # The step done by the genetic algorithm


    def step(self):
        # Sort the individuals of the population based on their score


        self.population = PopulationComputer.heapSort(self.population)


        if self.best >self.population[0]:
            self.best = self.population[0]

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
        total_score = sum([self.population[i].getScore() for i in range(self.size)])
        for index in range(self.size):
            ## {key:value} = { index: Aptidão do cromossomo como uma portcetagem da apitidão total}
            percentual = {"index": index, "score":(math.ceil(self.population[index].getScore() * 100.0) / total_score)}
            competitors.append(percentual)

        competitors_sorted = sorted(competitors, key=lambda k: k["score"])
        competitors_sorted.reverse()

        individual_sorted = None
        while individual_sorted is None:
            index = 0
            number_sorted = random.randrange(100)

            russian_roulette = [
                {
                    "interval": (0,( 100 - competitors_sorted[0]["score"]) - competitors_sorted[0]["score"]),
                    "element": competitors_sorted[0]["index"]
                }
            ]
            while russian_roulette.__len__() < competitors_sorted.__len__():
                if self.__russian_roulette(russian_roulette, number_sorted, index):
                    individual_sorted = self.population[russian_roulette[index]["element"]]
                    break
                else:
                    index = index + 1
                    russian_roulette.append(
                        {
                            "interval": (russian_roulette[-1]["interval"][1],
                                         (100 - competitors_sorted[index]["score"]) - competitors_sorted[index]["score"] + russian_roulette[-1]["interval"][1]),
                            "element": competitors_sorted[index]["index"]
                        }
                    )

            del russian_roulette

        return  individual_sorted

    def __russian_roulette(self, russian_roulette,number_sorted, index):
        if number_sorted > russian_roulette[index]["interval"][0] and number_sorted <= russian_roulette[index]["interval"][1]:
            return True
        return False

    def __crossover(self):
        # Elistism proccess (best individual is copied to the next generation)
        next_population = [self.best.copy()]

        while len(next_population) < self.size:

            mate1 = self.__select()
            random.seed(time.clock())
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
    def __mutate(self, individual):
        random.seed(time.clock())
        if random.random() < self.mutation_rate:
            index_gene = random.randrange(self.population[0].getLength())
            individual.mutate(index_gene)

    # Shows the results report
    def report(self):
        total_score = sum([self.population[i].getScore() for i in range(self.size)])

        print("\ngeneration: ", self.generation)
        print("Score total: ", total_score, " , Score media:", math.trunc(total_score / self.size))
        print("best", self.best)


