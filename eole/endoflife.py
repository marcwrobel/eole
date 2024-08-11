"""endoflife.date types."""

import logging
from enum import Enum


class UpdateMethod(Enum):
    """References available update methods in eole."""

    manual = 1
    """Manual update"""

    unsupported = 9998
    """Unsupported update method"""

    unspecified = 9999
    """unknown update method"""

    @staticmethod
    def safe_parse(s):
        try:
            return UpdateMethod[s]
        except KeyError:
            logging.warning("unsupported method '%s'", s)
            return UpdateMethod.unsupported


class FrontMatter:
    """Access to a product front matter data."""

    def __init__(self, data) -> None:
        self.data = data

    def update_method(self) -> UpdateMethod:
        if "auto_update" in self.data and "method" in self.data["auto_update"]:
            return UpdateMethod.safe_parse(self.data["auto_update"]["method"])

        return UpdateMethod.unspecified
