import random
import numpy as np

from models.suits import Suit
from Games.Hearts.hearts import HEARTSDECK, QUEENOFSPADES, TWOOFCLUBS
from models.deck import STANDARDDECK
from models.data_transformer import STANDARDDATATRANSFORMER


class Agent:
    def __init__(self, deck=HEARTSDECK):
        self.hand = []
        self.cardset = set()
        self.deck = deck
        self.played = []
        self.points = 0
        self.won_cards = []
        self.suit_counter = dict()
        self.name = "Ultimate AI"
        self.have_two_of_clubs = False
        self.QoS_worth = len(deck)//len(deck.suits)
        for s in deck.suits:
            self.suit_counter[s] = 0

    def __str__(self):
        return self.name

    def reset(self):
        self.__init__()

    def receive_hand(self, cards):
        self.hand = cards
        for card in cards:
            self.suit_counter[card.suit] += 1
            self.cardset.add(card)
            self.have_two_of_clubs |= card == TWOOFCLUBS

    def receive_card(self, card):
        self.hand.append(card)

    def win_cards(self, cards):
        self.won_cards.extend(cards)
        self.update_score()

    def update_score(self):
        for card in self.won_cards:
            if card.suit == Suit.HEARTS:
                self.points += 1
            if card == QUEENOFSPADES:
                self.points += self.QoS_worth

    def make_move(self, table, player_id):
        attempted_card = None
        card = self.pick_card(table, player_id)
        if not self.check_valid(card, table):
            if card in self.hand:
                self.points += 150
            else:
                self.points += 500
            options = self.determine_valid_options(table)
            attempted_card = card
            card = options[random.randrange(0, len(options))]
        self.hand.remove(card)
        self.suit_counter[card.suit] -= 1
        self.cardset.remove(card)
        self.played.append(card)
        if card == TWOOFCLUBS:
            self.have_two_of_clubs = False
        if attempted_card is None:
            return card, card
        else:
            return card, attempted_card

    def pick_card(self, table, player_id):
        print("Method needs to be overridden")
        pass

    def check_valid(self, card, table):
        valid = True
        valid &= card in self.cardset
        if table.first_suit is not Suit.NONE:
            valid &= (card.suit == table.first_suit if self.suit_counter[table.first_suit] > 0 else True)
        # if self.suit_counter[Suit.HEARTS] < len(self.hand) and not table.broken and table.first_suit == Suit.NONE:
        #     valid &= card.suit != Suit.HEARTS
        if len(self.hand) == 13:
            valid &= self.have_two_of_clubs == (card == TWOOFCLUBS)
        return valid

    def determine_valid_options(self, table):
        valid_options = []
        for i in self.hand:
            if self.check_valid(i, table):
                valid_options.append(i)
        return valid_options

    def end_game(self):
        return self.points


class HumanPlayer(Agent):
    def __init__(self, deck=HEARTSDECK, ask_name=False):
        super(HumanPlayer, self).__init__(deck)
        if ask_name:
            self.name = input("Your Name: ")
        else:
            self.name = "Henk" + str(random.randrange(0, 1000))

    def receive_hand(self, cards):
        cards.sort()
        super(HumanPlayer, self).receive_hand(cards)

    def pick_card(self, table, player_id):
        print("\n-------------------------\n")
        print("Current table: ")
        print("\n".join(["{}: {}".format(table.players[i].name, table.cards[i]) for i in range(len(table.players))]))
        print()
        print("Player that started round: " + table.players[table.first_player_id].name)
        print("Requested Suit: " + str(table.first_suit))
        print("Your hand: " + ", ".join(["{}: {}".format(i, card) for i, card in enumerate(self.hand)]))
        s = input(self.name + ", Choose card to play: ")
        card = self.hand[int(s)]
        return card

    def end_game(self):
        score = super(HumanPlayer, self).end_game()
        print("{}, you scored {} points!".format(self.name, score))
        return score


class BasicAgent:
    def __init__(self, deck, name="Ultimate AI"):
        self.name = name
        self.hand = []
        self.played = []
        self.points = 0
        self.won_cards = []
        self.suit_counter = dict()
        for s in deck.suits:
            self.suit_counter[s] = 0

    def __str__(self):
        return self.name

    def reset(self, deck):
        self.__init__(deck, name=self.name)

    def receive_hand(self, cards):
        self.hand = cards
        for card in cards:
            self.suit_counter[card.suit] += 1

    def receive_card(self, card):
        self.hand.append(card)

    def win_cards(self, cards):
        self.won_cards.extend(cards)
        self.update_score()

    def update_score(self):
        pass

    def make_move(self, table, player_id):
        card, attempted_card = None, None
        return card, attempted_card

    def pick_card(self, table, player_id):
        pass


