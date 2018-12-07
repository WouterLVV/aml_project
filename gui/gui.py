from tkinter import *
from logic.game import Hearts
from logic.cards import STANDARDDECK,Card,Deck
from PIL import Image,ImageTk


class GuiCard(Card):
    def __init__(self, suit, rank, compare_suit=False):
        Card.__init__(self,suit,rank,compare_suit)
        self.img = Image.open("gui/assets/cards")

class HeartsSpectator(Frame,Hearts):

    def __init__(self, players, deck=STANDARDDECK, master=None):
        Frame.__init__(self,master)
        Hearts.__init__(self,players,deck)

        self.master = master

    def init_window(self):
        self.master.title("Hearts")

