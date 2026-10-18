from bowling_game.frames import Frames


class Game:
    def __init__(self) -> None:
        self._frames = Frames()

    def roll(self, pins: int) -> None:
        self._frames.add_roll(pins)

    def score(self) -> int:
        return self._frames.score()

    @property
    def frame_number(self) -> int:
        return self._frames.number

    @property
    def rolls_per_frame(self) -> list[tuple[int, ...]]:
        return self._frames.rolls_per_frame

    def frame_scores(self) -> list[int | None]:
        return self._frames.frame_scores()
