import pytest

from utils.hand_value_calculator import calculate_hand_value_with_default_dict
from models.card import Card


class Test:
    def test_4_aces(self):
        test_list = [Card("♥", "A"), Card("♦", "A"), Card("♣", "A"), Card("♠", "A"), Card("♥", "J")]
        assert calculate_hand_value_with_default_dict(test_list) == 14

    def test_empty_list(self):
        assert calculate_hand_value_with_default_dict([]) == 0

    def test_invalid_card(self):
        test_list = [Card("♥", "X"), Card("♦", "A"), Card("♣", "A"), Card("♠", "A"), Card("♥", "J")]
        with pytest.raises(KeyError):
            calculate_hand_value_with_default_dict(test_list)
