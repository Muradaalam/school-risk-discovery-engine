import unittest

from data_pipeline.matching.school import SchoolCandidate, MatchStatus, match_schools


class TestSchoolMatching(unittest.TestCase):

    def test_matching_udise(self):
        first = SchoolCandidate("G.SR.SEC. SIRIYARI", "Pali", "Marwar Junction", "08200612501")
        second = SchoolCandidate("Government School Siriyari", "Pali", "Marwar Junction", "08200612501")

        result = match_schools(first, second)
        self.assertEqual(result.status, MatchStatus.CONFIRMED)

    def test_matching_without_udise(self):
        first = SchoolCandidate("G.SR.SEC. SIRIYARI", "Pali", "Marwar Junction")
        second = SchoolCandidate("g sr sec siriyari", "PALI", "Marwar Junction")

        result = match_schools(first, second)
        self.assertEqual(result.status, MatchStatus.POSSIBLE)

    def test_one_missing_udise(self):
        first = SchoolCandidate("SIRIYARI SCHOOL", "Pali", "Marwar Junction", "08200612501")
        second = SchoolCandidate("Siriyari School", "Pali", "Marwar Junction")

        result = match_schools(first, second)
        self.assertEqual(result.status, MatchStatus.POSSIBLE)

    def test_different_udise(self):
        first = SchoolCandidate("SIRIYARI SCHOOL", udise_code="08200612501")
        second = SchoolCandidate("SIRIYARI SCHOOL", udise_code="08200612502")

        result = match_schools(first, second)
        self.assertEqual(result.status, MatchStatus.NO_MATCH)

    def test_different_district(self):
        first = SchoolCandidate("Rampura School", "Pali", "Marwar Junction")
        second = SchoolCandidate("Rampura School", "Jaipur", "Marwar Junction")

        result = match_schools(first, second)
        self.assertEqual(result.status, MatchStatus.NO_MATCH)

    def test_insufficient_information(self):
        first = SchoolCandidate("Government School Rampura")
        second = SchoolCandidate("Govt School Rampura")

        result = match_schools(first, second)
        self.assertEqual(result.status, MatchStatus.UNRESOLVED)

    def test_school_without_udise_is_accepted(self):
        school = SchoolCandidate("Government School Rampura", "Pali")

        self.assertIsNone(school.udise_code)


if __name__ == "__main__":
    unittest.main()
