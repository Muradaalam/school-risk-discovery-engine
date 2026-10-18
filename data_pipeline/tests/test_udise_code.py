import unittest

from data_pipeline.normalization.udise_code import normalize_udise_code, match_udise_codes


class TestUdiseCode(unittest.TestCase):

    def test_valid_code(self):
        result = normalize_udise_code("08200612501")
        self.assertEqual(result, "08200612501")

    def test_whitespace_removed(self):
        result = normalize_udise_code(" 08200612501 ")
        self.assertEqual(result, "08200612501")

    def test_leading_zero_preserved(self):
        result = normalize_udise_code("08200612501")
        self.assertTrue(result.startswith("0"))

    def test_short_code_rejected(self):
        with self.assertRaises(ValueError):
            normalize_udise_code("8200612501")

    def test_non_digit_rejected(self):
        with self.assertRaises(ValueError):
            normalize_udise_code("0820061250A")

    def test_non_string_rejected(self):
        with self.assertRaises(TypeError):
            normalize_udise_code(8200612501)

    def test_matching_codes(self):
        result = match_udise_codes("08200612501", " 08200612501 ")
        self.assertTrue(result)

    def test_different_codes(self):
        result = match_udise_codes("08200612501", "08200612502")
        self.assertFalse(result)

    def test_missing_code(self):
        result = match_udise_codes(None, "08200612501")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()