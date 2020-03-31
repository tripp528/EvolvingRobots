import random
import copy
import logging
logging.basicConfig(level=logging.INFO)

import pickle
import pyrosim
import matplotlib.pyplot as plt
import numpy as np

#local
from robot import ROBOT
from individual import INDIVIDUAL
from population import POPULATION

hide_initial = True
hide_new_replacements = True
hide_final = True
save_checkpoints = True

parents = POPULATION(popSize=10, eval_time=500)
parents.initialize()
parents.evaluate(play_blind=True,play_paused=False)

print(0,parents)

#
for g in range(200):
    children = POPULATION(parents=parents)
    children.fillFrom(parents)
    children.evaluate(play_blind=True,play_paused=False)


#     children = copy.deepcopy(parents)
#     children.mutate()
#     children.evaluate(play_blind=True,play_paused=False)
    parents.replaceWith(children)
    print(g+1,parents)
#
parents.playbest()