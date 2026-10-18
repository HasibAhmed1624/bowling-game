from bowling_game.gui.logic import (
    EXPECTED_TOTALS,
    PLAYER_SERIES,
    cumulatives,
    expand_series,
    marks,
    play,
)


def test_expand_series_ada():
    assert expand_series(PLAYER_SERIES["Ada"]) == [
        10, 7, 2, 8, 2, 9, 0, 10, 3, 4, 6, 4, 5, 3, 7, 1, 7, 3, 8,
    ]


def test_expand_series_grace():
    assert expand_series(PLAYER_SERIES["Grace"]) == [
        3, 4, 10, 10, 9, 1, 6, 2, 10, 8, 1, 10, 10, 10, 10, 10,
    ]


def test_scripted_series_reach_their_expected_totals():
    for name, spec in PLAYER_SERIES.items():
        assert play(expand_series(spec)).score() == EXPECTED_TOTALS[name]


def test_marks_use_scorecard_notation():
    assert marks([10, 3, 7]) == ["X", "3", "/"]
    assert marks([0, 5, 5, 3]) == ["-", "5", "/", "3"]
    assert marks([10, 10, 10]) == ["X", "X", "X"]


def test_cumulatives_blank_until_frame_is_scored():
    assert cumulatives([17, 7, 12, 5, None]) == [17, 24, 36, 41, None]
