import random

import pyrosim
import matplotlib.pyplot as plt

#local
from robot import ROBOT
from individual import INDIVIDUAL


for i in range(0,10):
    individual = INDIVIDUAL()
    individual.evaluate()
    print(individual.fitness)


    # robot.plotPosition()
