from models.trick import BasicTrick
from models.suits import Suit


class HeartsTrick(BasicTrick):
    def __init__(self, players, first_player_id, broken):
        super(HeartsTrick, self).__init__(players=players, first_player_id=first_player_id)
        self.broken = broken

    def play(self):
        super(HeartsTrick, self).play()
        if not self.broken:
            for card in self.played_cards:
                if card.Suit == Suit.HEARTS:
                    self.broken = True
                    break
