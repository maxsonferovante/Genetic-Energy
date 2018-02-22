import random
import numpy as np


MAXIMIZE,MINIMIZE = (0,1)
STR_DELIMITER = ''

class Individual(object):
    def __init__(self,chromosome=''):
        self.__score = 0.0 ## Consumo Medio Mensal (kWh)
        self.__chromosome = chromosome or self.__makeChromosome()

        self.length = len(self.__chromosome)

    def getLength(self):
        return len(self.__chromosome)

    def getScore(self):
        return  self.__score

    def getChromosome(self):
        return self.__chromosome

    def setScore(self,score):
        if score > 0:
            self.__score = score
        else:
            raise "Not acceptable negative score"

    def setChromosome(self,chromosome):
        if chromosome:
            self.__chromosome = chromosome
        else:
            raise "Empty Chromosome Not Acceptable"

    chromosome = property(fget=getChromosome, fset=setChromosome)

    def __makeChromosome(self):
        bin32 = lambda x: ''.join(reversed([str((x >> i) & 1) for i in range(32)]))
        base_watts = np.loadtxt("Individual/base/watts.txt")
        choromosome_synthetized = ''
        for watts in base_watts:
            choromosome_synthetized +=   bin32(int(watts)) + bin32(random.randint(1,2678400))
        return choromosome_synthetized

    def evaluate(self):
        consumption = []
        for i in range(32,len(self.__chromosome),64):
            watt = int(self.__chromosome[i-32:(i-32)+32],2)/1000.0
            time_hour = int(self.__chromosome[i:i + 32],2)/3600.0
            consumption.append((watt*time_hour))
        self.__score = sum(consumption)/len(consumption)

    def crossover(self,mate):
        return self.__twopoint(mate)

    def mutate(self,gene):
        self.__pick(gene)

    def __twopoint(self,other):

        cut_one = self.__pickPivots()
        cut_two = self.__pickPivots()

        while cut_one > cut_two:
            cut_two = self.__pickPivots()

        def mate(c1,c2):
            child = c1.__class__(
                c1.__chromosome [:cut_one]+c2.__chromosome [cut_one:cut_two] + c1.chromosome[cut_two:]
            )
            return  child

        return mate(self, other), mate(other, self)


    def __pick(self,point):
        cut = self.__pickPivots()
        self.__chromosome = self.__chromosome[:cut] + str(int(not int( self.__chromosome[cut]))) + self.__chromosome[cut+1:]

    def __pickPivots(self):
        return  random.choice(
            [i for i in range(32,len(self.__chromosome),64)]
        )


    # Returns string representation of itself
    def __repr__(self):
        return "score %s kW" % self.__score

    # The comparison method with other individual
    # @param other: The other individual that will be compared.
    
    def __eq__(self, other):
        return (self.getScore() == other.getScore())

    def __ne__(self, other):
        return (self.getScore() != other.getScore())

    def __lt__(self, other):
        return (self.getScore() < other.getScore())

    def __le__(self, other):
        return (self.getScore() <= other.getScore())

    def __gt__(self, other):
        return (self.getScore() > other.getScore())

    def __ge__(self, other):
        return (self.getScore() >= other.getScore())
    
    # Creates a replicate of itself.
    def copy(self):
        clone = Individual(self.chromosome)
        clone.evaluate()
        return clone


