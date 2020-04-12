import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.models import Model,Sequential

class CPPN(Model):
    def __init__(self, xdim=500, ydim=500, cdim=3, z_dim=32, n_nodes=32, num_hidden=3, scale=8):
        super().__init__()
        self.xdim = xdim
        self.ydim = ydim
        self.z_dim = z_dim
        self.n_nodes = n_nodes
        self.num_hidden = num_hidden
        self.cdim = cdim
        self.scale = scale
        norm_init = tf.keras.initializers.RandomNormal(mean=0.0, stddev=1, seed=4)
        # norm_init = tf.keras.initializers.Ones()

        # input  ( xdim*ydim, z_dim )
        # output ( xdim*ydim, layer_size )
        self.z_input = Dense(self.n_nodes, input_shape=(self.xdim * self.ydim, self.z_dim))

        # input  ( xdim*ydim, 1 )
        # output ( xdim*ydim, layer_size )
        self.x_input = Dense(self.n_nodes,
                             input_shape=(self.xdim * self.ydim, 1),
                             kernel_initializer=norm_init,
                             use_bias=False)
        self.y_input = Dense(self.n_nodes,
                             input_shape=(self.xdim * self.ydim, 1),
                             kernel_initializer=norm_init,
                             use_bias=False)
        self.r_input = Dense(self.n_nodes,
                             input_shape=(self.xdim * self.ydim, 1),
                             kernel_initializer=norm_init,
                             use_bias=False)

        # input  ( xdim*ydim, layer_size )
        # output ( xdim*ydim, color_channels )
        self.fc_model = Sequential()
        for i in range(self.num_hidden):
            self.fc_model.add(Activation("tanh"))
            self.fc_model.add(Dense(self.n_nodes,
                                    kernel_initializer=norm_init))
        self.fc_model.add(Dense(self.cdim, kernel_initializer=norm_init))
        self.fc_model.add(Activation("sigmoid"))

    def call(self,inputs=None):
        # (1, z_dim)
        z = np.random.uniform(-1.0, 1.0, size=(1, self.z_dim))
        # (xdim*ydim, zdim)
        z_scaled = np.matmul(np.ones((self.xdim*self.ydim, 1)), z).astype(np.float32)
        # (xdim*ydim, layersize)
        Uz = self.z_input(z_scaled)

        # x,y,r  (xdim*ydim, 1)
        x, y, r = self.get_coordinates()
        # each output is (xdim*ydim, layersize)
        Ux = self.x_input(x)
        Uy = self.y_input(y)
        Ur = self.r_input(r)

        # still (xdim*ydim, layersize)
        U = Ux + Uy + Ur

        # outputs [xdim*ydim, colorchannels]
        result = self.fc_model(U)

        return result #  [xdim*ydim, 3]

    def get_coordinates(self, batch_size = 1):
        '''
        calculates and returns a vector of x and y coordintes, and corresponding radius from the centre of image.
        '''
        n_points = self.xdim * self.ydim
        # creates a list of self.xdim values ranging from -1 to 1, then scales them by scale
        x_range = self.scale*(np.arange(self.xdim)-(self.xdim-1)/2.0)/(self.xdim-1)/0.5
        y_range = self.scale*(np.arange(self.ydim)-(self.ydim-1)/2.0)/(self.ydim-1)/0.5
#         x_range = np.arange(self.xdim) / (self.xdim-1)
#         y_range = np.arange(self.ydim) / (self.ydim-1)
        x_mat = np.matmul(np.ones((self.ydim, 1)), x_range.reshape((1, self.xdim)))
        y_mat = np.matmul(y_range.reshape((self.ydim, 1)), np.ones((1, self.xdim)))
        r_mat = np.sqrt(x_mat*x_mat + y_mat*y_mat)
        x_mat = np.tile(x_mat.flatten(), batch_size).reshape(batch_size, n_points, 1)
        y_mat = np.tile(y_mat.flatten(), batch_size).reshape(batch_size, n_points, 1)
        r_mat = np.tile(r_mat.flatten(), batch_size).reshape(batch_size, n_points, 1)
        return x_mat.astype(np.float32), y_mat.astype(np.float32), r_mat.astype(np.float32)
