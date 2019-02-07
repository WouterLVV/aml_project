from models.round import Round
from Games.Hearts.hearts import HEARTSDECK
from Games.Hearts.trick import HeartsTrick


class Hearts2(Round):
    def __init__(self, players):
        super(Hearts2, self).__init__(players, deck=HEARTSDECK, trick_klass=HeartsTrick)
        self.broken = False

    def play_trick(self, verbose=False, **kwargs):
        trick = super(Hearts2, self).play_trick(verbose=verbose, **kwargs)
        self.broken = trick.broken


