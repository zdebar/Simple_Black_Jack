from models.card import Card
from models.player import HumanPlayer, ComputerPlayer, Player
from models.deck import Deck
from ui.ui_terminal import GameView
from utils.hand_value_calculator import calculate_hand_value_with_default_dict
from config.config import GameSettings, GameResult
from typing import Type, Optional


class GameController:
    def __init__(self, player: Player, dealer: Player, deck: Deck, view: GameView) -> None:
        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.view = view
        self.game_on = True

    def run_game(self) -> None:
        self.deal_initial_cards()
        self.draw_card_turn(self.player, self.view.ask_player_wants_card)
        self.draw_card_turn(self.dealer)
        self.determine_winner()

    def deal_initial_cards(self) -> None:
        for _ in range(2):
            self.player.hand.append(self.deck.draw_card())
        self.player.hand_value = calculate_hand_value_with_default_dict(self.player.hand)
        card = self.draw_card()
        self.perform_draw_card_sequence(self.dealer, card)

    def draw_card_turn(self, member: Player, want_card_fn=None) -> None:
        while self.game_on and (want_card_fn(member) if want_card_fn else member.want_card()):
            card = self.draw_card()
            self.view.print_card_drawn(member, card)
            self.perform_draw_card_sequence(member, card)

    def determine_winner(self) -> None:
        if self.game_on:
            if self.player.hand_value > self.dealer.hand_value:
                self.view.print_game_result(GameResult.PLAYER_WIN)
            elif self.player.hand_value < self.dealer.hand_value:
                self.view.print_game_result(GameResult.PLAYER_LOSS)
            else:
                self.view.print_game_result(GameResult.DRAW)

    def draw_card(self) -> Card:
        return self.deck.draw_card()

    def perform_draw_card_sequence(self, member, card) -> None:
        member.hand.append(card)
        member.hand_value = calculate_hand_value_with_default_dict(member.hand)
        self.view.present_cards(self.player, self.dealer)
        self.check_overreach()

    def check_overreach(self) -> None:
        player_bust = self.player.hand_value > GameSettings.GAME_GOAL_NUMBER.value
        dealer_bust = self.dealer.hand_value > GameSettings.GAME_GOAL_NUMBER.value

        if player_bust:
            self.view.print_game_result(GameResult.PLAYER_LOSS)
            self.game_on = False
        elif dealer_bust:
            self.view.print_game_result(GameResult.PLAYER_WIN)
            self.game_on = False


class GameControllerFactory:
    @staticmethod
    def create_game_controller(player_class: Optional[Type[Player]] = None,
                               dealer_class: Optional[Type[Player]] = None,
                               deck_class: Optional[Type[Deck]] = None,
                               view_class: Optional[Type[GameView]] = None) -> GameController:
        if player_class is None:
            player_class = HumanPlayer
        if dealer_class is None:
            dealer_class = ComputerPlayer
        if deck_class is None:
            deck_class = Deck
        if view_class is None:
            view_class = GameView

        player = player_class("Player")
        dealer = dealer_class("Dealer")
        deck = deck_class()
        view = view_class()

        return GameController(player, dealer, deck, view)
