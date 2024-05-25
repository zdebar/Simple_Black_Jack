from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    suit: str
    rank: str

    def __str__(self) -> str:
        return f"{self.rank:>2} of {self.suit}"
