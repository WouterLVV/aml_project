from logic.cards import STANDARDDECK, Suit, Rank, Card, Deck, TWOOFCLUBS


class Hearts:

    def __init__(self, players, deck=STANDARDDECK):
        self.players = players
        self.deck = deck
        self.history = []
        num_players = len(players)

        hands = deck.deal(num_players)
        for i, cards in enumerate(hands):
            self.players[i].receive_hand(cards)
            if TWOOFCLUBS in cards:
                self.first_player = i

    def play_round(self, verbose=False):
        round = Round(self.players, self.first_player)
        round.play()
        self.first_player = round.finish()
        self.history.append(round)
        if verbose:
            print("Starting player: " + str(round.players[round.first_player_id]) + ". -- Cards played: " + str(["{}: {}".format(round.players[i].name, round.cards[i]) for i in range(len(round.players))]))


    def finish(self, verbose=False):
        for player in self.players:
            score = player.end_game()
            if verbose:
                print("{} got {} points!".format(player.name, score))




class Round:
    def __init__(self, players, first_player_id):
        self.first_player_id = first_player_id
        self.players = players
        self.cards = [None]*len(players)
        self.num = len(players)
        self.first_suit = None

    def play(self):
        for i in range(self.num):
            player_id = (i + self.first_player_id) % self.num
            card = self.players[player_id].make_move(self)
            self.cards[player_id] = card
            if self.first_suit is None:
                self.first_suit = card.suit
        assert self.first_suit is not None

    def finish(self):
        highestcard = -1
        for i in range(self.num):
            if self.cards[i].suit == self.first_suit and self.cards[i] > highestcard:
                winner = i
                highestcard = self.cards[i]
        self.players[winner].win_cards(self.cards[:])
        return winner