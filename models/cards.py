class Card:
    def __init__(self, suit, rank, compare_suit=True):
        self.suit = suit
        self.rank = rank
        self.compare_suit = compare_suit

    def ascii_str(self):
        return str(self.rank) + self.suit.ascii_str()

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Card):
            return self.rank < other.rank or (self.compare_suit and self.rank == other.rank and self.suit < other.suit)
        else:
            return self.rank < other

    def __le__(self, other):
        if isinstance(other, Card):
            if self.compare_suit:
                return self.rank < other.rank or self.rank == other.rank and self.suit <= other.suit
            else:
                return self.rank <= other.rank
        else:
            return self.rank <= other

    def __gt__(self, other):
        if isinstance(other, Card):
            return self.rank > other.rank or (self.compare_suit and self.rank == other.rank and self.suit > other.suit)
        else:
            return self.rank > other

    def __ge__(self, other):
        if isinstance(other, Card):
            if self.compare_suit:
                return self.rank > other.rank or self.rank == other.rank and self.suit >= other.suit
            else:
                return self.rank >= other.rank
        else:
            return self.rank >= other

    @staticmethod
    def szudzik(a, b):
        return a * a + a + b if a >= b else a + b * b

    def __hash__(self):
        return self.szudzik(self.suit, self.rank)
