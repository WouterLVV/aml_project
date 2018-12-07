from logic.game import Hearts
from logic.agent import HumanPlayer,RandomAI
from logic.cards import STANDARDDECK
import random

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

one_human_three_random()