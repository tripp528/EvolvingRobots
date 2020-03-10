import pyrosim
import matplotlib.pyplot as plt

class ROBOT:
    def __init__(self, sim, wts):

        self.send_objects(sim)
        # self.send_joints(sim)
        # self.send_sensors(sim)
        # self.send_neurons(sim)
        # self.send_synapses(sim,wts)

    def send_objects(self,sim):
        self.whiteObject = sim.send_cylinder(x=0,y=0,z=0.6,length=1.0, radius=0.1)
        self.redObject = sim.send_cylinder(x=0,y=0.5,z=1.1, r=1,g=0,b=0, r1=0,r2=1, r3=0)

    def send_joints(self,sim):
        self.joint = sim.send_hinge_joint(x=0,y=0,z=1.1, n1=1,n2=0,n3=0,
                                    first_body_id =  self.redObject,
                                    second_body_id = self.whiteObject,
                                    lo=-3.14159/2,hi=3.14159/2)

    def send_sensors(self,sim):
        #sensors
        self.T0 = sim.send_touch_sensor(body_id = self.whiteObject)
        self.T1 = sim.send_touch_sensor(body_id = self.redObject)
        self.P2 = sim.send_proprioceptive_sensor(joint_id = self.joint)
        self.R3 = sim.send_ray_sensor(body_id = self.redObject,x=0,y=1.1,z=1.1,r1=0,r2=1, r3=0)
        self.P4 = sim.send_position_sensor(body_id = self.redObject)

    def send_neurons(self,sim):
        # sensor neurons
        self.sensorNeurons = {}
        self.sensorNeurons[0] = sim.send_sensor_neuron(sensor_id = self.T0) # white object
        self.sensorNeurons[1] = sim.send_sensor_neuron(sensor_id = self.T1) # red object
        self.sensorNeurons[2] = sim.send_sensor_neuron(sensor_id = self.P2) # joint sensor
        self.sensorNeurons[3] = sim.send_sensor_neuron(sensor_id = self.R3) # ray sensor

        # motor neurons
        self.motorNeurons = {}
        self.motorNeurons[0] = sim.send_motor_neuron(joint_id = self.joint)

    def send_synapses(self,sim,wts):
        # synapses
        for s in self.sensorNeurons:
            for m in self.motorNeurons:
                sim.send_synapse(source_neuron_id = self.sensorNeurons[s], target_neuron_id = self.motorNeurons[m], weight = wts[s])
