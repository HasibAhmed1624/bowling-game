import pytest

from bowling_game.game import Game


@pytest.mark.parametrize(("pins", "expected"), [(0, 0), (1, 20)])
def test_roll_same_pins_twenty_times(pins, expected):
    game = Game()
    for _ in range(20):
        game.roll(pins)
    assert game.score() == expected


def test_frame_number_advances_after_two_rolls_or_strike():
    game = Game()
    assert game.frame_number == 1
    game.roll(3)
    assert game.frame_number == 1
    game.roll(4)
    assert game.frame_number == 2
    game.roll(10)
    assert game.frame_number == 3


def test_spare_scores_next_roll_as_bonus():
    game = Game()
    for pins in (5, 5, 3, 4):
        game.roll(pins)
    assert game.score() == 20
