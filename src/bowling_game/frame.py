class Frame:
    def __init__(self) -> None:
        self._rolls: list[int] = []

    def add_roll(self, pins: int) -> None:
        self._rolls.append(pins)

    def __len__(self) -> int:
        return len(self._rolls)

    @property
    def pins(self) -> int:
        return sum(self._rolls)

    @property
    def is_complete(self) -> bool:
        if not self._rolls:
            return False
        return self._rolls[0] == 10 or len(self._rolls) == 2

    @property
    def is_spare(self) -> bool:
        return len(self._rolls) == 2 and self.pins == 10
