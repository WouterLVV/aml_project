import tensorflow as tf
from logic.game import Hearts
import numpy as np
from logic.cards import cards_to_vector, suits_to_vector, Suit
import matplotlib.pyplot as plt


class Simulator:
    def __init__(self, players, number_of_games_per_cycle, number_of_update_cycles, neural_network, update_rate, tensorflow_session):
        self.players = players
        self.number_of_update_cycles = number_of_update_cycles
        self.number_of_games = number_of_games_per_cycle
        self.neural_network = neural_network
        self.played_games = []
        self.update_rate = update_rate
        self.losses = []
        self.game_count = 0
        self.tensorflow_session = tensorflow_session

    def run_games(self):
        for _ in range(self.number_of_games):
            hearts = Hearts(players=self.players)
            hearts.play_game()
            self.game_count += 1
            print("Scores: {}".format(hearts.scores))
            self.played_games.append(hearts)

    def run_cycles(self):
        variable_initializer = tf.global_variables_initializer()
        self.tensorflow_session.run(variable_initializer)
        for _ in range(self.number_of_update_cycles):
            self.run_games()
            history = self.collect_histories()
            self.reset_games()

            for i in range(len(self.players)):
                states, actions, rewards, next_states, final_states = self.separate_history(history, player_id=i)
                targets = [r if f else r+self.update_rate*np.min(self.tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: np.array([ns])})) for (r, f, ns) in zip(rewards, final_states, next_states)]
                loss, _ = self.tensorflow_session.run([self.neural_network.loss, self.neural_network.optimizer],
                                                      feed_dict={self.neural_network.inputs_: states,
                                                                 self.neural_network.target_Q: targets,
                                                                 self.neural_network.action_: actions})

            self.losses.append(loss)
            print("----------------- NEW EPOCH -----------------")

    def collect_histories(self):
        history = []
        for game in self.played_games:
            for round_ in game.history:
                action_vector = [cards_to_vector([card]) for card in round_.cards]

                hands_vector = [cards_to_vector(hand) for hand in round_.hands]
                discard_vector = [cards_to_vector(round_.combined_discardpile) for _ in range(4)]
                action_vector_based_on_order_of_play = np.concatenate((round_.cards[round_.first_player_id:], round_.cards[:round_.first_player_id]))
                table_vector = [np.zeros((52,), dtype=np.bool) if k == 0 else cards_to_vector(action_vector_based_on_order_of_play[:k]) for k in range(4)]
                first_suit_vector = [suits_to_vector([round_.first_suit]) if round_.first_player_id == x else suits_to_vector([Suit(0)]) for x in range(4)]
                state_vector = [np.concatenate(p) for p in zip(hands_vector, discard_vector, table_vector, first_suit_vector)]

                reward_vector = round_.rewards

                final_states_vector = [True]*4 if len(round_.hands[0]) == 1 else [False]*4

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

    def plot_losses(self):
        plt.plot(range(len(self.losses)), self.losses)
        plt.title('Value loss function per cycle')
        plt.xlabel('Number of cycles')
        plt.ylabel('Value loss function')
        plt.show()
