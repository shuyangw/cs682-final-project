import tensorflow as tf
import numpy as np

class DDQNCNN(object):
    def __init__(self, state_size, action_size, lr, name="DDQN"):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = lr
        self.name = name

        with tf.variable_scope(self.name):
            
            # We create the placeholders
            # *state_size means that we take each elements of state_size in tuple hence is like if we wrote
            # [None, 100, 120, 4]
            self.inputs_ = tf.placeholder(tf.float32, [None, *state_size], name="inputs")
            
            #
            self.ISWeights_ = tf.placeholder(tf.float32, [None,1], name='IS_weights')
            
            self.actions_ = tf.placeholder(tf.float32, [None, action_size], name="actions_")
            
            # Remember that target_Q is the R(s,a) + ymax Qhat(s', a')
            self.target_Q = tf.placeholder(tf.float32, [None], name="target")
            
            """
            First convnet:
            CNN
            ELU
            """
            # Input is 100x120x4
            self.conv1 = tf.layers.conv2d(inputs = self.inputs_,
                                         filters = 32,
                                         kernel_size = [8,8],
                                         strides = [4,4],
                                         padding = "VALID",
                                          kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                                         name = "conv1")
            
            self.conv1_out = tf.nn.elu(self.conv1, name="conv1_out")
            
            
            """
            Second convnet:
            CNN
            ELU
            """
            self.conv2 = tf.layers.conv2d(inputs = self.conv1_out,
                                 filters = 64,
                                 kernel_size = [4,4],
                                 strides = [2,2],
                                 padding = "VALID",
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                                 name = "conv2")

            self.conv2_out = tf.nn.elu(self.conv2, name="conv2_out")
            
            
            """
            Third convnet:
            CNN
            ELU
            """
            self.conv3 = tf.layers.conv2d(inputs = self.conv2_out,
                                 filters = 128,
                                 kernel_size = [4,4],
                                 strides = [2,2],
                                 padding = "VALID",
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                                 name = "conv3")

            self.conv3_out = tf.nn.elu(self.conv3, name="conv3_out")
            
            
            self.flatten = tf.layers.flatten(self.conv3_out)


            self.value_fc = tf.layers.dense(inputs = self.flatten,
                        units = 512,
                        activation = tf.nn.elu,
                        kernel_initializer=tf.contrib.layers.xavier_initializer(),
                        name="value_fc")
                
            self.value = tf.layers.dense(inputs = self.value_fc,
                        units = 1,
                        activation = None,
                        kernel_initializer=tf.contrib.layers.xavier_initializer(),
                        name="value")
            
            # Ccalculate A(s,a)
            self.advantage_fc = tf.layers.dense(inputs = self.flatten,
                        units = 512,    
                        activation = tf.nn.elu,
                        kernel_initializer=tf.contrib.layers.xavier_initializer(),
                        name="advantage_fc")
            
            self.advantage = tf.layers.dense(inputs = self.advantage_fc,
                        units = self.action_size,
                        activation = None,
                        kernel_initializer=tf.contrib.layers.xavier_initializer(),
                        name="advantages")
            
            # Agregating layer
            # Q(s,a) = V(s) + (A(s,a) - 1/|A| * sum A(s,a'))
            self.output = self.value + tf.subtract(self.advantage, 
                tf.reduce_mean(self.advantage, axis=1, keepdims=True))
                
            # Q is our predicted Q value.
            self.Q = tf.reduce_sum(tf.multiply(self.output, self.actions_), axis=1)
            
            # The loss is modified because of PER 
            self.absolute_errors = tf.abs(self.target_Q - self.Q)
            
            self.loss = tf.reduce_mean(
                self.ISWeights_ * tf.squared_difference(self.target_Q, self.Q))
            
            self.optimizer = tf.train.RMSPropOptimizer(
                self.learning_rate).minimize(self.loss)
    
    def predict_action(explore_start, explore_stop, decay_rate, decay_step, state, actions):

