from bowling_game.frame import Frame


def test_empty_frame_is_not_complete():
    assert not Frame().is_complete


def test_one_roll_frame_is_not_complete_until_strike():
    frame = Frame()
    frame.add_roll(3)
    assert not frame.is_complete


def test_frame_is_complete_after_two_rolls():
    frame = Frame()
    frame.add_roll(3)
    frame.add_roll(4)
    assert frame.is_complete


def test_strike_completes_frame_in_one_roll():
    frame = Frame()
    frame.add_roll(10)
    assert frame.is_complete
