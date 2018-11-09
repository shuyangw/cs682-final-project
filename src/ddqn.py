import tensorflow as tf

class DDQN(object):
    def __init__(self, state_size, action_size, lr, name="DDQN"):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = lr
        self.name = name

        """
        Traditionally, here is where we would implement CNN layers, we would
        instead like to do it with capsule layers.
        """ 

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
