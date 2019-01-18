from Network.Network import DQNetwork
from logic.simulator import Simulator
from ai.ml_agent import ml_agent
from logic.agent import RandomAI
import time
import tensorflow as tf

start_time = time.time()
with tf.Session() as tensorflow_session:
    neural_network = DQNetwork(state_size=161,
                               action_size=52,
                               hidden_sizes=[250, 200, 200, 150, 100],
                               layer_activation_functions=['relu', 'relu', 'relu', 'relu', 'relu', 'softmax'],
                               learning_rate=0.3)
    saver = tf.train.Saver()
    players = [ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.000),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.000),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.000),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.000)]
    simulator = Simulator(players=players,
                          number_of_games_per_cycle=100000,
                          number_of_update_cycles=1,
                          neural_network=neural_network,
                          update_rate=0.9,
                          tensorflow_session=tensorflow_session)
    simulator.run_cycles()
    saver.save(tensorflow_session, './saved_tensorflow_sessions/tensorflow_session')

end_time = time.time()
t = end_time-start_time
print("Total time taken: {}".format(t))
print("Average time per game: {}". format(t/(simulator.number_of_games*simulator.number_of_update_cycles)))
simulator.plot_losses()
