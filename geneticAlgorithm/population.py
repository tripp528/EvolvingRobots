import copy
import random

from individual import INDIVIDUAL

class POPULATION:
    def __init__(self, popSize=5, eval_time=400, parents=None):
        self.p = {}
        self.popSize = popSize
        self.eval_time = eval_time

        if parents:
            self.popSize = parents.popSize
            self.eval_time = parents.eval_time

    def initialize(self):
        for i in range(self.popSize):
            self.p[i] = INDIVIDUAL(i,eval_time=self.eval_time)

    def __str__(self):
        poplist = ["[ "+str(self.p[ind])+" ]" for ind in self.p]
        return ", ".join(poplist)

    def evaluate(self,play_blind=True,play_paused=False):
        for ind in self.p:
            self.p[ind].start_evaluation(play_blind=play_blind,play_paused=play_paused)
        for ind in self.p:
            self.p[ind].compute_fitness()

    def playbest(self):
        maxFit = 0
        maxInd = -1
        for ind in self.p:
            if self.p[ind].fitness > maxFit:
                maxInd = ind
        self.p[maxInd].start_evaluation(play_blind=False,play_paused=True)
        self.p[maxInd].compute_fitness()

    def mutate(self):
        for ind in self.p:
            # print("mutating ", ind)
            self.p[ind].mutate()

    def replaceWith(self,other):
        """ For hillclimber """
        for i in self.p:
            if self.p[i].fitness < other.p[i].fitness:
                self.p[i] = other.p[i]

    def copyBestFrom(self,other):
        """ helper for genetic alg
            makes a copy of best parent and puts it  in the first spot of
            the children population.

            known as ‘elitism’: do not lose the most fit individual so far
        """
        highestFitness = 0
        highestFitnessIndex = -1
        for i in other.p:
            if highestFitness < other.p[i].fitness:
                highestFitness = other.p[i].fitness
                highestFitnessIndex = i

        copyOfBest = copy.deepcopy(other.p[highestFitnessIndex])
        self.p[0] = copyOfBest

    def tournamentSelect(self,other): # self not used
        """ helper for genetic alg
        """
        p1 = random.randint(0, other.popSize - 1) # 0 <= N <= popSize-1
        p2 = random.randint(0, other.popSize - 1)
        while p2 == p1:
            p2 = random.randint(0, other.popSize - 1)

        if other.p[p1].fitness > other.p[p2].fitness:
            return other.p[p1]

        return other.p[p2]

    def collectChildrenFrom(self,other):
        """ helper for genetic alg
        """
        for i in range(1, self.popSize):  # first slot has already been filled
            # self.p[i] = copy.deepcopy(other.p[i])
            winner = copy.deepcopy(self.tournamentSelect(other))
            winner.mutate()
            self.p[i] = winner

    def fillFrom(self, other):
        """ For genetic alg """
        self.copyBestFrom(other)
        self.collectChildrenFrom(other)
