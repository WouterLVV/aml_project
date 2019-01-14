import tensorflow as tf
from logic.game import Hearts
import numpy as np
from logic.cards import cards_to_vector, suits_to_vector, Suit

class Simulator:
    def __init__(self, players, number_of_games, number_of_update_cycles, neural_network, update_rate):
        self.players = players
        self.number_of_update_cyles = number_of_update_cycles
        self.number_of_games = number_of_games
        self.neural_network = neural_network
        self.played_games = []
        self.update_rate = update_rate

    def run_games(self):
        for _ in range(self.number_of_games):
            hearts = Hearts(players=self.players)
            hearts.play_game()
            self.played_games.append(hearts)

    def run_cycles(self):
        with tf.Session() as sess:
            for _ in range(self.number_of_update_cyles):
                self.run_games()

                history = self.collect_histories()

                states, actions, rewards, next_states, final_states = self.separate_histories(history)
                targets = []

                # Get Q values for next_state
                Qs_next_state = sess.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: next_states})

                # Set Q_target = r if the episode ends at s+1, otherwise set Q_target = r + gamma*maxQ(s', a')
                for i in range(13):
                    if final_states[i]:
                        targets.append(rewards[i])
                    else:
                        targets.append(rewards[i] + self.update_rate * np.max(next_states[i]))

                loss, _ = sess.run([self.neural_network.loss, self.neural_network.optimizer],
                                   feed_dict={self.neural_network.inputs_: states,
                                              self.neural_network.target_Q: targets,
                                              self.neural_network.actions_: actions})

    def collect_histories(self):
        for game in self.played_games:
            for round_ in game.history:
                for i, (p, h, c, d, f, id) in enumerate(zip(round_.players, round_.hands, round_.cards, round_.discardpiles, round_.first_suit, round_.first_player_id)):
                    hands_vector = [cards_to_vector(hand) for hand in h]
                    table_vector = [cards_to_vector(card) for card in c]
                    discard_vector = [cards_to_vector(discard) for discard in d]
                    first_suit_vector = [suits_to_vector(f) if id == x else suits_to_vector(Suit(0)) for x in range(0, 4)]
                    state_vector = [hv+tv+dv+fv for (hv, tv, dv, fv) in zip(hands_vector, table_vector, discard_vector, first_suit_vector)]
        history = [0, 0, 0, 0, 0]
        return history

    def separate_histories(self, history):
        states = np.array([each[0] for each in history], ndmin=3)
        actions = np.array([each[1] for each in history])
        rewards = np.array([each[2] for each in history])
        next_states = np.array([each[3] for each in history], ndmin=3)
        final_states = np.array([each[4] for each in history])
        return [states, actions, rewards, next_states, final_states]
