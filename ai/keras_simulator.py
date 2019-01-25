import tensorflow as tf
from logic.game import Hearts
import numpy as np
from logic.cards import cards_to_vector, suits_to_vector, Suit
import matplotlib.pyplot as plt
import time
from logic.simulator import Simulator
import sys

class KerasSimulator(Simulator):

    def __init__(self, players, number_of_games_per_cycle, number_of_update_cycles, neural_network, update_rate, tensorflow_session):
        Simulator.__init__(self, players, number_of_games_per_cycle, number_of_update_cycles, neural_network, update_rate, tensorflow_session)

    def run_cycles(self):
        variable_initializer = tf.global_variables_initializer()
        self.tensorflow_session.run(variable_initializer)
        for m in range(self.number_of_update_cycles):
            start_time = time.time()
            self.run_games()
            history, totalscore = self.collect_histories()
            self.reset_games()

            #print("Games are done")
            end_time = time.time()
            t = end_time - start_time
            #print("Time taken to simulate: {}".format(t))
            print("Combined scores: {}".format(totalscore))

            for i in range(len(self.players)):
                states, actions, rewards, next_states, final_states = self.separate_history(history, player_id=i)

                # targets = [r if f else r + self.update_rate * np.min(
                #     self.tensorflow_session.run(self.neural_network.output,
                #                                 feed_dict={self.neural_network.inputs_: np.array([ns])}))
                #            for (r, f, ns) in zip(rewards, final_states, next_states)]
                targets = [r if f else r + self.update_rate * np.min(
                           self.neural_network.model.predict(np.array(ns).reshape((1,161))))
                           for (r, f, ns) in zip(rewards, final_states, next_states)]

                target_vecs = [self.neural_network.model.predict(state.reshape((1,161)))[0] for state in states ]
                for vec, action, target in zip(target_vecs, actions, targets):
                    vec[action] = target

                # loss, _ = self.tensorflow_session.run([self.neural_network.loss, self.neural_network.optimizer],
                #                                       feed_dict={self.neural_network.inputs_: states,
                #                                                  self.neural_network.target_Q: targets,
                #                                                  self.neural_network.action_: actions})

                self.neural_network.model.fit(np.array(states), np.array(target_vecs), batch_size=1, epochs=1, verbose=False)

                # for s,a,r,ns,fs,t,tv in zip(states, actions, rewards, next_states, final_states, targets, target_vecs):
                #     self.neural_network.model.fit(np.array(s).reshape((1,161)), np.array(tv).reshape((1,52)), epochs=1, verbose=False)

            self.losses.append(-1)
            print("----------------- EPOCH {} -----------------".format(m))
            sys.stdout.flush()