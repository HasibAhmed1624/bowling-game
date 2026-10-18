from bowling_game.game import Game
from bowling_game.gui.logic import (
    EXPECTED_TOTALS,
    PLAYER_SERIES,
    cumulatives,
    expand_series,
    marks,
    narrate,
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


def _narrated_ball(game, name, pins, previous):
    game.roll(pins)
    return narrate(name, pins, game, previous)


def test_strike_is_narrated_with_the_frame_the_ball_landed_in():
    game = Game()
    lines, _ = _narrated_ball(game, "Ada", 10, [])
    assert lines[0] == "Ada — frame 1: STRIKE. Scores 10 + the next two rolls."


def test_spare_is_announced_against_its_own_frame():
    game = Game()
    previous: list = []
    for pins in (3, 4, 8, 2):
        lines, previous = _narrated_ball(game, "Ada", pins, previous)
    assert "Ada — frame 2: spare! Scores 10 + the next roll." in lines


def test_tenth_frame_bonus_strike_ball_is_labelled_as_bonus():
    game = Game()
    previous: list = []
    for pins in (*([0] * 18), 10):
        lines, previous = _narrated_ball(game, "Ada", pins, previous)
    lines, _ = _narrated_ball(game, "Ada", 10, previous)
    assert lines[0] == "Ada — frame 10: rolled 10 (bonus ball)."


def test_frame_final_line_waits_for_its_bonus_rolls():
    game = Game()
    previous: list = []
    logs: list[str] = []
    for pins in (3, 4, 10, 10, 9, 1):
        lines, previous = _narrated_ball(game, "Grace", pins, previous)
        logs.extend(lines)
    assert "    Grace frame 2 final: X → 29 pins" in logs


def test_final_lines_name_the_player_and_use_scorecard_notation():
    game = Game()
    previous: list = []
    logs: list[str] = []
    for pins in (10, 7, 2):
        lines, previous = _narrated_ball(game, "Ada", pins, previous)
        logs.extend(lines)
    assert "    Ada frame 1 final: X → 19 pins" in logs
    assert "    Ada frame 2 final: 7 2 → 9 pins" in logs


def test_narrating_a_full_scripted_game_reaches_the_expected_total():
    game = Game()
    previous: list = []
    for pins in expand_series(PLAYER_SERIES["Ada"]):
        _, previous = _narrated_ball(game, "Ada", pins, previous)
    assert game.score() == EXPECTED_TOTALS["Ada"]
