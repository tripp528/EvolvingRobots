import random
import math

import pyrosim
import matplotlib.pyplot as plt

#local
from robot import ROBOT

class INDIVIDUAL:
    def __init__(self, eval_time=100):
        self.eval_time = eval_time
        self.genome = random.random()*2-1 # between [-1,1]
        self.fitness = 0

    def evaluate(self,play_blind=True):
        sim = pyrosim.Simulator(play_paused=False,eval_time=self.eval_time, play_blind=play_blind)
        robot = ROBOT(sim, wt=self.genome)

        sim.start()

        sim.wait_to_finish()

        y = sim.get_sensor_data(sensor_id = robot.P4, svi=1)
        self.fitness = y[-1] #negative because we want into the screen

        # self.plotPosition(sim, robot)

    def mutate(self):
        self.genome = random.gauss(self.genome, math.fabs(self.genome))

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
