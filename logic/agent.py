from logic.cards import Suit, QUEENOFSPADES, TWOOFCLUBS, STANDARDDECK
import random


class Agent:
    def __init__(self, deck=STANDARDDECK):
        self.hand = []
        self.deck = deck
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

    def reset(self, deck):
        self.__init__(deck)

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
        for card in cards:
            if card.suit == Suit.HEARTS:
                self.points += 1
            if card == QUEENOFSPADES:
                self.points += 13

    def make_move(self, table, player_id):
        card = self.pick_card(table, player_id)
        toremove = card
        if not self.check_valid(card, table):
            self.points += 50
        if toremove not in self.cardset:
            self.points += 50
            toremove = self.hand[random.randrange(0,len(self.hand))]
        self.hand.remove(toremove)
        self.suit_counter[toremove.suit] -= 1
        self.cardset.remove(toremove)
        self.played.append(card)
        if toremove == TWOOFCLUBS:
            self.have_two_of_clubs = False
        return card

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
        # # MOVED TO win_cards
        # for card in self.won_cards:
        #     if card.suit == Suit.HEARTS:
        #         self.points += 1
        #     if card == QUEENOFSPADES:
        #         self.points += 13
        return self.points


class HumanPlayer(Agent):
    def __init__(self, deck=STANDARDDECK, ask_name=False):
        super(HumanPlayer, self).__init__(deck)
        if ask_name:
            self.name = input("Your Name: ")
        else:
            self.name = "Henk" + str(random.randrange(0,1000))

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
        print("Your hand: " + ", ".join(["{}: {}".format(i, card) for i,card in enumerate(self.hand)]))
        s = input(self.name + ", Choose card to play: ")
        card = self.hand[int(s)]
        return card

    def end_game(self):
        score = super(HumanPlayer, self).end_game()
        print("{}, you scored {} points!".format(self.name, score))
        return score


class RandomAI(Agent):

    def __init__(self, deck=STANDARDDECK):
        super(RandomAI, self).__init__(deck)
        self.name = "RetardedAI#" + str(random.randrange(0,1000))

    def pick_card(self, table, player_id):
        card = self.hand[random.randrange(0, len(self.hand))]
        while not self.check_valid(card, table):
            card = self.hand[random.randrange(0, len(self.hand))]
        return card


class AnythingGoesAgent(Agent):
    def __init__(self, deck=STANDARDDECK):
        Agent.__init__(self, deck)
        self.name = "RickAstley"

    def pick_card(self, table, player_id):
        pick_valid = random.random() > 0.5
        if pick_valid:
            card = self.hand[random.randrange(0, len(self.hand))]
            while not self.check_valid(card, table):
                card = self.hand[random.randrange(0, len(self.hand))]
            return card
        else:
            return self.deck.cardlist[random.randrange(0,len(self.deck.cardlist))]
