import random
from models.card import Card
from config.config import *


class Deck:
    def __init__(self) -> None:
        self.cards = []

    def create_deck(self) -> None:
        self.cards = [Card(c, v) for c in COLOR for v in RANK]
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        if not self.cards:
            self.create_deck()
        return self.cards.pop()
