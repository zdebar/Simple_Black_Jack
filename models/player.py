from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List
from models.card import Card
from utils.input_utils import input_yn
from config.config import GameSettings


@dataclass
class Player(ABC):
    name: str
    hand: List[Card] = field(default_factory=list)
    hand_value: int = 0

    def __str__(self) -> str:
        return f"\n{self.name}'s hand".ljust(18) + " | " + " | ".join(str(card) for card in self.hand) + " | " + \
               f"\nValue: {self.hand_value}"

    @abstractmethod
    def want_card(self) -> bool:
        pass

    def print_card_drawn(self, card: Card):
        print(f"\n{self.name} draws card: {card}")


@dataclass
class HumanPlayer(Player):
    def want_card(self) -> bool:
        return input_yn("\nDo you want another card? (y/n): ")


@dataclass
class ComputerPlayer(Player):
    def want_card(self) -> bool:
        return self.hand_value < GameSettings.DEALER_DRAW_NUMBER.value

