"""Pure display logic for the Tk scorecard — no tkinter imports here.

The two-player demo series are scripted as frame *intents* so the rolls are
always legal (spares/strikes pay off, opens stay under 10) and the game is
reproducible — you can re-watch the same game to follow the scoring.
"""

from collections.abc import Sequence

from bowling_game.game import Game

# Frame intents: ("strike", [bonus...]) | ("spare", a, b, [bonus...]) | ("open", a, b)
# Only the 10th frame carries bonus rolls inside its own intent.
PLAYER_SERIES: dict[str, tuple] = {
    "Ada": (
        ("strike",),
        ("open", 7, 2),
        ("spare", 8, 2),
        ("open", 9, 0),
        ("strike",),
        ("open", 3, 4),
        ("spare", 6, 4),
        ("open", 5, 3),
        ("open", 7, 1),
        ("spare", 7, 3, 8),
    ),
    "Grace": (
        ("open", 3, 4),
        ("strike",),
        ("strike",),
        ("spare", 9, 1),
        ("open", 6, 2),
        ("strike",),
        ("open", 8, 1),
        ("strike",),
        ("strike",),
        ("strike", 10, 10),
    ),
}

EXPECTED_TOTALS: dict[str, int] = {"Ada": 129, "Grace": 198}


def expand_series(frames_spec: Sequence[tuple]) -> list[int]:
    rolls: list[int] = []
    for spec in frames_spec:
        kind = spec[0]
        if kind == "strike":
            rolls.append(10)
            rolls.extend(spec[1:])
        elif kind == "spare":
            a, b = spec[1], spec[2]
            rolls.extend((a, b))
            rolls.extend(spec[3:])
        else:
            a, b = spec[1], spec[2]
            assert a + b < 10, "open frame must leave pins standing"
            rolls.extend((a, b))
    return rolls


def marks(rolls: Sequence[int]) -> list[str]:
    """Bowling scorecard notation: X strike, / spare, - zero, else digit."""
    out: list[str] = []
    for i, r in enumerate(rolls):
        if r == 10:
            out.append("X")
        elif i > 0 and rolls[i - 1] != 10 and rolls[i - 1] + r == 10:
            out.append("/")
        elif r == 0:
            out.append("-")
        else:
            out.append(str(r))
    return out


def cumulatives(frame_scores: Sequence[int | None]) -> list[int | None]:
    """Running totals: cumulative once a frame is scored, None while pending."""
    out: list[int | None] = []
    running = 0
    for score in frame_scores:
        if score is None:
            out.append(None)
        else:
            running += score
            out.append(running)
    return out


def narrate(
    name: str,
    pins: int,
    game: Game,
    previous_scores: Sequence[int | None],
) -> tuple[list[str], list[int | None]]:
    """Lines explaining a ball just rolled, plus the game's new frame scores.

    Call after `game.roll(pins)`. Frame scores only appear once their bonus
    rolls have landed, so a strike's line can be several balls late.
    """
    rolls_per_frame = game.rolls_per_frame
    frame_index = max(i for i, rolls in enumerate(rolls_per_frame) if rolls)
    frame = rolls_per_frame[frame_index]
    frame_number = frame_index + 1

    lines: list[str] = []
    if len(frame) == 1 and frame[0] == 10:
        lines.append(f"{name} — frame {frame_number}: STRIKE. Scores 10 + the next two rolls.")
    elif pins == 10:
        lines.append(f"{name} — frame {frame_number}: rolled 10 (bonus ball).")
    else:
        lines.append(f"{name} — frame {frame_number}: rolled {pins}.")
    if len(frame) == 2 and sum(frame) == 10:
        lines.append(f"{name} — frame {frame_number}: spare! Scores 10 + the next roll.")

    scores = game.frame_scores()
    for index, score in enumerate(scores):
        was = previous_scores[index] if index < len(previous_scores) else None
        if score is not None and was is None:
            notation = " ".join(marks(rolls_per_frame[index]))
            lines.append(f"    {name} frame {index + 1} final: {notation} → {score} pins")
    return lines, scores


def play(series: Sequence[int]) -> Game:
    game = Game()
    for pins in series:
        game.roll(pins)
    return game
