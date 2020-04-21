import random
import math

import pyrosim
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

#local
from robot import ROBOT
from cppn import CPPN

class INDIVIDUAL:
    def __init__(self, id, eval_time=400):
        self.eval_time = eval_time
        self.cppn = CPPN(num_hidden=randint(5,10),
                         scale=8,
                         n_nodes=randint(5,20))
        self.fitness = 0
        self.id = id

    def start_evaluation(self,env,play_blind=True,play_paused=False):
        self.sim = pyrosim.Simulator(play_paused=play_paused,eval_time=self.eval_time, play_blind=play_blind)
        self.robot = ROBOT(self.sim, self.getGenome())
        env.send_to(self.sim)
        self.sim.start()

    def compute_fitness(self):
        self.sim.wait_to_finish()
        y = self.sim.get_sensor_data(sensor_id = self.robot.L4)
        # add instead of set: need to avg all 4 envs
        self.fitness += y[-1] # how close to light source
        del self.sim

    def getGenome(self):
        return self.cppn.generate()

    def mutate(self):
        # totally redo the network every so often
        # if randint(200) == 1:
        #     self.cppn = CPPN(num_hidden=randint(2,10),
        #                      scale=np.random.rand() * 2,
        #                      n_nodes=randint(2,20))
        #     self.cppn.build((1,))

        # always mutate the weights
        self.cppn.mutate_weights()

        # add or remove a layer from fc portion
        # add_remove = randint(10)
        # if add_remove == 1: self.cppn.add_layer_to_fc()
        # elif add_remove == 2: self.cppn.remove_layer_from_fc()
        # self.cppn.build((1,))

    def __str__(self):
        return str(self.id) +": "+ str( np.round(self.fitness, decimals=2) ) # + " mutated " + str(self.geneToMutate)

    def __repr__(self):
        return self.__str__()
