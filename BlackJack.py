import random
from enum import Enum


""""
    Simple BlackJack Game

    Game start with dealing two cards to Player, and one to Dealer.
    In Player turn, game deals Player card as long as he wants one.
    In Computer turn, game deals Computer card as long as value of Computer's hand is lower than 17.
    
    After every card dealt, game evaluate premature game end. If value of hand is higher or equal to 21, game prints
    result and set is_game_running to False. With is_game_running == False subsequent game code is skipped.
    
    If there is no premature game end, game compares values of both hands and determines result. 
"""


COLOR = ("♥", "♦", "♣", "♠")
VALUE = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K')
VALUE_DICT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10,
              "Q": 10, "K": 10}


class GameResult(Enum):
    """
        Enum class representing the possible results of a game.
    """
    PLAYER_LOSS = -1
    DRAW = 0
    PLAYER_WIN = 1


class Card:
    def __init__(self, suit: str, rank: str) -> None:
        """
            Initializes a Card object with the given suit and rank.
        """
        self.suit = suit
        self.rank = str(rank)
        self.value = self.calculate_value(rank)
        self.ace = True if rank == "A" else False

    def __str__(self) -> str:
        """
            :return: The string representation of the card.
        """
        return f"{self.rank.rjust(2)} of {self.suit}"

    @staticmethod
    def calculate_value(r) -> int:
        """
            Determines value of card.
        """
        return VALUE_DICT.get(r)


class Player:
    def __init__(self, name: str) -> None:
        """
            Creates Player object with given name.
            :param self.name: Name of player
            :param self.hand: List of Card objects in hand.
            :param self.value: Calculated value of cards.
        """
        self.name = name
        self.hand = []
        self.hand_value = 0

    def __str__(self) -> str:
        """
            Returns string representation of player's hand and it's value.
        """
        output = f"\n{self.name}'s hand".ljust(18) + " | "
        output += " | ".join(str(card) for card in self.hand) + " | "
        output += f"\nValue: {self.hand_value}"
        return output

    def add_card(self, card) -> None:
        """
            Adds card to player hand and calculates new hand value.
            :param card: Adds card to player hand.
        """
        self.hand.append(card)
        self.calculate_hand_value()

    def calculate_hand_value(self) -> None:
        """
            Calculates the total value of the player's hand.
        """
        total_value = sum(card.value for card in self.hand)
        num_aces = sum(card.ace for card in self.hand)

        for _ in range(num_aces):
            total_value += 10 if total_value <= 11 else 0

        self.hand_value = total_value


class BlackJack:
    def __init__(self) -> None:
        """
            Starts a new game of BlackJack
        """
        self.player, self.dealer = Player("Player"), Player("Dealer")
        self.is_game_running = True
        self.shoe = []

    @staticmethod
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

    def add_deck_to_shoe(self) -> None:
        """
        Adds a deck of cards to the shoe.
        """
        deck = [Card(c, v) for c in COLOR for v in VALUE]
        random.shuffle(deck)
        self.shoe.extend(deck)

    def run_game(self) -> None:
        """
            Plays one round of game.
            Asks player to player another round.
            If player agrees, resets the game attributes and starts another round.
            :return: None
        """
        self.game_round()
        while self.check_input_yn("\nDo you want to play again? (y/n): "):
            self.__init__()
            self.game_round()
        else:
            print("\nIt was nice playing with you. Have a nice day.")

    def game_round(self) -> None:
        """
            Runs all phases of a game.
            :return: None
        """
        self.deal_cards()
        self.player_turn()
        self.computer_turn()
        self.compare_values()

    def draw_card(self, pl) -> None:
        """
            Draws a card from the deck and adds it to the specified player's hand.
            :param pl: Player to whom the card should be added.
        """
        if not self.shoe:
            self.add_deck_to_shoe()
        pl.add_card(self.shoe.pop())

    def evaluate_hand(self, pl) -> None:
        """
        Evaluates both hands for overreach and BlackJack. Present cards
        :param pl: Player to evaluate.
        """
        pl.calculate_hand_value()
        if self.player.hand_value > 21 or self.dealer.hand_value == 21:
            self.game_result(GameResult.PLAYER_LOSS)
        elif self.dealer.hand_value > 21 or self.player.hand_value == 21:
            self.game_result(GameResult.PLAYER_WIN)

    def present_cards(self):
        """
        Prints both players hands and their values.
        """
        print(self.player)
        print(self.dealer)

    def draw_card_and_evaluate(self, pl) -> None:
        """
           Combines drawing card, evaluating hand and presenting game.
           :param pl: Player to whom the card should be added.
        """
        self.draw_card(pl)
        self.evaluate_hand(pl)
        self.present_cards()

    def game_result(self, result: GameResult) -> None:
        """
            Prints the result based on outcome.
            :param result: Gamere
        """
        result_messages = {
            GameResult.PLAYER_LOSS: "\nYou lost!",
            GameResult.DRAW: "\nDraw!",
            GameResult.PLAYER_WIN: "\nYou won!",
        }
        print(result_messages.get(result, "\nInvalid result!"))
        self.is_game_running = False

    def deal_cards(self) -> None:
        """
            First round of game.
            Deals 2 card to player, and 1 card for computer.
            Evaluate hands of both players
        """
        for _ in range(2):
            self.draw_card(self.player)
        self.draw_card_and_evaluate(self.dealer)

    def player_turn(self) -> None:
        """
            Prompts the player whether to draw another card.
        """
        while self.is_game_running and self.check_input_yn("\nDo you want another card? (y/n): "):
            self.draw_card_and_evaluate(self.player)

    def computer_turn(self) -> None:
        """
            The computer draws cards until its hand value is 17 or higher.
        """
        while self.is_game_running and self.dealer.hand_value < 17:
            input("\nDealer draws a card! Press Enter to continue!")
            self.draw_card_and_evaluate(self.dealer)

    def compare_values(self) -> None:
        """
            Compares player's and computer's hand's values and determines game result.
        """
        if self.is_game_running:
            if self.player.hand_value == self.dealer.hand_value:
                self.game_result(GameResult.DRAW)
            elif self.player.hand_value > self.dealer.hand_value:
                self.game_result(GameResult.PLAYER_WIN)
            else:
                self.game_result(GameResult.PLAYER_LOSS)


if __name__ == "__main__":
    game = BlackJack()
    game.run_game()
