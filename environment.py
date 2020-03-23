import constants

class ENVIRONMENT:

    def __init__(self,id, eval_time=400):
        self.id = id
        self.eval_time = eval_time
        self.l = constants.L
        self.w = constants.L
        self.h = constants.L
        # initialize position to 0,0,0
        self.x = 0
        self.y = 0
        self.z = 0
        if id == 0: #front
            self.y = 30 * constants.L # pos y is "front"
        if id == 1: #right
            self.x = 30 * constants.L
        if id == 2: #back
            self.y = -30 * constants.L
        if id == 3: #left 
            self.x = -30 * constants.L


    def send_to(self,sim):
        lightsource = sim.send_box(x=self.x, y=self.y, z=self.z, length=self.l, width=self.w, height=self.h)#, r=0.5, g=0.5, b=0.5
        sim.send_light_source( body_id = lightsource )
