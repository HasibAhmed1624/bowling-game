import pytest

from bowling_game.game import Game


@pytest.mark.parametrize(("pins", "expected"), [(0, 0), (1, 20)])
def test_roll_same_pins_twenty_times(pins, expected):
    game = Game()
    for _ in range(20):
        game.roll(pins)
    assert game.score() == expected
