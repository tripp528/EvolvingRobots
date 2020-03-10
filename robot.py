import pyrosim
import matplotlib.pyplot as plt
import constants as c

class ROBOT:
    def __init__(self, sim, wts):

        self.send_objects(sim)
        # self.send_joints(sim)
        # self.send_sensors(sim)
        # self.send_neurons(sim)
        # self.send_synapses(sim,wts)

    def send_objects(self,sim):
        O0 = sim.send_box(x=0, y=0, z=c.L + c.R, length=c.L, width=c.L, height=2*c.R, r=0.5, g=0.5, b=0.5)
        O1 = sim.send_cylinder(x=0,y=c.L,z=c.L + c.R, length=c.L,radius=c.R, r=1, g=0, b=0, r1=0,r2=1, r3=0)
        O2 = sim.send_cylinder(x=c.L,y=0,z=c.L + c.R, length=c.L,radius=c.R, r=0, g=1, b=0, r1=1,r2=0, r3=0)
        O3 = sim.send_cylinder(x=0,y=-c.L,z=c.L + c.R, length=c.L,radius=c.R, r=0, g=0, b=1, r1=0,r2=1, r3=0)
        O4 = sim.send_cylinder(x=-c.L,y=0,z=c.L + c.R, length=c.L,radius=c.R, r=1, g=0, b=1, r1=1,r2=0, r3=0)

        O5 = sim.send_cylinder(x=0,y=c.L*3/2,z=c.L/2 + c.R, length=c.L,radius=c.R, r=1, g=0, b=0, r1=0,r2=0, r3=1)
        O6 = sim.send_cylinder(x=c.L*3/2,y=0,z=c.L/2 + c.R, length=c.L,radius=c.R, r=0, g=1, b=0, r1=0,r2=0, r3=1)
        O7 = sim.send_cylinder(x=0,y=-c.L*3/2,z=c.L/2 + c.R, length=c.L,radius=c.R, r=0, g=0, b=1, r1=0,r2=0, r3=1)
        O8 = sim.send_cylinder(x=-c.L*3/2,y=0,z=c.L/2 + c.R, length=c.L,radius=c.R, r=1, g=0, b=1, r1=0,r2=0, r3=1)


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
