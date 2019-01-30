from ai.ml_agent import ml_agent
from logic.agent import Agent
from logic.cards import STANDARDDECK, cards_to_vector, suits_to_vector, NUM2CARD
import random
import numpy as np


class KerasAgent(ml_agent):


    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)

        state = self.get_state(table, player_id)

        random_checker = np.random.rand()
        if self.get_exploration_rate() > random_checker:
            #print("Picking random card")
            card = options[random.randrange(0, len(options))]
        else:
            choices = self.neural_network.model.predict(state.reshape((1,52)), batch_size=1)
            choice = np.argmin((choices+1000))
            card = NUM2CARD[choice]
        return card
