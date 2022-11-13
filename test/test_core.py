import unittest

from eole.core import UpdateMethod


class TestUpdateMethod(unittest.TestCase):
    def test_safe_parse_ok(self):
        self.assertEqual(
            UpdateMethod.safe_parse("MANUAL"),
            UpdateMethod.MANUAL,
            "Should be MANUAL",
        )

    def test_safe_parse_unknown(self):
        self.assertEqual(
            UpdateMethod.safe_parse("TOTO"),
            UpdateMethod.UNKNOWN,
            "Should be UNKNOWN",
        )


if __name__ == "__main__":
    unittest.main()
