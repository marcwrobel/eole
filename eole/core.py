"""Common types, enum and routines used by eole."""
import sys
from enum import Enum

import frontmatter


class UpdateMethod(Enum):
    """References available update methods in eole."""

    MANUAL = 1
    """Manual update"""

    GITHUB = 2
    """Update based on GitHub information."""

    UNKNOWN = 999
    """Manual update"""

    @staticmethod
    def safe_parse(s):
        try:
            return UpdateMethod[s]
        except KeyError:
            print(f"Unknown method '{s}'", file=sys.stderr)
            return UpdateMethod.UNKNOWN


class Metadata:
    """Holds a product metadata."""

    def __init__(self, path) -> None:
        with open(path, "r") as f:
            metadata = frontmatter.load(f)
            update_versions = metadata["update"]["versions"]

            self.name = metadata["name"]
            self.category = metadata["category"]
            self.category = metadata["name"]
            self.update_version_method = UpdateMethod.safe_parse(
                update_versions["method"]
            )
            self.update_version_specs = {
                "owner": update_versions["owner"],
                "repo": update_versions["repo"],
            }


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
