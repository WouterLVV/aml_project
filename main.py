from Network.Network import DQNetwork
from logic.simulator import Simulator
from ai.ml_agent import ml_agent
from logic.agent import RandomAI
import time
import tensorflow as tf

start_time = time.time()
with tf.Session() as tensorflow_session:
    neural_network = DQNetwork(161, 52, [200, 100, 100], ['sigmoid', 'elu', 'relu', 'sigmoid'], 0.3)
    players = [ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session)]
    simulator = Simulator(players=players,
                          number_of_games_per_cycle=50,
                          number_of_update_cycles=100,
                          neural_network=neural_network,
                          update_rate=0.4,
                          tensorflow_session=tensorflow_session)
    simulator.run_cycles()


end_time = time.time()
t = end_time-start_time
print("Total time taken: {}".format(t))
print("Average time per game: {}". format(t/(simulator.number_of_games*simulator.number_of_update_cycles)))
simulator.plot_losses()
