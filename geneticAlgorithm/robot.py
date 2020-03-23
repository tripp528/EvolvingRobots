import pyrosim
import matplotlib.pyplot as plt
import constants as c

class ROBOT:
    def __init__(self, sim, wts):

        self.send_objects(sim)
        self.send_joints(sim)
        self.send_sensors(sim)
        self.send_neurons(sim)
        self.send_synapses(sim,wts)

        del self.O
        del self.J
        del self.S
        del self.sensorNeurons
        del self.motorNeurons


    def send_objects(self,sim):
        self.O = {}
        self.O[0] = sim.send_box(x=0, y=0, z=c.L + c.R, length=c.L, width=c.L, height=2*c.R, r=0.5, g=0.5, b=0.5)

        self.O[1] = sim.send_cylinder(x=0,y=c.L,z=c.L + c.R, length=c.L,radius=c.R, r=1, g=0, b=0, r1=0,r2=1, r3=0)
        self.O[2] = sim.send_cylinder(x=c.L,y=0,z=c.L + c.R, length=c.L,radius=c.R, r=0, g=1, b=0, r1=1,r2=0, r3=0)
        self.O[3] = sim.send_cylinder(x=0,y=-c.L,z=c.L + c.R, length=c.L,radius=c.R, r=0, g=0, b=1, r1=0,r2=1, r3=0)
        self.O[4] = sim.send_cylinder(x=-c.L,y=0,z=c.L + c.R, length=c.L,radius=c.R, r=1, g=0, b=1, r1=1,r2=0, r3=0)

        self.O[5] = sim.send_cylinder(x=0,y=c.L*3/2,z=c.L/2 + c.R, length=c.L,radius=c.R, r=1, g=0, b=0, r1=0,r2=0, r3=1)
        self.O[6] = sim.send_cylinder(x=c.L*3/2,y=0,z=c.L/2 + c.R, length=c.L,radius=c.R, r=0, g=1, b=0, r1=0,r2=0, r3=1)
        self.O[7] = sim.send_cylinder(x=0,y=-c.L*3/2,z=c.L/2 + c.R, length=c.L,radius=c.R, r=0, g=0, b=1, r1=0,r2=0, r3=1)
        self.O[8] = sim.send_cylinder(x=-c.L*3/2,y=0,z=c.L/2 + c.R, length=c.L,radius=c.R, r=1, g=0, b=1, r1=0,r2=0, r3=1)


    def send_joints(self,sim):
        self.J = {}

        self.J[0] = sim.send_hinge_joint( x=0,y=c.L/2,z=c.L + c.R,
                                        n1=1,n2=0,n3=0,
                                        first_body_id =  self.O[0],
                                        second_body_id = self.O[1],
                                        lo=-3.14159/2,hi=3.14159/2)
        self.J[1] = sim.send_hinge_joint( x=0,y=3*c.L/2,z=c.L + c.R,
                                        n1=1,n2=0,n3=0,
                                        first_body_id =  self.O[1],
                                        second_body_id = self.O[5],
                                        lo=-3.14159/2,hi=3.14159/2)

        self.J[2] = sim.send_hinge_joint( x=c.L/2,y=0,z=c.L + c.R,
                                        n1=0,n2=1,n3=0,
                                        first_body_id =  self.O[0],
                                        second_body_id = self.O[2],
                                        lo=-3.14159/2,hi=3.14159/2)
        self.J[3] = sim.send_hinge_joint( x=3*c.L/2,y=0,z=c.L + c.R,
                                        n1=0,n2=1,n3=0,
                                        first_body_id =  self.O[2],
                                        second_body_id = self.O[6],
                                        lo=-3.14159/2,hi=3.14159/2)

        self.J[4] = sim.send_hinge_joint( x=0,y=-c.L/2,z=c.L + c.R,
                                        n1=1,n2=0,n3=0,
                                        first_body_id =  self.O[0],
                                        second_body_id = self.O[3],
                                        lo=-3.14159/2,hi=3.14159/2)
        self.J[5] = sim.send_hinge_joint( x=0,y=-3*c.L/2,z=c.L + c.R,
                                        n1=1,n2=0,n3=0,
                                        first_body_id =  self.O[3],
                                        second_body_id = self.O[7],
                                        lo=-3.14159/2,hi=3.14159/2)

        self.J[6] = sim.send_hinge_joint( x=-c.L/2,y=0,z=c.L + c.R,
                                        n1=0,n2=1,n3=0,
                                        first_body_id =  self.O[0],
                                        second_body_id = self.O[4],
                                        lo=-3.14159/2,hi=3.14159/2)
        self.J[7] = sim.send_hinge_joint( x=-3*c.L/2,y=0,z=c.L + c.R,
                                        n1=0,n2=1,n3=0,
                                        first_body_id =  self.O[4],
                                        second_body_id = self.O[8],
                                        lo=-3.14159/2,hi=3.14159/2)

    def send_sensors(self,sim):
        #sensors
        self.S = {}
        self.S[0] = sim.send_touch_sensor(body_id = self.O[5])
        self.S[1] = sim.send_touch_sensor(body_id = self.O[6])
        self.S[2] = sim.send_touch_sensor(body_id = self.O[7])
        self.S[3] = sim.send_touch_sensor(body_id = self.O[8])

        self.P4 = sim.send_position_sensor(body_id = self.O[0])

    def send_neurons(self,sim):
        # sensor neurons
        self.sensorNeurons = {}
        for s in self.S:
            self.sensorNeurons[s] = sim.send_sensor_neuron(sensor_id = self.S[s])

        # motor neurons
        self.motorNeurons = {}
        for j in self.J:
            self.motorNeurons[j] = sim.send_motor_neuron(   joint_id = self.J[j],
                                                            tau = 0.3)

    def send_synapses(self,sim,wts):
        import random
        # synapses
        for s in self.sensorNeurons:
            for m in self.motorNeurons:
                sim.send_synapse(   source_neuron_id = self.sensorNeurons[s],
                                    target_neuron_id = self.motorNeurons[m],
                                    weight = wts[s,m])
