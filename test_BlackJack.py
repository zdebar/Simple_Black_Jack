from BlackJack import Player, Card


class TestPlayer:
    def test_calculate_hand_value(self):
        player = Player("Test_Player")
        player.hand = [Card("♥", "A"), Card("♦", "A"),
                       Card("♣", "A"), Card("♠", "A"), Card("♥", "J")]
        player.calculate_hand_value()
        assert player.value == 14
