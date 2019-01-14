import tensorflow as tf
from logic.game import Hearts
import numpy as np
from logic.cards import cards_to_vector, suits_to_vector, Suit


class Simulator:
    def __init__(self, players, number_of_games_per_cycle, number_of_update_cycles, neural_network, update_rate):
        self.players = players
        self.number_of_update_cyles = number_of_update_cycles
        self.number_of_games = number_of_games_per_cycle
        self.neural_network = neural_network
        self.played_games = []
        self.update_rate = update_rate
        self.losses = []

    def run_games(self):
        for _ in range(self.number_of_games):
            hearts = Hearts(players=self.players)
            hearts.play_game()
            self.played_games.append(hearts)
            # TODO player score geval reset functie

    def run_cycles(self):
        with tf.Session() as sess:
            for _ in range(self.number_of_update_cyles):
                self.run_games()
                history = self.collect_histories()
                self.reset_games()

                states, actions, rewards, next_states, final_states = self.separate_history(history)

                targets = [r if f else r+self.update_rate*np.max(sess.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: ns})) for (r, f, ns) in zip(rewards, final_states, next_states)]

                loss, _ = sess.run([self.neural_network.loss, self.neural_network.optimizer],
                                   feed_dict={self.neural_network.inputs_: states,
                                              self.neural_network.target_Q: targets,
                                              self.neural_network.actions_: actions})
                self.losses.append(loss)

    def collect_histories(self):
        history = []
        for game in self.played_games:
            for round_ in game.history:
                action_vector = [cards_to_vector(card) for card in round_.cards]

                hands_vector = [cards_to_vector(hand) for hand in round_.hands]
                discard_vector = [cards_to_vector(discard) for discard in round_.discardpiles]
                action_vector_based_on_order_of_play = action_vector[round_.first_player_id:]+action_vector[:round_.first_player_id]
                table_vector = [np.zeros((52,), dtype=np.bool) if k == 0 else np.sum(action_vector_based_on_order_of_play[:k], axis=0) for k in range(0, 4)]
                first_suit_vector = [suits_to_vector(round_.first_suit) if round_.first_player_id == x else suits_to_vector(Suit(0)) for x in range(0, 4)]
                state_vector = [hv+dv+tv+fv for (hv, dv, tv, fv) in zip(hands_vector, discard_vector, table_vector, first_suit_vector)]

                reward_vector = round_.rewards

                final_states_vector = tf.ones(4) if sum(round_.hands[0]) == 1 else tf.zeros(4)

                round_history = {"state": state_vector, "action": action_vector, "reward": reward_vector, "final": final_states_vector}
                history.append(round_history)
        return history

    def separate_history(self, history, player_id=0):
        states = np.array([round_history["state"][player_id] for round_history in history])
        actions = np.array([round_history["action"][player_id] for round_history in history])
        rewards = np.array([round_history["reward"][player_id] for round_history in history])
        final_states = np.array([round_history["final"][player_id] for round_history in history])

        next_states = [None if x % 13 == 12 else states[x+1] for x in range(len(states))]
        return [states, actions, rewards, next_states, final_states]

    def reset_games(self):
        self.played_games = []
