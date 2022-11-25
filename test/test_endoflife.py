import unittest

from eole.endoflife import FrontMatter, UpdateMethod


class TestUpdateMethod(unittest.TestCase):
    def test_safe_parse_ok(self):
        self.assertEqual(
            UpdateMethod.safe_parse("manual"),
            UpdateMethod.manual,
            "Should be manual",
        )

    def test_safe_parse_unknown(self):
        self.assertEqual(
            UpdateMethod.safe_parse("TOTO"),
            UpdateMethod.unsupported,
            "Should be unsupported",
        )


class TestFrontMatter(unittest.TestCase):
    def test_no_update_method(self):
        metadata = FrontMatter({"auto_update": {}})
        self.assertEqual(
            metadata.update_method(),
            UpdateMethod.unspecified,
            "Should be unspecified",
        )

    def test_unknown_update_method(self):
        metadata = FrontMatter(
            {"auto_update": {"method": "unsupported method"}}
        )
        self.assertEqual(
            metadata.update_method(),
            UpdateMethod.unsupported,
            "Should be unsupported",
        )


if __name__ == "__main__":
    unittest.main()
