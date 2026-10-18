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
