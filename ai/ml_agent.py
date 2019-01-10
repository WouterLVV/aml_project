from logic.agent import Agent
from logic.cards import STANDARDDECK


class ml_agent(Agent):

    def __init__(self, deck=STANDARDDECK):
        Agent.__init__(self, deck)
        self.name = "Learned AI"

