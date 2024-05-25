from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from models.card import Card
from utils.input_utils import input_yn
from config.config import *


@dataclass
class Player(ABC):
    name: str
    hand: list[Card] = field(default_factory=list)
    hand_value: int = 0

    def __str__(self) -> str:
        return f"\n{self.name}'s hand".ljust(18) + " | " + " | ".join(str(card) for card in self.hand) + " | " + \
               f"\nValue: {self.hand_value}"

    @abstractmethod
    def want_card(self) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def print_card_drawn():
        pass


@dataclass
class HumanPlayer(Player):
    def want_card(self) -> bool:
        return input_yn("\nDo you want another card? (y/n): ")

    def print_card_drawn(self):
        print("\nPlayer draws card!")


@dataclass
class ComputerPlayer(Player):
    def want_card(self) -> bool:
        return self.hand_value < DEALER_DRAW_NUMBER

    def print_card_drawn(self):
        input("\nDealer draws card! Press ENTER to continue! ")
