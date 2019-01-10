import tensorflow as tf


class DQNetwork:
    '''
    Neural network
    -----------------------
    inputs:
        statesize |s|, integer trice the size of the deck; representing the number of cards in the players hand, the cards played already, and the cards on the table.
        actionsize |a|, integer the size of the deck; representing the cards playable.
        learning_rate, value between 0 and 1; represents the rate at which the network learns from new experiences and discards older experiences.
        hidden_size, integer array; represents the number of nodes each of the hidden layers have
        layer_activation_functions, string array; represents the activation funtions used in each layer, including the output.
        name, string; represents the name associated with the neural network
    outputs:
        self.output; Calculate [Q(s'_1,a_1),...Q(s'_n,a_n)] with s'_i is the state after applying a_i on given input state s
        self.loss; norm 2 error function on Qhat-hat with Qhat = r + gamma*max_{a\inA} Q(s',a) where A is the set of possible action and s' the state after a round.
    '''
    def __init__(self, state_size, action_size, hidden_sizes, layer_activation_functions, learning_rate, name='DQNetwork'):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.hidden_sizes = hidden_sizes
        self.layer_activation_functions = layer_activation_functions

        try:
            assert len(self.layer_activation_functions) != len(self.hidden_sizes)+1
        except AssertionError:
            if len(self.layer_activation_functions) > len(self.hidden_sizes)+1:
                print("Too many activation functions, must be length(hidden sizes) +1 ")
            else:
                print("Too few activation functions, must be length(hidden sizes) +1 ")
            exit(1)

        with tf.variable_scope(name):
            self.inputs_ = tf.placeholder(tf.float32, [None, self.state_size], name="inputs")
            self.actions_ = tf.placeholder(tf.float32, [None, self.action_size], name="actions_")
            self.target_Q = tf.placeholder(tf.float32, [None], name="target")

            input_ = self.inputs_
            input_size = self.state_size
            self.hidden_sizes.append(self.action_size)
            for (output_size, activation_function) in zip(self.hidden_sizes, self.layer_activation_functions):
                if activation_function == "sigmoid":
                    input_ = tf.nn.sigmoid(tf.matmul(input_, self.init_weights([input_size, output_size])))
                elif activation_function == "relu":
                    input_ = tf.nn.relu(tf.matmul(input_, self.init_weights([input_size, output_size])))
                elif activation_function == "elu":
                    input_ = tf.nn.elu(tf.matmul(input_, self.init_weights([input_size, output_size])))
                else:
                    print("please specify proper activation_function.")
                    print("%s is not a valid activation function for this network." % activation_function)
                    exit(2)
                input_size = output_size
            del self.hidden_sizes[-1]
            self.output = input_

            # Q is our predicted Q value.
            self.Q = tf.reduce_sum(tf.multiply(self.output, self.actions_))

            # The loss is the difference between our predicted Q_values and the Q_target
            # Sum(Qtarget - Q)^2
            self.loss = tf.reduce_mean(tf.square(self.target_Q - self.Q))

            self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)

    @staticmethod
    def init_weights(shape):
        return tf.Variable(tf.random_normal(shape, stddev=0.01))
