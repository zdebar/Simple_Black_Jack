from enum import Enum, auto


# Deck Settings
COLOR = ("♥", "♦", "♣", "♠")
RANK = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K')
VALUE_DICT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10,
              "Q": 10, "K": 10}

# Game settings
DEALER_DRAW_NUMBER = 17
GAME_GOAL_NUMBER = 21
ALTERNATIVE_ACE_VALUE = 11
ACE_ADDITION = ALTERNATIVE_ACE_VALUE - VALUE_DICT["A"]


class GameResult(Enum):
    PLAYER_LOSS = auto()
    DRAW = auto()
    PLAYER_WIN = auto()