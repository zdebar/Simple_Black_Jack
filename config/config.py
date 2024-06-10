from enum import Enum


class DeckSettings(Enum):
    COLOR = ("♥", "♦", "♣", "♠")
    RANK = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K')
    VALUE_DICT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10,
                  "Q": 10, "K": 10}
    ACE_ADDITION = 10


class GameSettings(Enum):
    DEALER_DRAW_NUMBER = 17
    GAME_GOAL_NUMBER = 21


class GameResult(Enum):
    PLAYER_LOSS = "\nYou lost!"
    DRAW = "\nIt's a draw!"
    PLAYER_WIN = "\nYou won!"

