from logic.cards import Card,Rank,Suit

all_cards = [Card(s,r) for s in Suit for r in Rank]

def print_cards():
    for card in all_cards:
        print(card)

def test_comparisons():
    assert Card(Suit.CLUBS, Rank.FIVE) == Card(Suit.CLUBS, Rank.FIVE)
    assert Card(Suit.CLUBS, Rank.FIVE) != Card(Suit.CLUBS, Rank.FOUR)
    assert Card(Suit.HEARTS, Rank.FIVE) != Card(Suit.CLUBS, Rank.FIVE)

    assert not Card(Suit.SPADES, Rank.EIGHT, compare_suit=False) > Card(Suit.CLUBS, Rank.EIGHT, compare_suit=False)
    assert Card(Suit.SPADES, Rank.EIGHT, compare_suit=True) > Card(Suit.CLUBS, Rank.EIGHT, compare_suit=True)
    assert Card(Suit.SPADES, Rank.EIGHT, compare_suit=True) > Card(Suit.CLUBS, Rank.EIGHT, compare_suit=False)
    assert not Card(Suit.SPADES, Rank.EIGHT, compare_suit=False) > Card(Suit.CLUBS, Rank.EIGHT, compare_suit=True)
    assert not Card(Suit.SPADES, Rank.EIGHT, compare_suit=True) <= Card(Suit.CLUBS, Rank.EIGHT, compare_suit=True)
    assert Card(Suit.SPADES, Rank.EIGHT, compare_suit=False) <= Card(Suit.CLUBS, Rank.EIGHT, compare_suit=False)

    assert not Card(Suit.CLUBS, Rank.EIGHT, compare_suit=False) < Card(Suit.SPADES, Rank.EIGHT, compare_suit=False)
    assert Card(Suit.CLUBS, Rank.EIGHT, compare_suit=True) < Card(Suit.SPADES, Rank.EIGHT, compare_suit=True)
    assert Card(Suit.CLUBS, Rank.EIGHT, compare_suit=True) < Card(Suit.SPADES, Rank.EIGHT, compare_suit=False)
    assert not Card(Suit.CLUBS, Rank.EIGHT, compare_suit=False) < Card(Suit.SPADES, Rank.EIGHT, compare_suit=True)


def test_hashes():
    for index1, card1 in enumerate(all_cards):
        for index2, card2 in enumerate(all_cards):
            if index1 == index2:
                assert card1 == card2
                assert hash(card1) == hash(card2)
            else:
                assert card1 != card2
                assert hash(card1) != hash(card2)


def run_tests():
    print_cards()
    test_comparisons()
    test_hashes()

run_tests()