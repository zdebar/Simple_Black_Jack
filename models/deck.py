import random
from typing import List
from models.card import Card
from config.config import DeckSettings


class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = []
        self.create_deck()
        self.shuffle_deck()

    def create_deck(self) -> None:
        self.cards = [Card(color, rank) for color in DeckSettings.COLOR.value for rank in DeckSettings.RANK.value]

    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)

    def is_empty(self) -> bool:
        return not self.cards

    def draw_card(self) -> Card:
        if self.is_empty:
            self.create_deck()
            self.shuffle_deck()
        return self.cards.pop()
