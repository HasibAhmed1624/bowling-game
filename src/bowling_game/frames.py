from bowling_game.frame import Frame


class Frames:
    def __init__(self) -> None:
        self._rolls: list[int] = []
        self._frames: list[Frame] = [Frame()]

    def add_roll(self, pins: int) -> None:
        self._rolls.append(pins)
        frame = self._frames[-1]
        frame.add_roll(pins)
        if frame.is_complete and len(self._frames) < 10:
            self._frames.append(Frame())

    @property
    def number(self) -> int:
        return len(self._frames)

    def score(self) -> int:
        total = 0
        index = 0
        for frame in self._frames:
            if frame.is_strike:
                total += 10 + self._rolls[index + 1] + self._rolls[index + 2]
                index += 1
            elif frame.is_spare:
                total += 10 + self._rolls[index + 2]
                index += 2
            else:
                total += frame.pins
                index += len(frame)
        return total
