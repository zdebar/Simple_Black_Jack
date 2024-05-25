from models.player import HumanPlayer, ComputerPlayer, Player
from models.deck import Deck
from utils.hand_value_calculator import calculate_hand_value_with_default_dict
from config.config import *


class GameController:
    def __init__(self, player_class: Player, dealer_class: Player, deck_class: Deck) -> None:
        self.player = player_class
        self.dealer = dealer_class
        self.deck = deck_class
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
                self.game_result(GameResult.PLAYER_WIN)
            elif self.player.hand_value < self.dealer.hand_value:
                self.game_result(GameResult.PLAYER_LOSS)
            else:
                self.game_result(GameResult.DRAW.value)

    def perform_draw_card_sequence(self, member) -> None:
        member.hand.append(self.deck.draw_card())
        member.hand_value = calculate_hand_value_with_default_dict(member.hand)
        self.present_cards()
        self.check_overreach()

    def present_cards(self) -> None:
        print(self.player)
        print(self.dealer)

    def check_overreach(self) -> None:
        if self.player.hand_value > GAME_GOAL_NUMBER:
            self.game_result(GameResult.PLAYER_LOSS)
        elif self.dealer.hand_value > GAME_GOAL_NUMBER:
            self.game_result(GameResult.PLAYER_WIN)

    def game_result(self, result: GameResult) -> None:
        print(result.value)
        self.game_on = False


class GameControllerFactory:
    @staticmethod
    def create_game_controller(player_class: Player = HumanPlayer("Player"),
                               dealer_class: Player = ComputerPlayer("Computer"),
                               deck_class: Deck = Deck()) -> 'GameController':
        return GameController(player_class, dealer_class, deck_class)
