class Frame:
    def __init__(self) -> None:
        self._rolls: list[int] = []

    def add_roll(self, pins: int) -> None:
        self._rolls.append(pins)

    @property
    def is_complete(self) -> bool:
        if not self._rolls:
            return False
        return self._rolls[0] == 10 or len(self._rolls) == 2
