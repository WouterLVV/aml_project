from logic.cards import STANDARDDECK, Suit, Rank, Card, Deck, TWOOFCLUBS


class Hearts:
    def __init__(self, players, deck=STANDARDDECK):
        self.players = players
        self.deck = deck
        self.history = []
        self.broken = False
        self.scores = [None]*4
        num_players = len(players)

        hands = deck.deal(num_players, destructive=False)
        for i, cards in enumerate(hands):
            self.players[i].receive_hand(cards)
            if TWOOFCLUBS in cards:
                self.first_player = i

    def play_round(self, verbose=False):
        round_ = Round(self.players, self.first_player, self.broken)
        round_.play()
        self.first_player = round_.finish()
        self.history.append(round_)
        self.broken = round_.broken
        if verbose:
            print("Starting player: " + str(round_.players[round_.first_player_id]) + ". -- Cards played: " + ", ".join(["{}: {}".format(round_.players[i].name, round_.cards[i]) for i in range(len(round_.players))]))
        return round_

    def finish(self, verbose=False):
        for i, player in enumerate(self.players):
            self.scores[i] = player.end_game()
            if verbose:
                print("{} got {} points!".format(player.name, self.scores[i]))
            player.reset(deck=self.deck)

    def play_game(self):
        num_rounds = len(self.deck) // len(self.players)
        for i in range(num_rounds):
            self.play_round()
        self.finish()
        return self


class Round:
    def __init__(self, players, first_player_id, broken):
        self.first_player_id = first_player_id
        self.broken = broken
        self.players = players
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
            card = self.players[player_id].make_move(self, player_id)
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
