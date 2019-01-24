from logic.agent import Agent
from logic.cards import STANDARDDECK, cards_to_vector, suits_to_vector, NUM2CARD
import random
import numpy as np
import tensorflow as tf


class ml_agent(Agent):
    def __init__(self, neural_network, tensorflow_session, deck=STANDARDDECK, games_played=0, decay_rate=1):
        Agent.__init__(self, deck)
        self.neural_network = neural_network
        self.name = "Learned AI"
        self.games_played = games_played
        self.decay_rate = decay_rate
        self.tensorflow_session = tensorflow_session

    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)

        state = self.get_state(table, player_id)

        random_checker = np.random.rand()
        if self.get_exploration_rate() > random_checker:
            #print("Picking random card")
            card = options[random.randrange(0, len(options))]
        else:
            choices = np.array(self.tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: [state]}))
            choice = np.argmin((choices+1000)*np.array([np.inf if x == 0 else 1 for x in cards_to_vector(self.hand)]))
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
        self.__init__(deck=deck,
                      neural_network=self.neural_network,
                      games_played=self.games_played,
                      decay_rate=self.decay_rate,
                      tensorflow_session=self.tensorflow_session)


