from tkinter import *

from logic.agent import RandomAI
from logic.game import Hearts
from logic.cards import Card,Deck
from PIL import Image,ImageTk

import math


class GuiCard(Card):
    def __init__(self, suit, rank, compare_suit=False):
        Card.__init__(self,suit,rank,compare_suit)
        self.img = Image.open("assets/cards/{}.png".format(self.ascii_str()))


STANDARDGUIDECK = Deck.gen_default(min_suit=1, max_suit=4, min_rank=2, max_rank=14, card_class=GuiCard,
                                   allow_duplicates=False)


class HeartsSpectator(Frame,Hearts):

    def __init__(self, players, deck=STANDARDGUIDECK, master=None):
        Frame.__init__(self,master)
        Hearts.__init__(self,players,deck)

        self.master = master

        self.init_window()

    def play_round(self, verbose=True):
        round = Hearts.play_round(self,verbose)
        self.visualize_round(round)

    def visualize_round(self, round):
        num_players = len(round.players)
        dist = math.tau/num_players
        for i in range(num_players):
            render = ImageTk.PhotoImage(round.cards[i].img)

            img = Label(self, image=render, text=round.players[i].name)
            img.image = render

            place_scale = 0.4

            x = ((math.sin(dist*i)+1)/2)*place_scale + (1-place_scale)/2
            y = ((math.cos(dist*i)+1)/2)*place_scale + (1-place_scale)/2
            img.place(relx=x, rely=y, anchor=CENTER)


    def init_window(self):
        self.master.title("Hearts")
        self.pack(fill=BOTH, expand=1)

        play_button = Button(self,text="Play a Round!", command=self.play_round)
        play_button.place(relx=0.5, rely=0.99, anchor=S)



def four_random():
    players = [RandomAI(STANDARDGUIDECK) for i in range(4)]
    root = Tk()
    root.geometry("3840x2160")
    game = HeartsSpectator(players, master=root)
    root.mainloop()

four_random()
