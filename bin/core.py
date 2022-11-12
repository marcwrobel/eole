from enum import Enum


# Available update methods in eole.
class UpdateMethod(Enum):
    MANUAL = 1
    GITHUB = 2


class Version:
    def __init__(self, name, date) -> None:
        self.name = name
        self.date = date

    def __str__(self) -> str:
        return f"{self.name} ({self.date})"
