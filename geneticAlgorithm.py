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

parents = POPULATION(popSize=5, eval_time=500)
parents.initialize()
parents.evaluate(play_blind=True,play_paused=False)

print(parents)

#
for g in range(1):
    children = POPULATION(parents=parents)
    print(children)
#     children = copy.deepcopy(parents)
#     children.mutate()
#     children.evaluate(play_blind=True,play_paused=False)
#     parents.replaceWith(children)
#     print(g,parents)
#
# parents.playbest()
