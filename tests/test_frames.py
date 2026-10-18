from bowling_game.frames import Frames


def test_number_starts_at_one():
    assert Frames().number == 1


def test_number_advances_after_two_rolls():
    frames = Frames()
    frames.add_roll(3)
    assert frames.number == 1
    frames.add_roll(4)
    assert frames.number == 2


def test_number_caps_at_ten():
    frames = Frames()
    for _ in range(20):
        frames.add_roll(0)
    assert frames.number == 10
    frames.add_roll(0)
    assert frames.number == 10


def test_score_includes_tenth_frame_bonus_roll():
    frames = Frames()
    for _ in range(18):
        frames.add_roll(0)
    for pins in (5, 5, 3):
        frames.add_roll(pins)
    assert frames.score() == 13


def test_score_includes_two_tenth_frame_bonus_rolls():
    frames = Frames()
    for _ in range(18):
        frames.add_roll(0)
    for pins in (10, 3, 4):
        frames.add_roll(pins)
    assert frames.score() == 17
