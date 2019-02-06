import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import time
import sys

from models.round import Hearts
from models.deck import STANDARDDECK
from models.suits import Suit


class Simulator:
    def __init__(self, players, number_of_games_per_cycle, number_of_update_cycles, neural_network, future_reward_factor, tensorflow_session, data_transformer, deck=STANDARDDECK):
        self.players = players
        self.number_of_update_cycles = number_of_update_cycles
        self.number_of_games = number_of_games_per_cycle
        self.neural_network = neural_network
        self.played_games = []
        self.player_losses = [0]*len(players)
        self.player_wins = [0]*len(players)
        self.future_reward_factor = future_reward_factor
        self.losses = []
        self.game_count = 0
        self.tensorflow_session = tensorflow_session
        self.data_transformer = data_transformer
        self.deck = deck

    def run_games(self):
        for _ in range(self.number_of_games):
            hearts = Hearts(players=self.players, deck=self.deck)
            hearts.play_game()
            self.game_count += 1
            self.player_wins[hearts.winning_player()] += 1
            self.player_losses[hearts.losing_player()] += 1
            print("{:8}\tScores: {}".format(self.game_count, hearts.scores))
            self.played_games.append(hearts)

    def run_cycles(self):
        for m in range(1, self.number_of_update_cycles+1):
            print("----------------- EPOCH {} -----------------".format(m))
            start_time = time.time()
            self.run_games()
            history = self.collect_histories()
            self.reset_games()

            print("Games are done")
            end_time = time.time()
            t = end_time - start_time
            print("Time taken to simulate: {}".format(t))

            for i in range(len(self.players)):
                states, actions, rewards, next_states, final_states = self.separate_history(history, player_id=i)
                ## --------------
                # Assign the targets using a future_reward_factor of 0
                ## --------------
                targets = rewards

                ## --------------
                # Assign the targets properly
                ## --------------
                # targets = [r if f else r+self.future_reward_factor*np.min(self.tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: np.array([ns])})) for (r, f, ns) in zip(rewards, final_states, next_states)]

                ## --------------
                # Assign the targets based on only valid actions
                ## --------------
                # targets = [r if f else r+self.future_reward_factor*np.min(self.tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: np.array([ns])})+np.array([np.inf if x == 0 else 0 for x in ns[0:52]])) for (r, f, ns) in zip(rewards, final_states, next_states)]

                loss, _ = self.tensorflow_session.run([self.neural_network.loss, self.neural_network.optimizer],
                                                      feed_dict={self.neural_network.inputs_: states,
                                                                 self.neural_network.target_Q: targets,
                                                                 self.neural_network.action_: actions})
            self.losses.append(loss)

    def collect_histories(self):
        history = []
        for game in self.played_games:
            for round_ in game.history:
                action_vector = [self.data_transformer.cards_to_vector([card]) for card in round_.attempted_cards]

                hands_vector = [self.data_transformer.cards_to_vector(hand) for hand in round_.hands]
                discard_vector = [self.data_transformer.cards_to_vector(round_.combined_discardpile) for _ in range(4)]
                action_vector_based_on_order_of_play = np.concatenate((round_.cards[round_.first_player_id:], round_.cards[:round_.first_player_id]))
                table_vector = [np.zeros((24,), dtype=np.bool) if k == 0 else self.data_transformer.cards_to_vector(action_vector_based_on_order_of_play[:k]) for k in range(4)]
                first_suit_vector = [self.data_transformer.suits_to_vector([round_.first_suit]) if round_.first_player_id == x else self.data_transformer.suits_to_vector([Suit(0)]) for x in range(4)]

                ## --------------
                # Get state for good cards
                ## --------------
                state_vector = [np.concatenate(p) for p in zip(hands_vector, discard_vector, table_vector, first_suit_vector)]

                ## --------------
                # Get state for valid cards
                ## --------------
                state_vector = [np.concatenate(p) for p in zip(hands_vector, table_vector, first_suit_vector)]

                ## --------------
                # Get state for hand cards
                ## --------------
                state_vector = hands_vector

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

        next_states = [None if x % 13 == 12 else states[x + 1] for x in range(len(states))]
        return [states, actions, rewards, next_states, final_states]

    def reset_games(self):
        self.played_games = []

    def reset_win_and_losees(self):
        self.player_wins = [0]*len(self.players)
        self.player_losses = [0]*len(self.players)

    def plot_losses(self):
        plt.plot(range(len(self.losses)), self.losses)
        plt.title('Value loss function per cycle')
        plt.xlabel('Number of cycles')
        plt.ylabel('Value loss function')
        plt.show()


class KerasSimulator(Simulator):
    def run_cycles(self):
        for m in range(self.number_of_update_cycles):
            print("----------------- EPOCH {} -----------------".format(m))
            start_time = time.time()
            self.run_games()
            history = self.collect_histories()
            self.reset_games()

            #print("Games are done")
            end_time = time.time()
            t = end_time - start_time
            #print("Time taken to simulate: {}".format(t))
            # print("Combined scores: {}".format(totalscore))

            for i in range(len(self.players)):
                states, actions, rewards, next_states, final_states = self.separate_history(history, player_id=i)

                #targets = [r if True else r + self.update_rate * np.min(
                           # self.neural_network.model.predict(np.array(ns).reshape((1,52))))
                           # for (r, f, ns) in zip(rewards, final_states, next_states)]

                targets = rewards
                # target_vecs = [self.neural_network.model.predict(np.array([state])) for state in states ]
                target_vecs = [self.neural_network.model.predict(state.reshape((1,52)))[0] for state in states ]
                for vec, action, target in zip(target_vecs, actions, targets):
                    vec[action] = target

                loss = self.neural_network.model.fit(np.array(states), np.array(target_vecs), batch_size=1, epochs=1, verbose=False)
                self.losses.append(loss)

                # for s,a,r,ns,fs,t,tv in zip(states, actions, rewards, next_states, final_states, targets, target_vecs):
                #     self.neural_network.model.fit(np.array(s).reshape((1,161)), np.array(tv).reshape((1,52)), epochs=1, verbose=False)

            # self.losses.append(-1)
            # sys.stdout.flush()

    def plot_losses(self):
        plt.plot(range(len(self.losses)), [h.history['mean_squared_error'] for h in self.losses])
        plt.title('Value loss function per cycle')
        plt.xlabel('Number of cycles')
        plt.ylabel('Value loss function')
        plt.show()
