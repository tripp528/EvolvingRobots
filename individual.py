import random
import math

import pyrosim
import matplotlib.pyplot as plt
import numpy as np

#local
from robot import ROBOT

class INDIVIDUAL:
    def __init__(self, id, eval_time=400):
        self.eval_time = eval_time
        # self.genome = random.random()*2-1 # between [-1,1]
        self.genome = np.random.random(4) * 2 - 1
        self.fitness = 0
        self.id = id
        self.geneToMutate = -1 # not a real gene, placeholder

    def start_evaluation(self,play_blind=True,play_paused=False):
        self.sim = pyrosim.Simulator(play_paused=play_paused,eval_time=self.eval_time, play_blind=play_blind)
        self.robot = ROBOT(self.sim, self.genome)

        self.sim.start()

    def compute_fitness(self):
        self.sim.wait_to_finish()

        y = self.sim.get_sensor_data(sensor_id = self.robot.P4, svi=1)
        self.fitness = y[-1] #negative because we want into the screen

        del self.sim

    def mutate(self):
        self.geneToMutate = random.randint(0,3)
        self.genome[self.geneToMutate] = random.gauss(self.genome[self.geneToMutate], math.fabs(self.genome[self.geneToMutate]))

    def __str__(self):
        return str(self.id) +": "+ str(self.fitness) # + " mutated " + str(self.geneToMutate)

    def __repr__(self):
        return self.__str__()

    def plotPosition(self, sim, robot):
        # get robot position at end
        x = sim.get_sensor_data(sensor_id = robot.P4, svi=0)
        y = sim.get_sensor_data(sensor_id = robot.P4, svi=1)
        z = sim.get_sensor_data(sensor_id = robot.P4, svi=2)

        f = plt.figure()
        ax = f.add_subplot(221)
        ax.plot(x)
        ax.set_title("X Position")

        ax = f.add_subplot(222)
        ax.plot(y)
        ax.set_title("Y Position")

        ax = f.add_subplot(223)
        ax.plot(z)
        ax.set_title("Z Position")

        plt.tight_layout()
        plt.show()
