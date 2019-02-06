import numpy as np


class DataTransformer:
    def __init__(self, number_of_suits, number_of_cards, deck):
        self.number_of_suits = number_of_suits
        self.number_of_cards = number_of_cards
        self.deck = deck
        self.CARD2NUM = dict([(b, a) for a, b in enumerate(deck.cardlist)])
        self.NUM2CARD = dict([(a, b) for a, b in enumerate(deck.cardlist)])

    def suits_to_vector(self, suits, include_suit_NONE=True):
        if include_suit_NONE:
            vector = np.zeros((self.number_of_suits+1,), dtype=np.bool)
        else:
            vector = np.zeros((self.number_of_suits,), dtype=np.bool)
        for suit in suits:
            vector[suit.value] = 1
        return vector

    def cards_to_vector(self, cards):
        vector = np.zeros((self.number_of_cards,), dtype=np.bool)
        for i in cards:
            if i is None:
                continue
            vector[self.CARD2NUM[i]] = 1
        return vector

    def vector_to_cards(self, vector):
        cards = []
        for i, v in enumerate(vector):
            if v == 1:
                cards.append(self.NUM2CARD[i])
        return cards
