from models.suits import Suit


class Trick:
    def __init__(self, players, first_player_id, broken):
        self.first_player_id = first_player_id
        self.broken = broken
        self.players = players
        self.attempted_cards = [None]*len(players)
        self.cards = [None]*len(players)
        self.num = len(players)
        self.first_suit = Suit.NONE
        self.hands = [None]*self.num
        self.discardpiles = [None]*self.num
        self.scores = [None]*self.num
        self.rewards = [None]*self.num
        self.combined_discardpile = []

        for i in range(self.num):
            self.hands[i] = self.players[i].hand[:]
            self.discardpiles[i] = self.players[i].played[:]
            self.scores[i] = self.players[i].points
            self.combined_discardpile += self.discardpiles[i]

    def play(self):
        for i in range(self.num):
            player_id = (i + self.first_player_id) % self.num
            card, attempted_card = self.players[player_id].make_move(self, player_id)
            self.attempted_cards[player_id] = attempted_card
            self.cards[player_id] = card
            if self.first_suit is Suit.NONE:
                self.first_suit = card.suit
            self.broken |= card.suit == Suit.HEARTS
        assert self.first_suit is not None and not Suit.NONE

    def finish(self):
        highestcard = -1
        for i in range(self.num):
            if self.cards[i].suit == self.first_suit and self.cards[i] > highestcard:
                winner = i
                highestcard = self.cards[i]
        self.players[winner].win_cards(self.cards[:])
        for i in range(self.num):
            self.rewards[i] = self.players[i].points-self.scores[i]
        return winner


class BasicTrick:
    def __init__(self, players, first_player_id):
        self.first_player_id = first_player_id
        self.players = players
        self.first_suit = Suit.NONE

        self.number_of_players = len(players)
        self.hands = [None]*self.number_of_players
        self.discardpiles = [None]*self.number_of_players
        self.scores = [None]*self.number_of_players
        self.rewards = [None]*self.number_of_players
        self.attempted_cards = [None]*self.number_of_players
        self.played_cards = [None]*self.number_of_players
        self.combined_discardpile = []

        for i in range(self.number_of_players):
            self.hands[i] = self.players[i].hand[:]
            self.discardpiles[i] = self.players[i].played[:]
            self.scores[i] = self.players[i].points
            self.combined_discardpile += self.discardpiles[i]

    def play(self):
        for i in range(self.number_of_players):
            player_id = (i + self.first_player_id) % self.number_of_players
            card, attempted_card = self.players[player_id].make_move(self, player_id)
            self.attempted_cards[player_id] = attempted_card
            self.played_cards[player_id] = card
            if self.first_suit is Suit.NONE:
                self.first_suit = card.suit
        assert self.first_suit is not None and not Suit.NONE

    def finish(self):
        highestcard = -1
        for i, card in enumerate(self.played_cards):
            if card.suit == self.first_suit and card > highestcard:
                winner = i
                highestcard = card
        self.players[winner].win_cards(self.played_cards[:])
        for i in range(self.number_of_players):
            self.rewards[i] = self.players[i].points-self.scores[i]
        return winner


