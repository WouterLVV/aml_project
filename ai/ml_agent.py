from logic.agent import Agent
from logic.cards import STANDARDDECK, cards_to_vector, suits_to_vector, NUM2CARD
import random
import numpy as np


class ml_agent(Agent):
    def __init__(self, neural_network, tensorflow_session, deck=STANDARDDECK, exploration_factor=1):
        Agent.__init__(self, deck)
        self.neural_network = neural_network
        self.tensorflow_session = tensorflow_session
        self.name = "Learned AI"
        self.eps = exploration_factor

    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)

        state = self.get_state(table, player_id)

        random_checker = np.random.rand()
        if self.eps > random_checker:
            card = options[random.randrange(0, len(options))]
        else:
            choice = np.argmin(self.tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: state}))
            card = NUM2CARD(choice)
        return card

    def get_state(self, table, player_id):
        hands_vector = cards_to_vector(table.hands[player_id])
        table_vector = cards_to_vector(table.cards[player_id])
        discard_vector = cards_to_vector(table.combined_discardpile)
        first_suit_vector = suits_to_vector(table.first_suit)
        return hands_vector+table_vector+discard_vector+first_suit_vector
