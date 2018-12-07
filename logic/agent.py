from logic.cards import Suit, QUEENOFSPADES, TWOOFCLUBS


class Agent:

    def __init__(self, deck):
        self.hand = []
        self.cardset = set()
        self.played = []
        self.points = 0
        self.won_cards = []
        self.suit_counter = dict()
        self.name = "Ultimate AI"
        self.have_two_of_clubs = False
        for s in deck.suits:
            self.suit_counter[s] = 0

    def __str__(self):
        return self.name

    def receive_hand(self, cards):
        self.hand = cards
        for card in cards:
            self.suit_counter[card.suit] += 1
            self.cardset.add(card)
            self.have_two_of_clubs |= card == TWOOFCLUBS

    def receive_card(self, card):
        self.hand.append(card)

    def win_cards(self,cards):
        self.won_cards.extend(cards)


    def make_move(self, table):
        card = self.pick_card(table)
        assert self.check_valid(card,table)
        self.hand.remove(card)
        self.suit_counter[card.suit] -= 1
        self.cardset.remove(card)
        if card == TWOOFCLUBS:
            self.have_two_of_clubs = False
        return card

    def pick_card(self, table):
        print("Method needs to be overridden")
        pass

    def check_valid(self, card, table):
        valid = True
        valid &= card in self.cardset
        if table.first_suit is not None:
            valid &= (card.suit == table.first_suit if self.suit_counter[table.first_suit] > 0 else True)
        valid &= self.have_two_of_clubs == (card == TWOOFCLUBS)
        return valid

    def end_game(self):
        for card in self.won_cards:
            if card.suit == Suit.HEARTS:
                self.points += 1
            if card == QUEENOFSPADES:
                self.points += 13
        return self.points

import random

class HumanPlayer(Agent):

    def __init__(self, deck, ask_name=False):
        super(HumanPlayer, self).__init__(deck)
        if ask_name:
            self.name = input("Your Name: ")
        else:
            self.name = "Henk" + str(random.randrange(0,1000))


    def pick_card(self, table):
        print("Current table: " + str(["{}: {}".format(table.players[i].name, table.cards[i]) for i in range(len(table.players))]))
        print("Player that started round: " + table.players[table.first_player].name)
        print("Your hand: " + str(["{}: {}".format(i, card) for i,card in enumerate(self.hand)]))
        s = input(self.name + ", Choose card to play: ")
        card = self.hand[int(s)]
        return card

    def end_game(self):
        score = super(HumanPlayer, self).end_game()
        print("{}, you scored {} points!".format(self.name, score))
        return score


class RandomAI(Agent):

    def __init__(self, deck):
        super(RandomAI, self).__init__(deck)
        self.name = "RetardedAI#" + str(random.randrange(0,1000))

    def pick_card(self, table):
        card = self.hand[random.randrange(0,len(self.hand))]
        while not self.check_valid(card, table):
            card = self.hand[random.randrange(0, len(self.hand))]
        return card
