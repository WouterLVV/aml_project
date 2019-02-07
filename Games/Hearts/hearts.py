import tensorflow as tf

from models.cards import Card
from models.data_transformer import DataTransformer
from models.deck import Deck
from models.game import Game
from models.neural_network import KerasNetwork
from models.ranks import Rank
from models.simulator import KerasSimulator
from models.suits import Suit
from models.agent import *

HEARTSDECK = Deck.gen_default()
QUEENOFSPADES = Card(Suit.SPADES, Rank.QUEEN)
TWOOFCLUBS = Card(Suit.CLUBS, Rank.TWO)
HEARTSDATATRANSFORMER = DataTransformer(number_of_suits=4, number_of_cards=52, deck=HEARTSDECK)


class Hearts(Game):
    def __init__(self):
        super(Hearts, self).__init__()


if __name__ == "__main__":
    load_previously_saved_models = True

    with tf.Session() as tensorflow_session:
        if not load_previously_saved_models:
            hearts_networks = [
                KerasNetwork(
                    state_size=57,
                    action_size=52,
                    output_activation_function='linear',
                    discount_factor=0
                ),
                KerasNetwork(
                    state_size=57,
                    action_size=52,
                    hidden_sizes=[52],
                    hidden_activation_functions=['selu'],
                    output_activation_function='linear',
                    discount_factor=0
                ),
                KerasNetwork(
                    state_size=57,
                    action_size=52,
                    hidden_sizes=[52],
                    hidden_activation_functions=['elu'],
                    output_activation_function='linear',
                    discount_factor=0
                ),
                KerasNetwork(
                    state_size=57,
                    action_size=52,
                    hidden_sizes=[52],
                    hidden_activation_functions=['linear'],
                    output_activation_function='linear',
                    discount_factor=0
                )
            ]
            variable_initializer = tf.global_variables_initializer()
            tensorflow_session.run(variable_initializer)
        else:
            hearts_networks = [
                KerasNetwork(model="networks/hearts1.h5py", discount_factor=0),
                KerasNetwork(model="networks/hearts2.h5py", discount_factor=0),
                KerasNetwork(model="networks/hearts3.h5py", discount_factor=0),
                KerasNetwork(model="networks/hearts4.h5py", discount_factor=0)
            ]
        players = [KerasAgent(deck=HEARTSDECK,
                              datatransformer_klass=HEARTSDATATRANSFORMER,
                              neural_network=network,
                              name="Player {}".format(i)) for i, network in enumerate(hearts_networks)]
        hearts_simulator = KerasSimulator(
            players=players,
            number_of_games_per_cycle=1,
            number_of_update_cycles=1,
            neural_network=hearts_networks[0],
            future_reward_factor=0,
            tensorflow_session=tensorflow_session,
            data_transformer=HEARTSDATATRANSFORMER,
            deck=HEARTSDECK
        )
        hearts_simulator.run_cycles()
        hearts_simulator.plot_losses()
        hearts_simulator.plot_epoch_scores()
        # hearts_networks[0].save("networks/hearts1.h5py")
        # hearts_networks[1].save("networks/hearts2.h5py")
        # hearts_networks[2].save("networks/hearts3.h5py")
        # hearts_networks[3].save("networks/hearts4.h5py")

