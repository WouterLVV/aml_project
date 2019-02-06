from models.suits import Suit
from models.ranks import Rank
from models.cards import Card


class DuplicateCardError(Exception):
    pass


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

    def lowest_of_suit(self, suit):
        lowest = None
        for card in self.cardlist:
            if card.suit == suit and (None == lowest or card < lowest):
                lowest = card
        return lowest


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
TICHUDECK = Deck.gen_tichu()
SMALLDECK = Deck.gen_default(min_suit=2, max_suit=4, min_rank=7, max_rank=14)
