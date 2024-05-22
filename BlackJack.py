import random
from enum import Enum
from dataclasses import dataclass


COLOR = ("♥", "♦", "♣", "♠")
RANK = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K')
VALUE_DICT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10,
              "Q": 10, "K": 10}


def check_input_yn(question: str) -> bool:
    while True:
        user_input = input(question).strip().lower()
        if user_input == "y":
            return True
        if user_input == "n":
            return False
        print("\nInvalid input! Please enter 'y' or 'n'!")


class GameResult(Enum):
    """
        Possible results of game.
    """
    PLAYER_LOSS = "player_loss"
    DRAW = "draw"
    PLAYER_WIN = "player_win"


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
        num_aces = sum(1 for card in self.hand if card.rank == "A")

        for _ in range(num_aces):
            total_value += 10 if total_value <= 11 else 0

        self.hand_value = total_value


class BlackJack:
    def __init__(self) -> None:
        self.player, self.dealer = Player("Player"), Player("Dealer")
        self.shoe = []
        self.is_game_running = True

    def add_deck_to_shoe(self) -> None:
        deck = [Card(c, v) for c in COLOR for v in RANK]
        random.shuffle(deck)
        self.shoe.extend(deck)

    def draw_card(self, pl) -> None:
        if not self.shoe:
            self.add_deck_to_shoe()
        pl.hand.append(self.shoe.pop())
        pl.calculate_hand_value()

    def evaluate_hand(self, pl) -> None:
        pl.calculate_hand_value()
        if self.player.hand_value > 21 or self.dealer.hand_value == 21:
            self.game_result(GameResult.PLAYER_LOSS)
        elif self.dealer.hand_value > 21 or self.player.hand_value == 21:
            self.game_result(GameResult.PLAYER_WIN)

    def present_cards(self):
        print(self.player)
        print(self.dealer)

    def draw_and_present(self, pl) -> None:
        self.draw_card(pl)
        self.present_cards()
        self.evaluate_hand(pl)

    def game_result(self, result: GameResult) -> None:
        result_messages = {
            GameResult.PLAYER_LOSS: "\nYou lost!",
            GameResult.DRAW: "\nDraw!",
            GameResult.PLAYER_WIN: "\nYou won!",
        }
        print(result_messages.get(result, "\nInvalid result!"))
        self.is_game_running = False


if __name__ == "__main__":
    while check_input_yn("\nDo you want to play game of BlackJack? (y/n): "):
        game = BlackJack()

        # deal cards
        for _ in range(2):
            game.draw_card(game.player)
        game.draw_and_present(game.dealer)

        # player turn
        while game.is_game_running and check_input_yn("\nDo you want another card? (y/n): "):
            game.draw_and_present(game.player)

        # computer turn
        while game.is_game_running and game.dealer.hand_value < 17:
            input("\nDealer draws a card! Press Enter to continue!")
            game.draw_and_present(game.dealer)

        # final comparison
        if game.is_game_running:
            if game.player.hand_value == game.dealer.hand_value:
                game.game_result(GameResult.DRAW)
            elif game.player.hand_value > game.dealer.hand_value:
                game.game_result(GameResult.PLAYER_WIN)
            else:
                game.game_result(GameResult.PLAYER_LOSS)

    else:
        print("\nIt was nice playing with you. Have a nice day.")
