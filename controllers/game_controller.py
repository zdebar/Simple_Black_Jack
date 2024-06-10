from models.card import Card
from models.player import HumanPlayer, ComputerPlayer, Player
from models.deck import Deck
from utils.hand_value_calculator import calculate_hand_value_with_default_dict
from config.config import GameSettings, GameResult
from typing import Type, Optional


class GameController:
    def __init__(self, player_class: Player, dealer_class: Player, deck_class: Deck) -> None:
        self.player = player_class
        self.dealer = dealer_class
        self.deck = deck_class
        self.game_on = True

    def run_game(self) -> None:
        self.deal_initial_cards()
        self.draw_card_turn(self.player)
        self.draw_card_turn(self.dealer)
        self.determine_winner()

    def deal_initial_cards(self) -> None:
        for _ in range(2):
            self.player.hand.append(self.deck.draw_card())
        self.player.hand_value = calculate_hand_value_with_default_dict(self.player.hand)
        card = self.draw_card()
        self.perform_draw_card_sequence(self.dealer, card)

    def draw_card_turn(self, member) -> None:
        while self.game_on and member.want_card():
            card = self.draw_card()
            member.print_card_drawn(card)
            self.perform_draw_card_sequence(member, card)

    def determine_winner(self) -> None:
        if self.game_on:
            if self.player.hand_value > self.dealer.hand_value:
                self.print_game_result(GameResult.PLAYER_WIN.value)
            elif self.player.hand_value < self.dealer.hand_value:
                self.print_game_result(GameResult.PLAYER_LOSS.value)
            else:
                self.print_game_result(GameResult.DRAW.value)

    def draw_card(self) -> Card:
        return self.deck.draw_card()

    def perform_draw_card_sequence(self, member, card) -> None:
        member.hand.append(card)
        member.hand_value = calculate_hand_value_with_default_dict(member.hand)
        self.present_cards()
        self.check_overreach()

    def present_cards(self) -> None:
        print(self.player)
        print(self.dealer)

    def check_overreach(self) -> None:
        player_bust = self.player.hand_value > GameSettings.GAME_GOAL_NUMBER.value
        dealer_bust = self.dealer.hand_value > GameSettings.GAME_GOAL_NUMBER.value

        if player_bust:
            self.print_game_result(GameResult.PLAYER_LOSS)
        elif dealer_bust:
            self.print_game_result(GameResult.PLAYER_WIN)

    def print_game_result(self, result: GameResult) -> None:
        print(result.value)
        self.game_on = False


class GameControllerFactory:
    @staticmethod
    def create_game_controller(player_class: Optional[Type[Player]] = None,
                               dealer_class: Optional[Type[Player]] = None,
                               deck_class: Optional[Type[Deck]] = None) -> GameController:
        if player_class is None:
            player_class = HumanPlayer("Player")
        if dealer_class is None:
            dealer_class = ComputerPlayer("Computer")
        if deck_class is None:
            deck_class = Deck()

        return GameController(player_class, dealer_class, deck_class)
