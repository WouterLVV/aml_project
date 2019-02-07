class Game:
    def __init__(self, players, deck):
        self.players = players
        self.winners = None
        self.losers = None
        self.scores = [0]*len(players)

    def play_round(self):
        pass

    def finished(self):
        pass

    def play(self):
        while not self.finished():
            self.play_round()
        self.get_scoreboard()
        self.declare_winners()
        self.declare_losers()

    def get_scoreboard(self):
        pass

    def declare_winners(self):
        pass

    def declare_losers(self):
        pass

    def is_valid_move(self):
        pass

    def get_trick_reward(self, trick):
        pass
