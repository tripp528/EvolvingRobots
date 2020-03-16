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
        for i in self.p:
            if self.p[i].fitness < other.p[i].fitness:
                self.p[i] = other.p[i]
