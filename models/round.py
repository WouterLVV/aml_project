import numpy as np
from models.trick import Trick
from models.deck import STANDARDDECK
from models.suits import Suit


class Hearts:
    def __init__(self, players, deck=STANDARDDECK):
        self.players = players
        self.deck = deck
        self.history = []
        self.broken = False
        self.scores = [None]*4
        num_players = len(players)
        self.lowest_clubs = deck.lowest_of_suit(Suit.CLUBS)

        hands = deck.deal(num_players, destructive=False)
        for i, cards in enumerate(hands):
            self.players[i].receive_hand(cards)
            if self.lowest_clubs in cards:
                self.first_player = i

    def play_trick(self, verbose=False):
        trick = Trick(self.players, self.first_player, self.broken)
        trick.play()
        self.first_player = trick.finish()
        self.history.append(trick)
        self.broken = trick.broken
        if verbose:
            print("Starting player: " + str(trick.players[trick.first_player_id]) + ". -- Cards played: " + ", ".join(["{}: {}".format(trick.players[i].name, trick.cards[i]) for i in range(len(trick.players))]))
        return trick

    def winning_player(self):
        return np.argmin(self.scores)

    def losing_player(self):
        return np.argmax(self.scores)

    def finish(self, verbose=False):
        for i, player in enumerate(self.players):
            self.scores[i] = player.end_game()
            if verbose:
                print("{} got {} points!".format(player.name, self.scores[i]))
            player.reset(deck=self.deck)

    def play_game(self, verbose=False):
        num_tricks = len(self.deck) // len(self.players)
        for i in range(num_tricks):
            self.play_trick(verbose=verbose)
        self.finish(verbose=verbose)
        return self
