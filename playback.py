import logging
import pickle

from individual import INDIVIDUAL
logging.basicConfig(level=logging.INFO)

best = pickle.load(open('saved_robots/robot.p','rb'))
logging.info('\t[fitness: %.2f' % best.fitness + ']'+
             '\t[genome: ' + str(best.genome) + ']')

best.evaluate(play_blind=False)
