from logic.agent import Agent
from logic.cards import STANDARDDECK, cards_to_vector, suits_to_vector, NUM2CARD
import random
import numpy as np
import tensorflow as tf


class ml_agent(Agent):
    def __init__(self, neural_network, deck=STANDARDDECK, games_played=0, decay_rate=1):
        Agent.__init__(self, deck)
        self.neural_network = neural_network
        self.name = "Learned AI"
        self.games_played = games_played
        self.decay_rate = decay_rate

    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)

        state = self.get_state(table, player_id)

        random_checker = np.random.rand()
        if self.get_exploration_rate() > random_checker:
            card = options[random.randrange(0, len(options))]
        else:
            with tf.Session() as tensorflow_session:
                # TODO kijk of dit wel strookt met session in Simulator
                variable_initializer = tf.global_variables_initializer()
                tensorflow_session.run(variable_initializer)
                choices = np.array(tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: [state]}))
                choice = np.argmin((choices+100)*np.array([np.inf if x == 0 else 1 for x in cards_to_vector(self.hand)]))
            card = NUM2CARD[choice]
        return card

    def get_state(self, table, player_id):
        hands_vector = cards_to_vector(table.hands[player_id])
        table_vector = cards_to_vector(table.cards)
        discard_vector = cards_to_vector(table.combined_discardpile)
        first_suit_vector = suits_to_vector([table.first_suit])
        return np.concatenate((hands_vector, table_vector, discard_vector, first_suit_vector))

    def get_exploration_rate(self):
        return np.exp(-self.decay_rate*self.games_played)

    def end_game(self):
        score = super(ml_agent, self).end_game()
        self.games_played += 1
        return score

    def reset(self, deck):
        self.__init__(deck=deck, neural_network=self.neural_network, games_played=self.games_played)
