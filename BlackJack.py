import random
import logging
from enum import Enum, auto
from dataclasses import dataclass

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
            return True
        if user_input == "n":
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


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = []
        self.hand_value = 0

    def __str__(self) -> str:
        return f"\n{self.name}'s hand".ljust(18) + " | " + " | ".join(str(card) for card in self.hand) + " | " + \
               f"\nValue: {self.hand_value}"

    def calculate_hand_value(self) -> None:
        total_value = sum(VALUE_DICT[card.rank] for card in self.hand)
        num_aces = sum(VALUE_DICT["A"] for card in self.hand if card.rank == "A")

        for _ in range(num_aces):
            if total_value + ACE_ADDITION <= GAME_GOAL_NUMBER:
                total_value += ACE_ADDITION

        self.hand_value = total_value
        logging.debug(f"{self.name}'s hand value calculated: {self.hand_value}")


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
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.deck = Deck()
        self.game_on = True

    def run_game(self):
        self.deal_initial_cards()
        self.player_turn()
        self.dealer_turn()
        self.determine_winner()

    def deal_initial_cards(self) -> None:
        for _ in range(2):
            self.player.hand.append(self.deck.draw_card())
        self.player.calculate_hand_value()
        self.perform_draw_block(self.dealer)

    def player_turn(self) -> None:
        while self.game_on and input_yn("\nDo you want another card? (y/n): "):
            self.perform_draw_block(self.player)

    def dealer_turn(self) -> None:
        while self.game_on and self.dealer.hand_value < DEALER_DRAW_NUMBER:
            input("\nDealer draws a card! Press Enter to continue!")
            self.perform_draw_block(self.dealer)

    def determine_winner(self) -> None:
        if self.game_on:
            if self.player.hand_value > self.dealer.hand_value:
                print("\nYou win!")
            elif self.player.hand_value < self.dealer.hand_value:
                print("\nDealer wins!")
            else:
                print("\nIt's a draw!")

    def perform_draw_block(self, member) -> None:
        member.hand.append(self.deck.draw_card())
        member.calculate_hand_value()
        self.present_cards()
        self.check_game_status()

    def present_cards(self) -> None:
        print(self.player)
        print(self.dealer)

    def check_game_status(self) -> None:
        if self.player.hand_value > GAME_GOAL_NUMBER or self.dealer.hand_value == GAME_GOAL_NUMBER:
            self.game_result(GameResult.PLAYER_LOSS)
        elif self.dealer.hand_value > GAME_GOAL_NUMBER or self.player.hand_value == GAME_GOAL_NUMBER:
            self.game_result(GameResult.PLAYER_WIN)

    def game_result(self, result: GameResult) -> None:
        result_messages = {
            GameResult.PLAYER_LOSS: "\nYou lost!",
            GameResult.DRAW: "\nIt's a draw!",
            GameResult.PLAYER_WIN: "\nYou won!",
        }
        print(result_messages.get(result, "\nInvalid result!"))
        self.game_on = False


if __name__ == "__main__":
    while input("\nDo you want to play game of BlackJack? (y/n): "):
        game_controller = GameController()
        game_controller.run_game()

    print("\nThanks for playing! Have a great day!")
