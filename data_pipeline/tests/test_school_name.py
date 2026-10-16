import unittest

from data_pipeline.normalization.school_name import (normalize_school_name)


class TestSchoolNameNormalization(unittest.TestCase):

    def test_uppercase_name(self):
        result = normalize_school_name("SIRIYARI SCHOOL")
        self.assertEqual(result, "siriyari school")

    def test_punctuation(self):
        result = normalize_school_name("G.SR.SEC. SIRIYARI")
        self.assertEqual(result, "g sr sec siriyari")

    def test_extra_spaces(self):
        result = normalize_school_name("  G  SR  SEC   SIRIYARI  ")
        self.assertEqual(result, "g sr sec siriyari")

    def test_equivalent_names(self):
        first = normalize_school_name("G.SR.SEC. SIRIYARI")
        second = normalize_school_name("g sr sec siriyari")

        self.assertEqual(first, second)

    def test_hindi_name(self):
        result = normalize_school_name("राजकीय विद्यालय, सिरियारी")
        self.assertEqual(result, "राजकीय विद्यालय सिरियारी")

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            normalize_school_name("   ")

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            normalize_school_name(123)

    def test_different_names_remain_different(self):
        first = normalize_school_name("SIRIYARI SCHOOL")
        second = normalize_school_name("SOJAT SCHOOL")

        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
