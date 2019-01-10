from enum import IntEnum


def szudzik(a, b):
    return a * a + a + b if a >= b else a + b * b


class Suit(IntEnum):
    NONE = 0
    DIAMOND = 1
    CLUBS = 2
    HEARTS = 3
    SPADES = 4
    RED = 5
    GREEN = 6
    BLUE = 7
    BLACK = 8

    def __str__(self):
        return {
            0: "",
            1: "\u2666",
            2: "\u2663",
            3: "\u2665",
            4: "\u2660",
            5: "RED",
            6: "GREEN",
            7: "BLUE",
            8: "BLACK",
        }[self.value]

    def ascii_str(self):
        return {
            0: "",
            1: "D",
            2: "C",
            3: "H",
            4: "S",
            5: "R",
            6: "G",
            7: "B",
            8: "K",
        }[self.value]


class Rank(IntEnum):
    DOG = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    CHICKEN = 15
    DRAGON = 16

    def __str__(self):
        return {
            0: "DOG",
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K",
            14: "A",
            15: "CHICKEN",
            16: "DRAGON"
        }[self.value]


class DuplicateCardError(Exception):
    pass


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
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit

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

    def __hash__(self):
        return szudzik(self.suit, self.rank)


QUEENOFSPADES = Card(Suit.SPADES, Rank.QUEEN)
TWOOFCLUBS = Card(Suit.CLUBS, Rank.TWO)

class Deck:

    def __init__(self, cardlist, allow_duplicates=False):
        self.allow_duplicates = allow_duplicates
        self.cardlist = cardlist
        self.cardmap = dict()
        self.suits = set()
        self.ranks = set()
        for card in cardlist:
            value = self.cardmap.setdefault(card, 0)
            self.cardmap[card] = value + 1
            self.suits.add(card.suit)
            self.ranks.add(card.rank)

    def __len__(self):
        return len(self.cardlist)

    def __contains__(self, item):
        return self.cardmap.get(item, 0) > 0

    def shuffle(self):
        import random
        random.shuffle(self.cardlist)

    def take_one(self, index=0):
        card = self.cardlist.pop(index)
        self.cardmap[card] -= 1
        return card

    def take(self, amount=1):
        return [self.take_one() for _ in range(amount)]

    def put_multiple(self, cards, position=-1):
        if position < 0:
            position = len(self.cardlist)
        for card in reversed(cards):
            self.put(card, position)

    def put(self, card, position=-1):
        value = self.cardmap.setdefault(card, 0)
        if not self.allow_duplicates and value > 0:
            raise DuplicateCardError
        self.cardmap[card] = value + 1
        self.suits.add(card.suit)
        self.ranks.add(card.rank)
        if position < 0:
            position = len(self.cardlist)
        self.cardlist.insert(position, card)

    def deal(self, hands=4, cards=-1, shuffled=True, equal_size=True, destructive=True):
        if (shuffled):
            self.shuffle()

        if cards <= 0:
            cards = len(self.cardlist) / hands

        if (equal_size):
            cards = int(cards)

        handlist = [self.cardlist[int(i * cards):int((i + 1) * cards)] for i in range(hands)]
        restlist = self.cardlist[cards * hands:]

        for hand in handlist:
            for card in hand:
                self.cardmap[card] -= 1

        if destructive:
            self.cardlist = restlist

        return handlist

    @staticmethod
    def gen_default(min_suit=1, max_suit=4, min_rank=2, max_rank=14, card_class=Card, allow_duplicates=False):
        max_suit += 1
        max_rank += 1

        return Deck([card_class(Suit(a), Rank(b)) for a in range(min_suit, max_suit) for b in range(min_rank, max_rank)],
                    allow_duplicates=allow_duplicates)

    @staticmethod
    def gen_tichu():
        deck = Deck([Card(Suit(a), Rank(b), compare_suit=True) for a in range(5, 9) for b in range(2, 15)], allow_duplicates=False)
        deck.put(Card(Suit.NONE, Rank.ONE))
        deck.put(Card(Suit.NONE, Rank.DOG))
        deck.put(Card(Suit.NONE, Rank.CHICKEN))
        deck.put(Card(Suit.NONE, Rank.DRAGON))
        return deck


STANDARDDECK = Deck.gen_default()
CARD2NUM = dict([(b,a) for a,b in enumerate(STANDARDDECK.cardlist)])
NUM2CARD = dict([(a,b) for a,b in enumerate(STANDARDDECK.cardlist)])
TICHUDECK = Deck.gen_tichu()
