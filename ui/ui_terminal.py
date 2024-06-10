from models.player import Player
from models.card import Card
from config.config import GameResult


class GameView:
    @staticmethod
    def present_cards(player: Player, dealer: Player) -> None:
        print(player)
        print(dealer)

    @staticmethod
    def print_game_result(result: GameResult) -> None:
        print(result.value)

    @staticmethod
    def print_card_drawn(member: Player, card: Card) -> None:
        print(f"\n{member.name} draws card:".ljust(24) + f" | {card} |")

    @staticmethod
    def ask_player_wants_card(player: Player) -> bool:
        return 'y' == input(f"\n{player.name}, do you want another card? (y/n)? ").strip().lower()
