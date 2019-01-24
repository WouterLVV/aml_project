from Network.Network import DQNetwork
from ai.keras_agent import KerasAgent
from ai.keras_simulator import KerasSimulator
from ai.kerasnet import KerasNetwork
from logic.simulator import Simulator, RandomGameSimulator
from ai.ml_agent import ml_agent
import time
import tensorflow as tf

start_time = time.time()
with tf.Session() as tensorflow_session:
    neural_network = KerasNetwork(state_size=161,
                               action_size=52,
                               hidden_sizes=[100, 100, 100],
                               layer_activation_functions=['tanh', 'tanh', 'tanh', 'linear'],
                               learning_rate=0.3)
    # new_saver = tf.train.import_meta_graph('saved_tensorflow_sessions/tensorflow_session.meta')
    # new_saver.restore(tensorflow_session, tf.train.latest_checkpoint('saved_tensorflow_sessions/'))
    saver = tf.train.Saver()
    players = [KerasAgent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=1.0),
               KerasAgent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.00),
               KerasAgent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.000),
               KerasAgent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.0000)]
    # simulator = RandomGameSimulator(
    #                     number_of_games_per_cycle=20,
    #                     number_of_update_cycles=20,
    #                     neural_network=neural_network,
    #                     update_rate=0.9,
    #                     tensorflow_session=tensorflow_session,
    #                     thread_count=10)
    # simulator.run_cycles()
    playsim = KerasSimulator(players=players,
                        number_of_games_per_cycle=20,
                        number_of_update_cycles=500,
                        neural_network=neural_network,
                        update_rate=0.1,
                        tensorflow_session=tensorflow_session)
    playsim.run_cycles()
    saver.save(tensorflow_session, './saved_tensorflow_sessions/tensorflow_session')

end_time = time.time()
t = end_time-start_time
print("Total time taken: {}".format(t))
# print("Average time per game: {}". format(t/(simulator.number_of_games*simulator.number_of_update_cycles)))
# simulator.plot_losses()
