import random
import logging
from typing import List, Dict
from functools import partial
from enum import Enum, auto
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

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


def input_yn(question: str) -> bool:
    while True:
        user_input = input(question).strip().lower()
        if user_input == "y":
            logging.debug(f"Input yn == True")
            return True
        if user_input == "n":
            logging.debug(f"Input yn == False")
            return False
        print("\nInvalid input! Please enter 'y' or 'n'!")


class GameResult(Enum):
    PLAYER_LOSS = auto()
    DRAW = auto()
    PLAYER_WIN = auto()


@dataclass(frozen=True)
class Card:
    suit: str
    rank: str

    def __str__(self) -> str:
        return f"{self.rank:>2} of {self.suit}"


def calculate_hand_value(hand: list[Card], value_dict: dict[str, int]) -> int:
    total_value = sum(VALUE_DICT[card.rank] for card in hand)
    num_aces = sum(value_dict["A"] for card in hand if card.rank == "A")

    for _ in range(num_aces):
        if total_value + ACE_ADDITION <= GAME_GOAL_NUMBER:
            total_value += ACE_ADDITION

    logging.debug(f"{Player}'s hand value calculated: {total_value}")
    return total_value


calculate_hand_value_with_default_dict = partial(calculate_hand_value, value_dict=VALUE_DICT)


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


class GameController:
    def __init__(self) -> None:
        self.player = HumanPlayer("Player")
        self.dealer = ComputerPlayer("Dealer")
        self.deck = Deck()
        self.game_on = True

    def run_game(self):
        self.deal_initial_cards()
        self.draw_card_turn(self.player)
        self.draw_card_turn(self.dealer)
        self.determine_winner()

    def deal_initial_cards(self) -> None:
        for _ in range(2):
            self.player.hand.append(self.deck.draw_card())
        self.player.hand_value = calculate_hand_value_with_default_dict(self.player.hand)
        self.perform_draw_card_sequence(self.dealer)

    def draw_card_turn(self, member) -> None:
        while self.game_on and member.want_card():
            member.print_card_drawn()
            self.perform_draw_card_sequence(member)

    def determine_winner(self) -> None:
        if self.game_on:
            if self.player.hand_value > self.dealer.hand_value:
                print("\nYou win!")
            elif self.player.hand_value < self.dealer.hand_value:
                print("\nDealer wins!")
            else:
                print("\nIt's a draw!")

    def perform_draw_card_sequence(self, member) -> None:
        member.hand.append(self.deck.draw_card())
        member.hand_value = calculate_hand_value_with_default_dict(member.hand)
        # print(f"{member.name} draws a card {member.hand[-1]}")
        self.present_cards()
        self.check_game_status()

    def present_cards(self) -> None:
        print(self.player)
        print(self.dealer)

    def check_game_status(self) -> None:
        if self.player.hand_value > GAME_GOAL_NUMBER:
            self.game_result(GameResult.PLAYER_LOSS)
        elif self.dealer.hand_value > GAME_GOAL_NUMBER:
            self.game_result(GameResult.PLAYER_WIN)

    def game_result(self, result: GameResult) -> None:
        result_messages = {
            GameResult.PLAYER_LOSS: "\nYou lost!",
            GameResult.DRAW: "\nIt's a draw!",
            GameResult.PLAYER_WIN: "\nYou won!",
        }
        print(result_messages.get(result, "\nInvalid result!"))
        self.game_on = False


class GameControllerFactory:
    @staticmethod
    def create_game_controller() -> 'GameController':
        return GameController()


if __name__ == "__main__":
    while input_yn("\nDo you want to play game of BlackJack? (y/n): "):
        logging.debug(f"New game started.")
        game = GameControllerFactory.create_game_controller()
        game.run_game()

    print("\nThanks for playing! Have a great day!")
