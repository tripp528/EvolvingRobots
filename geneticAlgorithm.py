import random
import copy
import logging
logging.basicConfig(level=logging.INFO)
import pickle
import pyrosim
import matplotlib.pyplot as plt
import numpy as np
from robot import ROBOT
from individual import INDIVIDUAL
from population import POPULATION
import constants
from environments import ENVIRONMENTS

# create environment with "light source"
envs = ENVIRONMENTS(numEnvs=constants.numEnvs, eval_time=constants.eval_time)

# create initial population
parents = POPULATION(envs,popSize=constants.popSize, eval_time=constants.eval_time)
parents.initialize()
parents.evaluate(play_blind=False,play_paused=False)
print(0,parents)

# evolve:
# for g in range(constants.numGen):
#     children = POPULATION(parents=parents)
#     children.fillFrom(parents)
#     children.evaluate(play_blind=True,play_paused=False)
#     parents.replaceWith(children)
#     print(g+1,parents)
# parents.playbest()
