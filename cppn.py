import random
import math
import numpy as np
from numpy.random import randint

import tensorflow as tf
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.models import Model,Sequential

def mutate_nested_element(nestedArray):
    try:
        len(nestedArray)
        index = random.randint(0,len(nestedArray)-1)
        nestedArray[index] = mutate_nested_element(nestedArray[index])
        return nestedArray
    except TypeError:
        # stddev = math.fabs(nestedArray)
        # if stddev < 0.05: stddev = 0.05
        stddev = 0.5
        newval = random.gauss(nestedArray, stddev)
        if newval < -2: newval = -2
        if newval > 2: newval = 2
        return newval

class CPPN(Model):
    def __init__(self, xdim=8, ydim=5, cdim=1, num_hidden=3, scale=1, n_nodes=10, seed=None):
        super().__init__()
        self.xdim = xdim
        self.ydim = ydim
        self.n_nodes = n_nodes
        self.num_hidden = num_hidden
        self.cdim = cdim
        self.scale = scale
        self.norm_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=1, seed=seed)
        self.x_input = Dense(self.n_nodes,
                             input_shape=(self.xdim * self.ydim, 1),
                             kernel_initializer=self.norm_init,
                             use_bias=False)
        self.y_input = Dense(self.n_nodes,
                             input_shape=(self.xdim * self.ydim, 1),
                             kernel_initializer=self.norm_init,
                             use_bias=False)

        self.pre_fc = Activation("tanh")

        self.fc_model = Sequential()
        for i in range(self.num_hidden):
            self.add_layer_to_fc(outside=False)

        self.lastdense = Dense(self.cdim,
                               kernel_initializer=self.norm_init,
                               name="lastdense",
                               activation="sigmoid")

    def add_layer_to_fc(self, outside=True):
        # activations = ["tanh", "relu", "sigmoid"]
        activations = ["tanh"]
        if outside: self.num_hidden += 1
        self.fc_model.add(Dense(self.n_nodes,
                                kernel_initializer=self.norm_init,
                                activation=random.choice(activations),
                                name="fc_"+str(len(self.fc_model.layers))))

    def remove_layer_from_fc(self):
        if self.num_hidden > 1:
            self.num_hidden -= 1
            self.fc_model.pop()

    def call(self,inputs=None):
        # x,y,r  (xdim*ydim, 1)
        x, y = self.get_coordinates()
        # each output is (xdim*ydim, layersize)
        Ux = self.x_input(x)
        Uy = self.y_input(y)
        U = Ux + Uy

        # outputs [xdim*ydim, colorchannels]
        result = self.pre_fc(U)
        result = self.fc_model(result)
        result = self.lastdense(result)

        return result #  [xdim*ydim, 3]

    def get_coordinates(self, batch_size = 1):
        '''
        calculates and returns a vector of x and y coordintes, and corresponding radius from the centre of image.
        '''
        n_points = self.xdim * self.ydim
        # creates a list of self.xdim values ranging from -1 to 1, then scales them by scale
        x_range = self.scale*(np.arange(self.xdim)-(self.xdim-1)/2.0)/(self.xdim-1)/0.5
        y_range = self.scale*(np.arange(self.ydim)-(self.ydim-1)/2.0)/(self.ydim-1)/0.5
        x_mat = np.matmul(np.ones((self.ydim, 1)), x_range.reshape((1, self.xdim)))
        y_mat = np.matmul(y_range.reshape((self.ydim, 1)), np.ones((1, self.xdim)))

        x_mat = np.tile(x_mat.flatten(), batch_size).reshape(batch_size, n_points, 1)
        y_mat = np.tile(y_mat.flatten(), batch_size).reshape(batch_size, n_points, 1)

        return x_mat.astype(np.float32), y_mat.astype(np.float32)

    def generate(self):
        return self(None).numpy().reshape(self.ydim, self.xdim, self.cdim).squeeze()

    def mutate_weights(self):
        num_mutations = randint(int(self.count_params() / 50) + 1) + 1
        # num_mutations = 5
        weights = self.get_weights()
        for i in range(num_mutations):
            mutate_nested_element(weights)
        self.set_weights(weights)

    def __deepcopy__(self, memo):
        newmodel = CPPN(self.xdim,
                          self.ydim,
                          self.cdim,
                          num_hidden=self.num_hidden,
                          scale=self.scale,
                          n_nodes=self.n_nodes)
        newmodel.build((1,))
        newmodel.set_weights(self.get_weights())
        return newmodel
