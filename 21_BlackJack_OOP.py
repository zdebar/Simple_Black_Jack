import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{' ' if len(self.rank) == 1 else ''}{self.rank:.2} of {self.suit}"


class Deck:

    def __init__(self):
        color = ("♥", "♦", "♣", "♠")
        value = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K']
        self.cards = [Card(c, v) for c in color for v in value]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.value = 0

    def add_card(self, card):
        self.hand.append(card)
        self.calculate_hand_value()

    def show_hand(self):
        print(f"{self.name}'s hand".ljust(18) + " | ", end="")
        for card in self.hand:
            print(f"{card} | ", end="")
        print(f"\nValue: {self.value}")

    def calculate_hand_value(self):
        total_value, num_aces = 0, 0

        for card in self.hand:
            match card.rank:
                case "J" | "Q" | "K":
                    total_value += 10
                case "A":
                    num_aces += 1
                case _:
                    total_value += int(card.rank)

        while num_aces:
            num_aces -= 1
            if total_value > 10:
                total_value += 1
            else:
                total_value += 11

        self.value = total_value


def ask_input_yn(question):
    while True:
        user_input = input(f"{question}").lower()
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        else:
            print("Invalid input! Please enter 'y' or 'n'!")


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player, self.computer = Player("Player"), Player("Computer")
        self.game_is_on = True
        self.initiate_game()
        self.player_turn()
        self.computer_turn()
        self.end_game()

    def show_game(self):
        self.player.show_hand()
        self.computer.show_hand()

    def test_early_game_end(self):
        if self.player.value > 21 or self.computer.value == 21:
            self.print_result(-1)
        elif self.computer.value > 21 or self.player.value == 21:
            self.print_result(1)

    def print_result(self, w):
        if w == 1:
            print("\nYou won!\n")
        elif w == -1:
            print("\nYou lost!\n")
        else:
            print("\nDraw\n")
        self.game_is_on = False

    def initiate_game(self):
        for _ in 1, 2:
            self.player.add_card(self.deck.draw_card())
        self.computer.add_card(self.deck.draw_card())
        self.show_game()
        self.test_early_game_end()

    def player_turn(self):
        while self.game_is_on and ask_input_yn("\nDo you want another card? (y/n): "):
            self.player.add_card(self.deck.draw_card())
            self.show_game()
            self.test_early_game_end()

    def computer_turn(self):
        while self.computer.value < 17 and self.game_is_on:
            print("\nComputer draws card!")
            self.computer.add_card(self.deck.draw_card())
            self.show_game()
            self.test_early_game_end()
            input("Press any key to continue!")

    def end_game(self):
        if self.game_is_on:
            if self.player.value == self.computer.value:
                self.print_result(0)
            elif self.player.value > self.computer.value:
                self.print_result(1)
            else:
                self.print_result(-1)


while ask_input_yn("Do you want to play? (y/n): "):
    print()
    new_game = Game()
else:
    print("It was nice playing with you. Have a nice day.")

#test option
