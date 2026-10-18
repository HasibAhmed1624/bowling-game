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

    @property
    def rolls_per_frame(self) -> list[tuple[int, ...]]:
        return [frame.rolls for frame in self._frames]

    def score(self) -> int:
        return sum(score for score in self.frame_scores() if score is not None)

    def frame_scores(self) -> list[int | None]:
        scores: list[int | None] = []
        index = 0
        for frame in self._frames:
            if frame.is_strike:
                if index + 2 >= len(self._rolls):
                    scores.append(None)
                else:
                    scores.append(10 + self._rolls[index + 1] + self._rolls[index + 2])
                index += 1
            elif frame.is_spare:
                if index + 2 >= len(self._rolls):
                    scores.append(None)
                else:
                    scores.append(10 + self._rolls[index + 2])
                index += 2
            elif frame.is_complete:
                scores.append(frame.pins)
                index += len(frame)
            else:
                scores.append(None)
                index += len(frame)
        return scores
