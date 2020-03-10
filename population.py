from individual import INDIVIDUAL
class POPULATION:
    def __init__(self, popSize=5, eval_time=400):
        self.p = {}

        for i in range(popSize):
            self.p[i] = INDIVIDUAL(i,eval_time=eval_time)

    def __str__(self):
        poplist = ["[ "+str(self.p[ind])+" ]" for ind in self.p]
        return ", ".join(poplist)

    def evaluate(self,play_blind=True,play_paused=False):
        for ind in self.p:
            self.p[ind].start_evaluation(play_blind=play_blind,play_paused=play_paused)
        for ind in self.p:
            self.p[ind].compute_fitness()

    def mutate(self):
        for ind in self.p:
            # print("mutating ", ind)
            self.p[ind].mutate()

    def replaceWith(self,other):
        for i in self.p:
            if self.p[i].fitness < other.p[i].fitness:
                self.p[i] = other.p[i]
