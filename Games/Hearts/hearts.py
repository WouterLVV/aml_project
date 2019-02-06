import tensorflow as tf

from models.cards import Card
from models.data_transformer import DataTransformer
from models.deck import Deck
from models.game import Game
from models.neural_network import KerasNetwork
from models.ranks import Rank
from models.simulator import KerasSimulator
from models.suits import Suit
from Games.Hearts.agents import *

HEARTSDECK = Deck.gen_default()
QUEENOFSPADES = Card(Suit.SPADES, Rank.QUEEN)
TWOOFCLUBS = Card(Suit.CLUBS, Rank.TWO)
HEARTSDATATRANSFORMER = DataTransformer(number_of_suits=4, number_of_cards=52, deck=HEARTSDECK)


class Hearts(Game):
    def __init__(self):
        super(Hearts, self).__init__()


if __name__ == "__main__":
    with tf.Session() as tensorflow_session:
        hearts_network = KerasNetwork(
            state_size=52,
            action_size=52,
            hidden_sizes=[],
            layer_activation_functions=['lin'],
            learning_rate=0.01
        )
        variable_initializer = tf.global_variables_initializer()
        tensorflow_session.run(variable_initializer)

        players = [
            KerasAgent(deck=HEARTSDECK, neural_network=hearts_network, tensorflow_session=tensorflow_session),
            KerasAgent(deck=HEARTSDECK, neural_network=hearts_network, tensorflow_session=tensorflow_session),
            KerasAgent(deck=HEARTSDECK, neural_network=hearts_network, tensorflow_session=tensorflow_session),
            KerasAgent(deck=HEARTSDECK, neural_network=hearts_network, tensorflow_session=tensorflow_session)
            # YoloAI(),
            # YoloAI(),
            # YoloAI()
        ]
        hearts_simulator = KerasSimulator(
            players=players,
            number_of_games_per_cycle=100,
            number_of_update_cycles=10,
            neural_network=hearts_network,
            future_reward_factor=0,
            tensorflow_session=tensorflow_session,
            data_transformer=HEARTSDATATRANSFORMER,
            deck=HEARTSDECK
        )
        hearts_simulator.run_cycles()
        hearts_simulator.plot_losses()
        hearts_network.save("network.h5py")
