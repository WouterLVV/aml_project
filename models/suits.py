from enum import IntEnum


class Suit(IntEnum):
    NONE = 0
    DIAMOND = 1
    CLUBS = 2
    HEARTS = 3
    SPADES = 4
    RED = 5
    GREEN = 6
    BLUE = 7
    BLACK = 8

    def __str__(self):
        return {
            0: "",
            1: "\u2666",
            2: "\u2663",
            3: "\u2665",
            4: "\u2660",
            5: "RED",
            6: "GREEN",
            7: "BLUE",
            8: "BLACK",
        }[self.value]

    def ascii_str(self):
        return {
            0: "",
            1: "D",
            2: "C",
            3: "H",
            4: "S",
            5: "R",
            6: "G",
            7: "B",
            8: "K",
        }[self.value]
