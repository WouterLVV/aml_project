import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.engine import InputLayer
from tensorflow.python.keras.layers import Dense


class KerasNetwork:
    def __init__(self, state_size, action_size, hidden_sizes, layer_activation_functions, learning_rate, name='DQNetwork'):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.hidden_sizes = hidden_sizes
        self.layer_activation_functions = layer_activation_functions
        self.name = name

        try:
            assert len(self.layer_activation_functions) == len(self.hidden_sizes)+1
        except AssertionError:
            if len(self.layer_activation_functions) > len(self.hidden_sizes)+1:
                print("Too many activation functions, must be length(hidden sizes) +1 ")
            else:
                print("Too few activation functions, must be length(hidden sizes) +1 ")
            exit(1)

        self.model = Sequential()
        self.model.add(InputLayer(input_shape=(self.state_size,), batch_size=1))
        # self.model.add(Dense(100, activation='tanh'))
        # self.model.add(Dense(100, activation='tanh'))
        self.model.add(Dense(self.action_size, activation='linear'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['mse'])



