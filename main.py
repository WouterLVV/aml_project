from Network.Network import DQNetwork
from logic.simulator import Simulator, RandomGameSimulator
from ai.ml_agent import ml_agent
import time
import tensorflow as tf

start_time = time.time()
with tf.Session() as tensorflow_session:
    neural_network = DQNetwork(state_size=161,
                               action_size=52,
                               hidden_sizes=[250, 200, 200, 150, 100],
                               layer_activation_functions=['relu', 'relu', 'relu', 'relu', 'relu', 'softmax'],
                               learning_rate=0.3)
    # new_saver = tf.train.import_meta_graph('saved_tensorflow_sessions/tensorflow_session.meta')
    # new_saver.restore(tensorflow_session, tf.train.latest_checkpoint('saved_tensorflow_sessions/'))
    saver = tf.train.Saver()
    players = [ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=1.000),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.010),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.010),
               ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=0.010)]
    simulator = RandomGameSimulator(
                        number_of_games_per_cycle=2000,
                        number_of_update_cycles=200,
                        neural_network=neural_network,
                        update_rate=0.9,
                        tensorflow_session=tensorflow_session,
                        thread_count=10)
    simulator.run_cycles()
    playsim = Simulator(players=players,
                        number_of_games_per_cycle=20,
                        number_of_update_cycles=50,
                        neural_network=neural_network,
                        update_rate=0.9,
                        tensorflow_session=tensorflow_session)
    playsim.run_cycles()
    saver.save(tensorflow_session, './saved_tensorflow_sessions/tensorflow_session')

end_time = time.time()
t = end_time-start_time
print("Total time taken: {}".format(t))
# print("Average time per game: {}". format(t/(simulator.number_of_games*simulator.number_of_update_cycles)))
# simulator.plot_losses()
