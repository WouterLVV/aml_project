from Network.Network import DQNetwork
from logic.simulator import Simulator, RandomGameSimulator
from ai.ml_agent import ml_agent
import time
import tensorflow as tf


if __name__ == '__main__':
    load_previously_trained_network = True

    start_time = time.time()
    with tf.Session() as tensorflow_session:
        neural_network = DQNetwork(state_size=161,
                                   action_size=52,
                                   hidden_sizes=[100, 100, 100, 100, 100],
                                   layer_activation_functions=['tanh', 'tanh', 'tanh', 'tanh', 'tanh', 'lin'],
                                   learning_rate=0.3)
        saver = tf.train.Saver()
        if load_previously_trained_network:
            saver.restore(tensorflow_session, tf.train.latest_checkpoint('saved_tensorflow_sessions/'))
        else:
            variable_initializer = tf.global_variables_initializer()
            tensorflow_session.run(variable_initializer)

        players = [ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=100.000),
                   ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=100.010),
                   ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=100.010),
                   ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=100.010)]
        simulator = RandomGameSimulator(
                            number_of_games_per_cycle=2000,
                            number_of_update_cycles=20,
                            neural_network=neural_network,
                            future_reward_factor=0.9,
                            tensorflow_session=tensorflow_session,
                            thread_count=1,
                            random_from_deck_instead_of_hand=False)
        simulator.run_cycles()
        playsim = Simulator(players=players,
                            number_of_games_per_cycle=20,
                            number_of_update_cycles=1,
                            neural_network=neural_network,
                            future_reward_factor=0.9,
                            tensorflow_session=tensorflow_session)
        playsim.run_cycles()

        saver.save(tensorflow_session, './saved_tensorflow_sessions/tensorflow_session')

    end_time = time.time()
    t = end_time-start_time
    print("Total time taken: {}".format(t))
    # simulator.plot_losses()
