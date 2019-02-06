from models.agent import Agent
from models.deck import STANDARDDECK
from Games.Hearts.hearts import HEARTSDATATRANSFORMER

import numpy as np
import random


class RandomAI(Agent):
    def __init__(self, deck=STANDARDDECK, random_from_deck_instead_of_hand=True):
        super(RandomAI, self).__init__(deck)
        self.name = "RetardedAI#" + str(random.randrange(0,1000))
        self.random_from_deck_instead_of_hand = random_from_deck_instead_of_hand

    def pick_card(self, table, player_id):
        if self.random_from_deck_instead_of_hand:
            card = self.deck.cardlist[random.randrange(0, self.deck.__len__())]
        else:
            card = self.hand[random.randrange(0, len(self.hand))]
        return card

    def reset(self, deck):
        self.__init__(deck=deck,
                      random_from_deck_instead_of_hand=self.random_from_deck_instead_of_hand)


class YoloAI(Agent):
    def __init__(self, deck=STANDARDDECK):
        super(YoloAI, self).__init__(deck)
        self.name = "RetardedAI#" + str(random.randrange(0,1000))

    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)
        card = options[random.randrange(0, len(options))]
        return card


class TensorFlowAgent(Agent):
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

        random_checker = np.random.rand()+100
        if self.get_exploration_rate() > random_checker:
            card = options[random.randrange(0, len(options))]
            print("Picking random card {}".format(card.ascii_str()))
        else:
            ## --------------
            # Get Q values of network for given state
            ## --------------
            choices = np.array(self.tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: [state]}))

            ## --------------
            # select lowest Q value
            ## --------------
            choice = np.argmin(choices)

            ## --------------
            # prefilter on valid actions
            ## --------------
            # choice = np.argmin(choices+np.array([np.inf if x == 0 else 0 for x in cards_to_vector(options)]))
            card = HEARTSDATATRANSFORMER.NUM2CARD[choice]
        return card

    def get_state(self, table, player_id):
        hands_vector = HEARTSDATATRANSFORMER.cards_to_vector(table.hands[player_id])
        table_vector = HEARTSDATATRANSFORMER.cards_to_vector(table.cards)
        discard_vector = HEARTSDATATRANSFORMER.cards_to_vector(table.combined_discardpile)
        first_suit_vector = HEARTSDATATRANSFORMER.suits_to_vector([table.first_suit])

        ## --------------
        # return partial state used for valid card training
        ## --------------
        # return np.concatenate((hands_vector, table_vector, first_suit_vector))

        ## --------------
        # return partial state used for hand card training
        ## --------------
        return hands_vector

        ## --------------
        # return full state used for good card training
        ## --------------
        # return np.concatenate((hands_vector, table_vector, discard_vector, first_suit_vector))

    def get_exploration_rate(self):
        return np.exp(-self.decay_rate*self.games_played)

    def end_game(self):
        score = super(TensorFlowAgent, self).end_game()
        self.games_played += 1
        return score

    def reset(self, deck):
        self.__init__(deck=deck,
                      neural_network=self.neural_network,
                      games_played=self.games_played,
                      decay_rate=self.decay_rate,
                      tensorflow_session=self.tensorflow_session)


class KerasAgent(TensorFlowAgent):
    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)

        state = self.get_state(table, player_id)

        random_checker = np.random.rand()
        if self.get_exploration_rate() > random_checker:
            card = options[random.randrange(0, len(options))]
        else:
            choices = self.neural_network.model.predict(state.reshape((1,52)), batch_size=1)
            choice = np.argmin((choices+1000))
            card = HEARTSDATATRANSFORMER.NUM2CARD[choice]
        return card
