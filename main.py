# main.py
from controllers.game_controller import GameControllerFactory
from utils.input_utils import input_yn
from config.logging_config import *
import logging

if __name__ == "__main__":
    logging.debug("Starting Blackjack game.")

    while input_yn("\nDo you want to play game of BlackJack? (y/n): "):
        logging.debug(f"New game started.")
        game_controller = GameControllerFactory.create_game_controller()
        game_controller.run_game()

    print("\nThanks for playing! Have a great day!")
