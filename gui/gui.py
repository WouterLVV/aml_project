from tkinter import *

from logic.agent import RandomAI
from logic.game import Hearts
from logic.cards import Card,Deck
from PIL import Image,ImageTk

import math
import time
import json


class GuiCard(Card):
    def __init__(self, suit, rank, compare_suit=False):
        Card.__init__(self,suit,rank,compare_suit)
        self.img = Image.open("assets/cards/{}.png".format(self.ascii_str()))


STANDARDGUIDECK = Deck.gen_default(min_suit=1, max_suit=4, min_rank=2, max_rank=14, card_class=GuiCard,
                                   allow_duplicates=False)


class HeartsSpectator(Frame,Hearts):

    class HeartsSettings:

        def __init__(self, master=None, game=None, filepath="hearts.conf"):
            self.parent = game
            self.options = {}
            self.filename = filepath

            menubar = Menu(master)
            viewmenu = Menu(menubar, tearoff=0)

            anim_toggle = BooleanVar()
            anim_toggle.set(True)
            self.options['animate'] = anim_toggle
            viewmenu.add_checkbutton(label="animations", variable=anim_toggle, command=self.changed)

            cardsize = DoubleVar()
            cardsize.set(.4)
            self.options['cardsize'] = cardsize
            cardsizemenu = Menu(viewmenu, tearoff=0)
            cardsizemenu.add_radiobutton(label="mini", variable=cardsize, value=0.1,
                                         command=self.changed)
            cardsizemenu.add_radiobutton(label="small", variable=cardsize, value=0.2,
                                         command=self.changed)
            cardsizemenu.add_radiobutton(label="normal", variable=cardsize, value=0.4,
                                         command=self.changed)
            cardsizemenu.add_radiobutton(label="big", variable=cardsize, value=0.7,
                                         command=self.changed)
            cardsizemenu.add_radiobutton(label="huge", variable=cardsize, value=0.9,
                                         command=self.changed)
            viewmenu.add_cascade(label="card size", menu=cardsizemenu)

            menubar.add_cascade(label="View", menu=viewmenu)

            self.load_config()
            self.save_config()
            self.changed()

            master.config(menu=menubar)

        def load_config(self):
            try:
                with open(self.filename, 'r') as conffile:
                    d = json.load(conffile)
                    for k,v in d.items():
                        self.options[k].set(v)
            except FileNotFoundError:
                with open(self.filename, 'w') as conffile:
                    json.dump({}, conffile)

        def save_config(self):
            with open(self.filename, 'w') as conffile:
                d = {}
                for k,v in self.options.items():
                    d[k] = v.get()
                json.dump(d, conffile)

        def changed(self):
            for k,v in self.options.items():
                self.parent.__dict__[k] = v.get()
            self.save_config()

    def __init__(self, players, deck=STANDARDGUIDECK, master=None):
        Frame.__init__(self,master)
        Hearts.__init__(self,players,deck)

        self.master = master

        # Dummy values that are overwritten when the program starts
        self.cardsize = 0.
        self.animate = True
        self.animation_duration = 0.5
        self.last_round = None

        self.init_window()

    def play_round(self, verbose=True):
        round_ = Hearts.play_round(self, verbose)
        self.visualize_round(round_)

    def visualize_round(self, round):
        if self.last_round is not None:
            for player in self.last_round.players:
                player.card_img.destroy()

        num_players = len(round.players)
        dist = math.tau/num_players
        for i in range(num_players):
            i = (i + round.first_player_id) % num_players

            image = round.cards[i].img
            width,height = image.size

            image = image.resize((int(width * self.cardsize), int(height * self.cardsize)), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(image)

            img = Label(self, image=render, text=round.players[i].name)
            img.image = render

            round.players[i].card_img = img

            place_scale = 0.4

            # ----------------------------

            handsize = len(round.hands[i])

            # ----------------------------

            x = ((math.sin(dist*i)+1)/2)*place_scale + (1-place_scale)/2
            y = ((math.cos(dist*i)+1)/2)*place_scale + (1-place_scale)/2

            if (self.animate):
                starttime = time.perf_counter()
                time_elapsed = 0.
                relx = 0.5 - x
                rely = 0.5 - y
                while (time_elapsed < self.animation_duration):
                    time_elapsed = time.perf_counter() - starttime
                    offset = 1-(time_elapsed/self.animation_duration)
                    img.place(relx=x-relx*offset, rely=y-rely*offset, anchor=CENTER)
                    self.update()

            img.place(relx=x, rely=y, anchor=CENTER)

        self.last_round = round

    def init_window(self):
        self.master.title("Hearts")

        self.create_menu()

        self.pack(fill=BOTH, expand=1)

        play_button = Button(self,text="Play a Round!", command=self.play_round)
        play_button.place(relx=0.5, rely=0.99, anchor=S)

    def create_menu(self):
        self.settings = HeartsSpectator.HeartsSettings(self.master, self)


def four_random():
    players = [RandomAI(STANDARDGUIDECK) for i in range(4)]
    root = Tk()
    root.geometry("1920x1080")
    game = HeartsSpectator(players, master=root)
    root.mainloop()


four_random()
