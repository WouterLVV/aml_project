from logic.game import Hearts
from logic.agent import HumanPlayer,RandomAI
from logic.cards import STANDARDDECK, Deck
import random
import time

def one_human_three_random():
    players = [RandomAI(STANDARDDECK) for i in range(3)]
    players.append(HumanPlayer(STANDARDDECK, ask_name=True))
    random.shuffle(players)
    game = Hearts(players)
    for i in range(13):
        game.play_round(verbose=True)
    game.finish(verbose=True)

def four_random():
    players = [RandomAI(STANDARDDECK) for i in range(4)]
    game = Hearts(players)
    for i in range(13):
        game.play_round(verbose=True)
    game.finish(verbose=True)

def many_games():
    for i in range(1000):
        deck = Deck.gen_default()
        players = [RandomAI(deck) for i in range(4)]
        game = Hearts(players, deck=deck)
        for i in range(13):
            game.play_round(verbose=False)
        game.finish(verbose=False)

starttime = time.perf_counter_ns()
many_games()
endtime = time.perf_counter_ns()
print((endtime-starttime)/1000000000)

# four_random()
