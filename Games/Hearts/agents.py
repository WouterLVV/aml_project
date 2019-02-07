import numpy as np
import random

from models.agent import KerasAgent, TensorFlowAgent
from Games.Hearts.hearts import HEARTSDECK, HEARTSDATATRANSFORMER


class HeartsKerasAgent(KerasAgent):
    def __init__(self, neural_network,
                 name="Keras AI #" + str(random.randrange(0, 1000)),
                 deck=HEARTSDECK, datatransformer_klass=HEARTSDATATRANSFORMER,
                 games_played=0, decay_rate=1):
        super(HeartsKerasAgent, self).__init__(
            name=name,
            neural_network=neural_network,
            deck=deck,
            datatransformer_klass=datatransformer_klass,
            games_played=games_played,
            decay_rate=decay_rate)

    def best_action(self, actions):
        return np.argmin(actions)


class HeartsTensorFlowAgent(TensorFlowAgent):
    def __init__(self, name, neural_network, tensorflow_session, deck=HEARTSDECK,
                 datatransformer_klass=HEARTSDATATRANSFORMER, games_played=0, decay_rate=1):
        super(HeartsTensorFlowAgent, self).__init__(
            name=name,
            neural_network=neural_network,
            deck=deck,
            datatransformer_klass=datatransformer_klass,
            tensorflow_session=tensorflow_session,
            games_played=games_played,
            decay_rate=decay_rate)

    def best_action(self, actions):
        return np.argmin(actions)


