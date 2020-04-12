import random
import math

import pyrosim
import matplotlib.pyplot as plt
import numpy as np

#local
from robot import ROBOT
from cppn import CPPN

class INDIVIDUAL:
    def __init__(self, id, eval_time=400):
        self.eval_time = eval_time

        # self.genome = np.random.rand(5,8) * 2 - 1
        xdim,ydim,cdim = (5,8,1)
        cppn = CPPN(xdim,ydim,cdim,num_hidden=0,scale=10, n_nodes=1)
        self.genome = cppn(None).numpy().reshape(xdim,ydim,cdim).squeeze()
        print(self.genome)

        self.fitness = 0
        self.id = id
        self.geneToMutate = -1 # not a real gene, placeholder

    def start_evaluation(self,env,play_blind=True,play_paused=False):
        self.sim = pyrosim.Simulator(play_paused=play_paused,eval_time=self.eval_time, play_blind=play_blind)
        self.robot = ROBOT(self.sim, self.genome)
        env.send_to(self.sim)
        self.sim.start()

    def compute_fitness(self):
        self.sim.wait_to_finish()
        y = self.sim.get_sensor_data(sensor_id = self.robot.L4)
        # add instead of set: need to avg all 4 envs
        self.fitness += y[-1] # how close to light source
        del self.sim

    def mutate(self):
        self.geneToMutate = random.randint(0,4), random.randint(0,7)
        newval = random.gauss(self.genome[self.geneToMutate], math.fabs(self.genome[self.geneToMutate]))

        # make sure between -1 and 1
        if newval < -1:
            new = -1
        if newval > 1:
            newval = 1

        self.genome[self.geneToMutate] = newval

    def __str__(self):
        return str(self.id) +": "+ str(self.fitness) # + " mutated " + str(self.geneToMutate)

    def __repr__(self):
        return self.__str__()
