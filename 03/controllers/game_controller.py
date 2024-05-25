from models.player import HumanPlayer, ComputerPlayer, Player
from models.deck import Deck
from utils.hand_value_calculator import calculate_hand_value_with_default_dict
from config.config import *


class GameController:
    def __init__(self, player_class: Player, dealer_class: Player, deck_class: Deck) -> None:
        self.player = player_class("Player")
        self.dealer = dealer_class("Dealer")
        self.deck = deck_class()
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
    def create_game_controller(player_class: Player = HumanPlayer, dealer_class: Player = ComputerPlayer,
                               deck_class: Deck = Deck) -> 'GameController':

        return GameController(player_class, dealer_class, deck_class)