class RandomDeckAI(Agent):
    def __init__(self, deck=STANDARDDECK):
        super(RandomDeckAI, self).__init__(deck)
        self.name = "RandomDeckAI#" + str(random.randrange(0, 1000))

    def pick_card(self, table, player_id):
        card = self.deck.cardlist[random.randrange(0, self.deck.__len__())]
        return card


class RandomHandAI(Agent):
    def __init__(self, deck=STANDARDDECK):
        super(RandomHandAI, self).__init__(deck)
        self.name = "RandomDeckAI#" + str(random.randrange(0, 1000))

    def pick_card(self, table, player_id):
        card = self.hand[random.randrange(0, len(self.hand))]
        return card


class RandomValidAI(Agent):
    def __init__(self, deck=STANDARDDECK):
        super(RandomValidAI, self).__init__(deck)
        self.name = "RandomDeckAI#" + str(random.randrange(0, 1000))

    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)
        card = options[random.randrange(0, len(options))]
        return card


class NeuralNetworkAgent(Agent):
    def __init__(self, name, neural_network, deck=STANDARDDECK, datatransformer_klass=STANDARDDATATRANSFORMER,
                 games_played=0, decay_rate=1):
        super(NeuralNetworkAgent, self).__init__(deck)
        self.name = name
        self.neural_network = neural_network
        self.games_played = games_played
        self.decay_rate = decay_rate
        self.datatransformer_klass = datatransformer_klass

    def pick_card(self, table, player_id):
        options = self.determine_valid_options(table)

        random_checker = np.random.rand() + 100
        if self.get_exploration_rate() > random_checker:
            card = options[random.randrange(0, len(options))]
        else:
            state = self.get_state(table, player_id)
            actions = self.calculate_actions(state)
            best_action = self.best_action(actions=actions)
            card = self.datatransformer_klass.NUM2CARD[best_action]
        return card

    def get_state(self, table, player_id):
        hands_vector = self.datatransformer_klass.cards_to_vector(table.hands[player_id])
        table_vector = self.datatransformer_klass.cards_to_vector(table.cards)
        discard_vector = self.datatransformer_klass.cards_to_vector(table.combined_discardpile)
        first_suit_vector = self.datatransformer_klass.suits_to_vector([table.first_suit])
        return hands_vector

    def calculate_actions(self, state):
        pass

    def best_action(self, actions):
        pass

    def get_exploration_rate(self):
        return np.exp(-self.decay_rate * self.games_played)

    def end_game(self):
        self.games_played += 1
        return super(NeuralNetworkAgent, self).end_game()

    def reset(self):
        self.__init__(name=self.name,
                      deck=self.deck,
                      neural_network=self.neural_network,
                      games_played=self.games_played,
                      decay_rate=self.decay_rate)


class TensorFlowAgent(NeuralNetworkAgent):
    def __init__(self, neural_network, tensorflow_session, deck=STANDARDDECK,
                 datatransformer_klass=STANDARDDATATRANSFORMER, games_played=0,
                 name="TensorFlow AI #" + str(random.randrange(0, 1000)), decay_rate=1):
        super(TensorFlowAgent, self).__init__(neural_network=neural_network,
                                              deck=deck,
                                              games_played=games_played,
                                              decay_rate=decay_rate,
                                              name=name,
                                              datatransformer_klass=datatransformer_klass)
        self.tensorflow_session = tensorflow_session

    def calculate_actions(self, state):
        return np.array(
            self.tensorflow_session.run(self.neural_network.output, feed_dict={self.neural_network.inputs_: [state]}))

    def reset(self):
        self.__init__(deck=self.deck,
                      neural_network=self.neural_network,
                      games_played=self.games_played,
                      decay_rate=self.decay_rate,
                      tensorflow_session=self.tensorflow_session)


class KerasAgent(NeuralNetworkAgent):
    def __init__(self, neural_network, deck=STANDARDDECK, decay_rate=1,
                 datatransformer_klass=STANDARDDATATRANSFORMER, games_played=0,
                 name="Keras AI #" + str(random.randrange(0, 1000))):
        super(KerasAgent, self).__init__(neural_network=neural_network,
                                         deck=deck,
                                         games_played=games_played,
                                         decay_rate=decay_rate,
                                         name=name,
                                         datatransformer_klass=datatransformer_klass)

    def calculate_actions(self, state):
        return self.neural_network.model.predict(state.reshape((1, 52)), batch_size=1)
