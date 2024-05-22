import random
from enum import Enum
from dataclasses import dataclass, field


COLOR = ("♥", "♦", "♣", "♠")
RANK = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K')
VALUE_DICT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10,
              "Q": 10, "K": 10}


# ze shoe do ruky hráče a další prvky
def add_card(self, card) -> None:
    self.hand.append(card)
    self.calculate_value()


def present_cards(self):
    print(self.player)
    print(self.dealer)


def game_round(self) -> None:
    self.deal_cards()
    self.player_turn()
    self.computer_turn()
    self.compare_values()


def draw_evaluate_present(self, pl) -> None:
    self.draw_card(pl)
    self.present_cards()
    self.evaluate_hand(pl)


def deal_cards(self) -> None:
    for _ in range(2):
        self.draw_card(self.player)
    self.draw_evaluate_present(self.dealer)


def player_turn(self) -> None:
    while self.is_game_running and self.check_input_yn("\nDo you want another card? (y/n): "):
        self.draw_evaluate_present(self.player)


def computer_turn(self) -> None:
    while self.is_game_running and self.dealer.value < 17:
        input("\nDealer draws a card! Press Enter to continue!")
        self.draw_evaluate_present(self.dealer)


def compare_values(self) -> None:
    if self.is_game_running:
        if self.player.value == self.dealer.value:
            self.game_result(GameResult.DRAW)
        elif self.player.value > self.dealer.value:
            self.game_result(GameResult.PLAYER_WIN)
        else:
            self.game_result(GameResult.PLAYER_LOSS)


def game_result(self, result: GameResult) -> None:
    result_messages = {
        GameResult.PLAYER_LOSS: "\nYou lost!",
        GameResult.DRAW: "\nDraw!",
        GameResult.PLAYER_WIN: "\nYou won!",
    }
    print(result_messages.get(result, "\nInvalid result!"))
    self.is_game_running = False


def check_input_yn(question: str) -> bool:
    """
        Asks the user y/n question. Returns their response. Handles invalid input.
        :param question: Question for player.
        :return: True for "y", False for "n".
    """
    while True:
        user_input = input(question).strip().lower()
        if user_input == "y":
            return True
        if user_input == "n":
            return False
        print("\nInvalid input! Please enter 'y' or 'n'!")


class GameResult(Enum):
    PLAYER_LOSS = "player_loss"
    DRAW = "draw"
    PLAYER_WIN = "player_win"


@dataclass(frozen=True)
class Card:
    suit: str
    rank: str

    def __str__(self) -> str:
        return f"{self.rank:>2} of {self.suit}"


@dataclass
class Player:
    name: str
    hand: list = field(default_factory=list)
    value: int = 0

    def __str__(self) -> str:
        return f"\n{self.name}'s hand".ljust(18) + " | " + " | ".join(str(card) for card in self.hand) + " | " \
            + f"\nValue: {self.value}"

    def calculate_value(self) -> None:
        total_value = sum(VALUE_DICT[card.rank] for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.rank == "A")

        for _ in range(num_aces):
            total_value += 10 if total_value <= 11 else 0

        self.value = total_value

    def evaluate_hand(self, pl) -> None:
        pl.calculate_value()
        if self.player.value > 21 or self.dealer.value == 21:
            self.game_result(GameResult.PLAYER_LOSS)
        elif self.dealer.value > 21 or self.player.value == 21:
            self.game_result(GameResult.PLAYER_WIN)

@dataclass
class BlackJack:
    def __init__(self) -> None:
        self.player, self.dealer = Player("Player"), Player("Dealer")
        self.is_game_running = True
        self.shoe = []

    def add_deck_to_shoe(self) -> None:
        deck = [Card(c, v) for c in COLOR for v in RANK]
        random.shuffle(deck)
        self.shoe.extend(deck)


if __name__ == "__main__":
    game = BlackJack()
    game_round()
    while check_input_yn("\nDo you want to play again? (y/n): "):
        game.__init__()
        game_round()
    else:
        print("\nIt was nice playing with you. Have a nice day.")

class GameMechanics:
