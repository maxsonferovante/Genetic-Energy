import random
import numpy as np


MAXIMIZE,MINIMIZE = (0,1)
STR_DELIMITER = ''

class Individual(object):
    def __init__(self,chromosome=''):
        self.__score = 0.0 ## Consumo Médio Mensal (kWh)
        self.__chromosome = chromosome or self.__makeChromosome()

        self.length = len(self.__chromosome)

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
        base_watts = np.loadtxt("C:\\Users\\Maxson Ferovante\\PycharmProjects\\Genetic-Energy\\base\\watts")
        choromosome_synthetized = ''
        for watts in base_watts:
            choromosome_synthetized +=   bin32(int(watts)) + bin32(random.randint(0,2678400))
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
        cut= self.__pickPivots()
        def mate(p0,p1):
            chromosome = p0._chromosome[:]
            chromosome[cut:cut+32] = p1._chromosome[cut:cut+32]
            child = p0.__class__(chromosome)
            child.repair(p0,p1)
            return child
        return mate(self,other),mate(other,self)

    def __pick(self):
        cut = self.__pickPivots()
        point = random.choice(
            [i for i in range(cut,cut+32)]
        )
        self.__chromosome[point] = str(int (not self.__chromosome[point]))

    def __pickPivots(self):
        cuts = [i for i in range(32,len(self.__chromosome),64)]
        return  random.choice(cuts)

    def repair(self,p0,p1):
        pass

    # Returns string representation of itself
    def __repr__(self):
        return "score %s kW" % self.__score

    # The comparison method with other individual
    # @param other: The other individual that will be compared.
    def __cmp__(self, other):
        if (self.getScore() <other.getScore()):
            return 1
        elif (self.getScore()> other.getScore()):
            return  0
        else:
            return -1
    # Creates a replicate of itself.
    def copy(self):
        clone = self.__class__(self.chromosome[:])
        clone.score = self.getScore()
        return clone