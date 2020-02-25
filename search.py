import random

import pyrosim
import matplotlib.pyplot as plt
from robot import ROBOT


for i in range(0,10):
    sim = pyrosim.Simulator(play_paused=False,eval_time=75)

    random_weight = random.random()*2-1 # between [-1,1]
    robot = ROBOT(sim, wt=random_weight)

    sim.start()

    sim.wait_to_finish()

# sensorData = sim.get_sensor_data(sensor_id = MN2)
# f = plt.figure()
# panel = f.add_subplot(111)
# plt.plot(sensorData)
# plt.show()
