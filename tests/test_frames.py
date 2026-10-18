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


def test_perfect_game_scores_three_hundred():
    frames = Frames()
    for _ in range(12):
        frames.add_roll(10)
    assert frames.score() == 300


def test_all_spares_scores_one_fifty():
    frames = Frames()
    for _ in range(21):
        frames.add_roll(5)
    assert frames.score() == 150


def test_score_is_partial_safe_while_strike_awaits_bonus():
    frames = Frames()
    frames.add_roll(10)
    assert frames.score() == 0
    frames.add_roll(10)
    assert frames.score() == 0
    frames.add_roll(10)
    assert frames.score() == 30


def test_score_is_partial_safe_while_spare_awaits_bonus():
    frames = Frames()
    frames.add_roll(5)
    frames.add_roll(5)
    assert frames.score() == 0
    frames.add_roll(3)
    assert frames.score() == 13


def test_rolls_per_frame_exposes_each_frames_rolls():
    frames = Frames()
    for pins in (10, 3, 4):
        frames.add_roll(pins)
    assert frames.rolls_per_frame == [(10,), (3, 4), ()]


def test_frame_scores_show_pending_frames_as_none():
    frames = Frames()
    frames.add_roll(10)
    assert frames.frame_scores() == [None, None]
    frames.add_roll(10)
    assert frames.frame_scores() == [None, None, None]
    frames.add_roll(10)
    assert frames.frame_scores() == [30, None, None, None]


def test_frame_scores_breakdown_for_mixed_game():
    frames = Frames()
    for pins in (10, 3, 4, 5, 5, 2, 3):
        frames.add_roll(pins)
    assert frames.frame_scores() == [17, 7, 12, 5, None]
