import random as rn
import os

""""
    Simple BlackJack Game

    The game deals cards first to the player ("Player") as long as the player wants cards, then to the 
    computer ("Dealer") as long as the hand's value is less than 17. After every card is dealt, it checks for both 
    overreach (value > 21) and blackjack (value == 21). If the game ends prematurely, it prints the result and sets 
    is_game_running to False, which enables skipping the rest of the game code. If card dealing finishes without a 
    premature game end, the values of both hands are compared, and the winner is determined.
"""


def check_input_yn(question: str) -> bool:
    """
        Asks the user y/n question. Returns their response. Handles invalid input.
        :param question: Question for player.
        :return: True for "y", False for "n".
    """
    while True:
        user_input = input(f"{question}").lower()
        if user_input == "y":
            return True
        if user_input == "n":
            return False
        print("\nInvalid input! Please enter 'y' or 'n'!")

class Card:
    def __init__(self, suit: str, rank: str) -> None:
        """
            Initializes a Card object with the given suit and rank.
        """
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        """
            :return: The string representation of the card.
        """
        return f"{' ' if len(self.rank) == 1 else ''}{self.rank:.2} of {self.suit}"


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
        self.value = 0

    def __str__(self) -> str:
        """
            Returns string representation of player's hand and it's value.
        """
        output = f"\n{self.name}'s hand".ljust(18) + " | "
        for card in self.hand:
            output += f"{card} | "
        output += f"\nValue: {self.value}"
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
        total_value, num_aces = 0, 0

        for card in self.hand:
            match card.rank:
                case "J" | "Q" | "K":
                    total_value += 10
                case "A":
                    total_value += 1
                    num_aces += 1
                case _:
                    total_value += int(card.rank)

        while num_aces:
            total_value += 10 if total_value <= 11 else 0
            num_aces -= 1

        self.value = total_value


class Game:
    def __init__(self) -> None:
        """
            Starts a new game of BlackJack
        """
        self.player, self.dealer = Player("Player"), Player("Dealer")
        self.is_game_running = True
        self.create_deck()
        self.deal_cards()
        self.player_turn()
        self.computer_turn()
        self.compare_values()

    def create_deck(self) -> None:
        """
            Create list of 52 Card object, assigns it to self.deck() and shuffles it.
        """
        color = ("♥", "♦", "♣", "♠")
        value = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K']
        self.deck = [Card(c, v) for c in color for v in value]
        rn.shuffle(self.deck)

    def draw_card(self, pl) -> None:
        """
            Draws a card from the deck and adds it to the specified player's hand.
            :param pl: Player to whom the card should be added.
        """
        pl.add_card(self.deck.pop())

    def draw_card_and_evaluate(self, pl) -> None:
        """
           Draws a card from the deck and adds it to the specified player's hand.
           Prints both player's and computer's hands.
           Evaluates both hands for overreach and BlackJack.
           :param pl: Player to whom the card should be added.
        """
        pl.add_card(self.deck.pop())

        print(self.player)
        print(self.dealer)

        if self.player.value > 21 or self.dealer.value == 21:
            self.game_result(-1)
        elif self.dealer.value > 21 or self.player.value == 21:
            self.game_result(1)

    def game_result(self, w) -> None:
        """
            Prints the result based on outcome.
            :param w: -1 for player's loss, 0 for draw, 1 for player's win
        """
        result_messages = {
            -1: "\nYou lost!",
            0: "\nDraw!",
            1: "\nYou won!",
        }
        print(result_messages.get(w, "\nInvalid result!"))
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
        while self.is_game_running and check_input_yn("\nDo you want another card? (y/n): "):
            self.draw_card_and_evaluate(self.player)

    def computer_turn(self) -> None:
        """
            The computer draws cards until its hand value is 17 or higher.
        """
        while self.is_game_running and self.dealer.value < 17:
            print("\nDealer draws card!")
            self.draw_card_and_evaluate(self.dealer)
            input("\nPress Enter to continue!")

    def compare_values(self) -> None:
        """
            Compares player's and computer's hand's values and determines game result.
        """
        if self.is_game_running:
            if self.player.value == self.dealer.value:
                self.game_result(0)
            elif self.player.value > self.dealer.value:
                self.game_result(1)
            else:
                self.game_result(-1)


if __name__ == "__main__":
    while check_input_yn("\nDo you want to play? (y/n): "):
        new_game = Game()
    else:
        print("\nIt was nice playing with you. Have a nice day.")
