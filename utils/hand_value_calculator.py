# utils/hand_value_calculator.py

from typing import List, Dict
from models.card import Card
from config.config import DeckSettings, GameSettings
import logging
from functools import partial


def calculate_hand_value(hand: List[Card], value_dict: Dict[str, int]) -> int:
    total_value = sum(value_dict[card.rank] for card in hand)
    num_aces = sum(1 for card in hand if card.rank == 'A')

    for _ in range(num_aces):
        if total_value + DeckSettings.ACE_ADDITION.value <= GameSettings.GAME_GOAL_NUMBER.value:
            total_value += DeckSettings.ACE_ADDITION.value

    logging.debug(f"{hand} calculated: {total_value}")
    return total_value


calculate_hand_value_with_default_dict = partial(calculate_hand_value, value_dict=DeckSettings.VALUE_DICT.value)
