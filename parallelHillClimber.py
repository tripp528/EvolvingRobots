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

hide_initial = True
hide_new_replacements = True
hide_final = True
save_checkpoints = True

parent = INDIVIDUAL(eval_time=1000)
parent.evaluate(play_blind=hide_initial)

# loop through and evolve using gaussian dist.
for i in range(0,200):
    child = copy.deepcopy(parent)
    child.mutate()
    child.evaluate()
    logging.info('[g: %d' % i + ']' +
                 '\t[p: %.2f' % parent.fitness + ']'+
                 '\t[c: %.2f' % child.fitness + ']' +
                 '\t[pw: ' + str(parent.genome) + ']')

    if (child.fitness > parent.fitness):
        parent = child
        # play the new one when it is changed out
        parent.evaluate(play_blind=hide_new_replacements)
        # if save_checkpoints:
        pickle.dump(parent,open('saved_robots/robot.p','wb'))

# show the final robot
parent.evaluate(play_blind=hide_final)
