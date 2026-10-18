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


def test_strike_scores_next_two_rolls_as_bonus():
    game = Game()
    for pins in (10, 3, 4):
        game.roll(pins)
    assert game.score() == 24


def test_tenth_frame_spare_counts_bonus_roll():
    game = Game()
    for _ in range(18):
        game.roll(0)
    for pins in (5, 5, 3):
        game.roll(pins)
    assert game.score() == 13
    assert game.frame_number == 10


def test_tenth_frame_strike_counts_two_bonus_rolls():
    game = Game()
    for _ in range(18):
        game.roll(0)
    for pins in (10, 3, 4):
        game.roll(pins)
    assert game.score() == 17
    assert game.frame_number == 10


def test_perfect_game_scores_three_hundred():
    game = Game()
    for _ in range(12):
        game.roll(10)
    assert game.score() == 300
    assert game.frame_number == 10


def test_all_spares_scores_one_fifty():
    game = Game()
    for _ in range(21):
        game.roll(5)
    assert game.score() == 150
    assert game.frame_number == 10
