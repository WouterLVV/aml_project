from Network.Network import DQNetwork
from logic.simulator import Simulator, RandomGameSimulator
from ai.ml_agent import ml_agent
from logic.agent import YoloAI
import time
import tensorflow as tf
import numpy as np


if __name__ == '__main__':
    load_previously_trained_network = True

    start_time = time.time()
    with tf.Session() as tensorflow_session:
        neural_network = DQNetwork(state_size=52,
                                   action_size=52,
                                   hidden_sizes=[],
                                   layer_activation_functions=['lin'],
                                   learning_rate=0.000005)
        saver = tf.train.Saver()
        if load_previously_trained_network:
            saver.restore(tensorflow_session, tf.train.latest_checkpoint('saved_tensorflow_sessions/'))
        else:
            variable_initializer = tf.global_variables_initializer()
            tensorflow_session.run(variable_initializer)

        ml_players = [ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=10.000),
                      ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=10.000),
                      ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=10.000),
                      ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=10.000)]
        mixed_players = [ml_agent(neural_network=neural_network, tensorflow_session=tensorflow_session, decay_rate=1.000),
                         YoloAI(),
                         YoloAI(),
                         YoloAI()]
        yolo_players = [YoloAI(), YoloAI(), YoloAI(), YoloAI()]
        simulator_random_deck = RandomGameSimulator(
                            number_of_games_per_cycle=500,
                            number_of_update_cycles=2000,
                            neural_network=neural_network,
                            future_reward_factor=0.9,
                            tensorflow_session=tensorflow_session,
                            thread_count=1,
                            random_from_deck_instead_of_hand=True)
        simulator_random = RandomGameSimulator(
                            number_of_games_per_cycle=200,
                            number_of_update_cycles=1000,
                            neural_network=neural_network,
                            future_reward_factor=0.9,
                            tensorflow_session=tensorflow_session,
                            thread_count=1,
                            random_from_deck_instead_of_hand=False)
        simulator_yolo = Simulator(players=yolo_players,
                                   number_of_games_per_cycle=200,
                                   number_of_update_cycles=250,
                                   neural_network=neural_network,
                                   future_reward_factor=0.001,
                                   tensorflow_session=tensorflow_session)
        simulator_player = Simulator(players=ml_players,
                                     number_of_games_per_cycle=20,
                                     number_of_update_cycles=1,
                                     neural_network=neural_network,
                                     future_reward_factor=0.1,
                                     tensorflow_session=tensorflow_session)
        # simulator_random_deck.run_cycles()
        # simulator_random.run_cycles()
        # simulator_yolo.run_cycles()
        # simulator_player.run_cycles()
        # vars_ = tf.trainable_variables()
        # vars_vals = tensorflow_session.run(vars_)
        # for var, val in zip(vars_, vars_vals):
        #     print("var: {}, value: {}".format(var.name, val))
        # simulator_player.run_games()
        # with tf.variable_scope("DQNetwork", reuse=True):
        #     w = tf.get_variable('w0')
        #     p = w.assign([[1]*52 if x<52 else [0]*52 for x in range(161)])
        #     b = tf.get_variable('b0')
        #     q = b.assign([1]*52)
        #     tensorflow_session.run(p)
        #     tensorflow_session.run(q)
        # vars_ = tf.trainable_variables()
        # vars_vals = tensorflow_session.run(vars_)
        # for var, val in zip(vars_, vars_vals):
        #     print("var: {}, value: {}".format(var.name, val))
        # simulator_player.run_games()
        saver.save(tensorflow_session, './saved_tensorflow_sessions/tensorflow_session2')
        print("Only clubs")
        print(np.array(tensorflow_session.run(neural_network.output, feed_dict={neural_network.inputs_: [[1]*13+[0]*39]})))
        # print("Only last suit")
        # print(np.array(tensorflow_session.run(neural_network.output, feed_dict={neural_network.inputs_: [[0]*39+[1]*13]})))

    end_time = time.time()
    t = end_time-start_time
    print("Total time taken: {}".format(t))
    # print(simulator_player.player_wins)
    # print(simulator_player.player_losses)
    simulator_random_deck.plot_losses()
    simulator_random.plot_losses()
    simulator_yolo.plot_losses()
    simulator_player.plot_losses()
