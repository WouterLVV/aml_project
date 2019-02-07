import tensorflow as tf
import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.engine import InputLayer
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.models import save_model, load_model


class TensorNetwork:
    """"
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
        self.loss; norm 2 error function on Qhat-hat with Qhat = r + gamma*min_{a\inA} Q(s',a) where A is the set of possible action and s' the state after a round.
    """

    def __init__(self, state_size, action_size, hidden_sizes, layer_activation_functions, learning_rate,
                 name='DQNetwork'):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.hidden_sizes = hidden_sizes
        self.layer_activation_functions = layer_activation_functions
        self.name = name

        try:
            assert len(self.layer_activation_functions) == len(self.hidden_sizes) + 1
        except AssertionError:
            if len(self.layer_activation_functions) > len(self.hidden_sizes) + 1:
                print("Too many activation functions, must be length(hidden sizes) +1 ")
            else:
                print("Too few activation functions, must be length(hidden sizes) +1 ")
            exit(1)

        with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
            self.inputs_ = tf.placeholder(tf.float32, shape=[None, self.state_size], name="inputs")
            self.action_ = tf.placeholder(tf.float32, shape=[None, self.action_size], name="actions_")
            self.target_Q = tf.placeholder(tf.float32, [None], name="target")

            input_ = self.inputs_
            input_size = self.state_size
            self.hidden_sizes.append(self.action_size)
            for i, (output_size, activation_function) in enumerate(
                    zip(self.hidden_sizes, self.layer_activation_functions)):
                if activation_function == "sigmoid":
                    input_ = tf.nn.sigmoid(
                        tf.matmul(input_, self.init_weights("w{}".format(i), [input_size, output_size])))
                elif activation_function == "relu":
                    input_ = tf.nn.relu(
                        tf.matmul(input_, self.init_weights("w{}".format(i), [input_size, output_size])))
                elif activation_function == "elu":
                    input_ = tf.nn.elu(tf.matmul(input_, self.init_weights(str(i), [input_size, output_size])))
                elif activation_function == "softplus":
                    input_ = tf.nn.softplus(tf.matmul(input_, self.init_weights(str(i), [input_size, output_size])))
                elif activation_function == "softsign":
                    input_ = tf.nn.softsign(tf.matmul(input_, self.init_weights(str(i), [input_size, output_size])))
                elif activation_function == "softmax":
                    input_ = tf.nn.softmax(tf.matmul(input_, self.init_weights(str(i), [input_size, output_size])))
                elif activation_function == "tanh":
                    input_ = tf.nn.tanh(
                        tf.matmul(input_, self.init_weights("w{}".format(i), [input_size, output_size])))
                elif activation_function == "lin":
                    input_ = tf.matmul(input_, self.init_weights("w{}".format(i), [input_size, output_size]))
                elif activation_function == "leaky_relu":
                    input_ = tf.nn.leaky_relu(tf.matmul(input_, self.init_weights(str(i), [input_size, output_size])))
                else:
                    print("please specify proper activation_function.")
                    print("%s is not a valid activation function for this network." % activation_function)
                    exit(2)
                input_size = output_size
            del self.hidden_sizes[-1]
            self.output = input_

            ## --------------
            # Q is our predicted Q value.
            ## --------------
            self.Q = tf.reduce_sum(tf.multiply(self.output, self.action_))

            ## --------------
            # The loss is the difference between our predicted Q_values and the Q_target
            # Sum(Qtarget - Q)^2
            ## --------------
            self.loss = tf.reduce_mean(tf.square(self.target_Q - self.Q))

            self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)

    @staticmethod
    def init_weights(name, shape):
        return tf.get_variable(name=name,
                               shape=shape,
                               initializer=tf.random_normal_initializer(stddev=0.001))


class KerasNetwork:
    def __init__(self, discount_factor, name='DQNetwork',
                 model=None, state_size=None, action_size=None, hidden_sizes=None,
                 hidden_activation_functions=None, output_activation_function=None):
        self.name = name
        self.discount_factor = discount_factor
        if model is not None:
            self.model = load_model(model)
        else:
            try:
                assert state_size is not None
                assert action_size is not None
                assert output_activation_function is not None
            except AssertionError:
                print("Network needs to know at least state_size, actionsize, and have an output_activation_function")
            try:
                if hidden_activation_functions is not None or hidden_sizes is not None:
                    assert len(hidden_activation_functions) == len(hidden_sizes)
            except AssertionError:
                if len(hidden_activation_functions) > len(hidden_sizes):
                    print("Too many hidden activation functions, must have length(hidden sizes) ")
                else:
                    print("Too few hidden activation functions, must have length(hidden sizes) ")
                exit(1)
            except TypeError:
                print("Either hidden_activation_functions or hidden_sizes is None; Make both None or neither.")

            self.model = Sequential()
            self.model.add(InputLayer(input_shape=(state_size,)))
            if hidden_activation_functions is not None and hidden_sizes is not None:
                hidden_inputs = np.roll(hidden_sizes, 1)
                hidden_inputs[0] = state_size
                for s, i, a in zip(hidden_sizes, hidden_inputs, hidden_activation_functions):
                    self.model.add(Dense(s, input_dim=i, activation=a))
                    self.model.add(Dropout(0.1))
            self.model.add(Dense(action_size, input_dim=state_size, activation=output_activation_function))
            self.model.compile(loss='mse', optimizer='adam', metrics=['mse'])

    def summary(self):
        return self.model.summary()

    def save(self, path):
        save_model(self.model, path)

    def load(self, path):
        self.model = load_model(path)

    def generate_target_vecs(self, states, actions, rewards, next_states, final_states):
        target_vecs = [self.model.predict(np.array([state]))[0] for state in states]
        for vec, action, reward, next_state, final_state in zip(target_vecs, actions, rewards, next_states, final_states):
            if final_state or self.discount_factor == 0:
                vec[action] = reward
            else:
                vec[action] = reward + self.discount_factor*np.min(self.model.predict(np.array([next_state]))[0])
        return target_vecs

# targets = [r if True else r + self.update_rate * np.min(
# self.neural_network.model.predict(np.array(ns).reshape((1,52))))
# for (r, f, ns) in zip(rewards, final_states, next_states)]
# target_vecs = [self.neural_network.model.predict(np.array([state])) for state in states ]
# for s,a,r,ns,fs,t,tv in zip(states, actions, rewards, next_states, final_states, targets, target_vecs):
#     self.neural_network.model.fit(np.array(s).reshape((1,161)), np.array(tv).reshape((1,52)), epochs=1, verbose=False)
