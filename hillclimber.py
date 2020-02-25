import random
import copy
import logging
logging.basicConfig(level=logging.INFO)

import pickle
import pyrosim
import matplotlib.pyplot as plt

#local
from robot import ROBOT
from individual import INDIVIDUAL

initBlind = True
newBlind = True
endBlind = False

parent = INDIVIDUAL(eval_time=1000)
parent.evaluate(play_blind=initBlind)

# loop through and evolve using gaussian dist.
for i in range(0,1000):
    child = copy.deepcopy(parent)
    child.mutate()
    child.evaluate()
    logging.info('[g: %d' % i + ']' +
                 '\t[p: %.2f' % parent.fitness + ']'+
                 '\t[c: %.2f' % child.fitness + ']' +
                 '\t[pw: %.2f' % parent.genome + ']')

    if (child.fitness > parent.fitness):
        parent = child
        # play the new one when it is changed out
        parent.evaluate(play_blind=newBlind)
        pickle.dump(parent,open('saved_robots/robot'+str(i)+'.p','wb'))

# show the final robot
parent.evaluate(play_blind=endBlind)
