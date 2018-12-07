from logic.cards import Suit

def print_suits():
    for s in Suit:
        print(s)


def test_comparison():
    assert Suit.CLUBS < Suit.SPADES
    assert Suit.DIAMOND == Suit.DIAMOND
    assert Suit(0) == Suit.NONE
    assert Suit(7) == Suit(7)
    assert Suit(2) <= Suit(3)


def run_tests():
    print_suits()
    test_comparison()

run_tests()