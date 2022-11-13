"""Common types, enum and routines used by eole."""

from enum import Enum


class UpdateMethod(Enum):
    """References available update methods in eole."""

    MANUAL = 1
    """Manual update"""

    GITHUB = 2
    """Update based on GitHub information.
    """


class Version:
    """Holds data about a version."""

    def __init__(self, name, date) -> None:
        """Creates a version using the given data.

        Args:
            name (str): the version name (e.g. 1.2.3)
            date (date): the version release date (e.g. 2022-01-01)
        """
        self.name = name
        self.date = date

    def __str__(self) -> str:
        return f"{self.name} ({self.date})"
