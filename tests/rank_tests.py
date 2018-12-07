from logic.cards import Rank

def print_ranks():
    for r in Rank:
        print(r)

def test_comparison():
    assert Rank.DRAGON == Rank(16)
    assert Rank(4) == Rank.FOUR
    assert Rank.ACE > 3

def run_tests():
    print_ranks()
    test_comparison()

run_tests()