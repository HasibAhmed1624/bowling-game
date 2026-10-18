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


def test_spare_requires_two_rolls_totalling_ten():
    frame = Frame()
    frame.add_roll(5)
    assert not frame.is_spare
    frame.add_roll(5)
    assert frame.is_spare


def test_strike_is_not_a_spare():
    frame = Frame()
    frame.add_roll(10)
    assert not frame.is_spare


def test_strike_is_first_roll_of_ten():
    frame = Frame()
    assert not frame.is_strike
    frame.add_roll(10)
    assert frame.is_strike


def test_non_ten_first_roll_is_not_a_strike():
    frame = Frame()
    frame.add_roll(9)
    assert not frame.is_strike


def test_pins_is_sum_of_rolls():
    frame = Frame()
    frame.add_roll(3)
    frame.add_roll(4)
    assert frame.pins == 7
