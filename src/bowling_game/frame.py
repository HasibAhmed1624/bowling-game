class Frame:
    def __init__(self) -> None:
        self._rolls: list[int] = []

    def add_roll(self, pins: int) -> None:
        self._rolls.append(pins)

    def __len__(self) -> int:
        return len(self._rolls)

    @property
    def rolls(self) -> tuple[int, ...]:
        return tuple(self._rolls)

    @property
    def pins(self) -> int:
        return sum(self._rolls)

    @property
    def is_complete(self) -> bool:
        return self.is_strike or len(self._rolls) >= 2

    @property
    def is_spare(self) -> bool:
        return len(self._rolls) == 2 and self.pins == 10

    @property
    def is_strike(self) -> bool:
        return bool(self._rolls) and self._rolls[0] == 10
