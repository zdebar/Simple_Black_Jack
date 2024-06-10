from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List
from models.card import Card
from config.config import GameSettings


@dataclass
class Player(ABC):
    name: str
    hand: List[Card] = field(default_factory=list)
    hand_value: int = 0

    def __str__(self) -> str:
        return f"\n{self.name}'s hand:".ljust(24) + " | " + " | ".join(str(card) for card in self.hand) + " | " + \
               f"\nValue: {self.hand_value}"

    @abstractmethod
    def want_card(self) -> bool:
        raise NotImplementedError


@dataclass
class HumanPlayer(Player):
    def want_card(self) -> bool:
        return False


@dataclass
class ComputerPlayer(Player):
    def want_card(self) -> bool:
        return self.hand_value < GameSettings.DEALER_DRAW_NUMBER.value

