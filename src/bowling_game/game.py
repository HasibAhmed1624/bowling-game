from bowling_game.frame import Frame


class Game:
    def __init__(self) -> None:
        self._rolls: list[int] = []
        self._frames: list[Frame] = [Frame()]

    def roll(self, pins: int) -> None:
        self._rolls.append(pins)
        frame = self._frames[-1]
        frame.add_roll(pins)
        if frame.is_complete and len(self._frames) < 10:
            self._frames.append(Frame())

    def score(self) -> int:
        return sum(self._rolls)

    @property
    def frame_number(self) -> int:
        return len(self._frames)
