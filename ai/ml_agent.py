from logic.agent import Agent
from logic.cards import STANDARDDECK, cards_to_vector, NUM2CARD
import random
import numpy as np
import tensorflow as tf


class ml_agent(Agent):

    def __init__(self, deck=STANDARDDECK, exploration_factor=1):
        Agent.__init__(self, deck)
        self.name = "Learned AI"
        self.eps = exploration_factor


    def pick_card(self, table):
        options = self.determine_valid_options(self.hand, table)
        random_checker=np.random.rand()
        if self.eps>random_checker:
            card = options[random.randrange(0, len(options))]
        else:
            ku_es = np.zeros((52,), dtype=np.bool)
            options_vector = cards_to_vector(options)
            choice = np.argmax(tf.multiply(options_vector, ku_es))
            card = NUM2CARD(choice)
        return card

